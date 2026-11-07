// VYAS ASTRA — a self-contained reader for the JPL DE440s SPK kernel.
//
// DE440s ships as a "DAF/SPK Type 2 (Chebyshev) — little-endian" file: a
// Chebyshev polynomial per body, per time segment, evaluated on normalised
// intervals.  This reader implements exactly what a natal chart needs and
// nothing more, so the C++ engine has no external astronomy dependency and
// reads the very same 32 MB kernel the Python engine uses.
#pragma once

#include <cstdint>
#include <cstring>
#include <cmath>
#include <fstream>
#include <stdexcept>
#include <string>
#include <vector>

#include "astro.hpp"  // delta_t_seconds

namespace vyas {

class SpkError : public std::runtime_error {
public:
    explicit SpkError(const std::string& what) : std::runtime_error(what) {}
};

// 3-vector in kilometres.
struct Vec3 {
    double x, y, z;
};

class SpkKernel {
public:
    // Reads the whole DAF into memory (32 MB for de440s.bsp) and validates the
    // header.  Throws SpkError on any structural problem.
    explicit SpkKernel(const std::string& path) {
        std::ifstream f(path, std::ios::binary);
        if (!f) throw SpkError("cannot open SPK kernel: " + path);
        f.seekg(0, std::ios::end);
        const auto size = static_cast<std::size_t>(f.tellg());
        f.seekg(0, std::ios::beg);
        if (size < 632) throw SpkError("SPK kernel is truncated: " + path);
        buf_.resize(size);
        f.read(reinterpret_cast<char*>(buf_.data()), static_cast<std::streamsize>(size));
        if (!f) throw SpkError("short read on SPK kernel: " + path);

        if (std::string(reinterpret_cast<const char*>(buf_.data()), 8) != "DAF/SPK ") {
            throw SpkError("not a DAF/SPK file: " + path);
        }
        // ND, NI are little-endian int32 at offsets 8 and 12.
        nd_ = read_i32(8);
        ni_ = read_i32(12);
        if (nd_ != 2) throw SpkError("only double-precision SPK kernels are supported");
        const int fward = read_i32(76);
        if (fward <= 0) throw SpkError("SPK has no segment summary records");
        // A DAF summary record is 1024 bytes: two little-endian doubles
        // (NEXT, PREV as 64-bit addresses) followed by NSUM as a double.
        const std::size_t rec = static_cast<std::size_t>(fward - 1) * 1024;
        const double nsum = read_f64(rec + 16);
        summary_ = static_cast<int>(nsum);
        if (summary_ <= 0) throw SpkError("SPK summary count is zero");
    }

    struct Segment {
        double start_sec, end_sec;      // seconds past J2000 (TDB)
        int target, center, frame, type;
        int start_word, end_word;       // 1-based addresses of the data
    };

    // All segments that target `body` (NAIF id) from `center`.  The `frame` field
    // tells us which rotation applies: frame 1 = J2000/ICRF (SSB segments),
    // frame 17 = ECLIPJ2000 / of-date (planetocentric segments).
    std::vector<Segment> segments_for(int body, int center) const {
        std::vector<Segment> out;
        const int fward = read_i32(76);
        // Segment descriptors start 3 doubles into the summary record and each
        // one is 2 doubles (start/end) + NI int32 values.
        const std::size_t summary_base =
            static_cast<std::size_t>(fward - 1) * 1024 + 24;
        const std::size_t stride = 16 + static_cast<std::size_t>(ni_) * 4;
        for (int i = 0; i < summary_; ++i) {
            const std::size_t base = summary_base + static_cast<std::size_t>(i) * stride;
            Segment s;
            s.start_sec = read_f64(base);
            s.end_sec = read_f64(base + 8);
            s.target = read_i32(base + 16);
            s.center = read_i32(base + 20);
            s.frame = read_i32(base + 24);
            s.type = read_i32(base + 28);
            s.start_word = read_i32(base + 32);
            s.end_word = read_i32(base + 36);
            if (s.target == body && s.center == center) out.push_back(s);
        }
        return out;
    }

    // Raw 8-byte double at a 0-based byte offset (used by the tooling and by
    // unit tests that inspect a segment header).
    double raw_double(std::size_t byte_offset) const { return read_f64(byte_offset); }
    int raw_int(std::size_t byte_offset) const { return read_i32(byte_offset); }

    // Position of `body` relative to `center` at `jd_tt` (TDB ~ TT to <2 ms).
    Vec3 position(int body, int center, double jd_tt) const {
        auto segs = segments_for(body, center);
        if (segs.empty() && center != 0) {
            // No direct segment (DE440s carries the Moon only relative to the
            // Earth-Moon barycentre): fall back to SSB-relative and subtract.
            const Vec3 b = position(body, 0, jd_tt);
            const Vec3 c = position(center, 0, jd_tt);
            return Vec3{b.x - c.x, b.y - c.y, b.z - c.z};
        }
        if (segs.empty()) {
            throw SpkError("no SPK segment for body " + std::to_string(body));
        }
        // Segment times are seconds past J2000 on the TDB scale, and the
        // caller passes TT (TDB == TT to < 2 ms, far below our error budget),
        // so NO time-scale shift is applied here.  (An earlier revision
        // subtracted delta_t, evaluating every position ~64 s early -- the
        // Earth moves ~30 km/s, so that was a ~1900 km error.)
        const double seconds = (jd_tt - 2451545.0) * 86400.0;
        const Segment* chosen = nullptr;
        for (const auto& s : segs) {
            if (seconds >= s.start_sec && seconds <= s.end_sec) { chosen = &s; break; }
        }
        if (!chosen) {
            throw SpkError("time outside the SPK coverage for body " +
                           std::to_string(body) + " (segments: " +
                           std::to_string(segs.size()) + ")");
        }
        if (chosen->type != 2) {
            throw SpkError("only SPK type 2 (Chebyshev position) is supported");
        }
        // Type-2 record layout (decoded exactly the way jplephem does it, and
        // verified word-by-word against de440s.bsp):
        //   * the last four doubles of the segment are INIT (MID), INTLEN
        //     (RADIUS), RSIZE and N;
        //   * the coefficient block is [start, end - 4 words), reshaped as
        //     (N rows) x (RSIZE columns) = (MID, RADIUS, 3*(DEG+1) coeffs);
        //   * DEG + 1 = coefficient_count = (RSIZE - 2) / 3;
        //   * interval index and offset inside it:
        //       index, offset = divmod((tdb - T0)*86400 - INIT, INTLEN)
        //     (T0 = JD 2451545.0), evaluated with the Clenshaw recurrence
        //     over the reversed coefficient order.
        const std::size_t head = static_cast<std::size_t>(chosen->start_word - 1) * 8;
        const std::size_t seg_words =
            static_cast<std::size_t>(chosen->end_word - chosen->start_word + 1);
        if (seg_words < 8) throw SpkError("SPK type-2 segment is too short");

        const double init = read_f64(head + (seg_words - 4) * 8);
        const double intlen = read_f64(head + (seg_words - 3) * 8);
        const double rsize_d = read_f64(head + (seg_words - 2) * 8);
        const double n_d = read_f64(head + (seg_words - 1) * 8);
        const int records = static_cast<int>(n_d);
        const int rsize = static_cast<int>(rsize_d);
        if (records <= 0 || records > 1000000) {
            throw SpkError("SPK type-2 record has an invalid interval count");
        }
        if (rsize < 5 || ((rsize - 2) % 3) != 0) {
            throw SpkError("SPK type-2 record has an inconsistent coefficient size");
        }
        const int coeffs = (rsize - 2) / 3;   // per component per interval

        // (tdb - T0)*86400 - INIT, split into whole intervals + offset.
        const double since = seconds - init;
        int record = static_cast<int>(std::floor(since / intlen));
        double offset = since - static_cast<double>(record) * intlen;
        if (record < 0) record = 0;
        if (record >= records) { record = records - 1; offset = intlen; }

        // Chebyshev argument on [-1, +1] for this interval.
        const double t = 2.0 * offset / intlen - 1.0;

        Vec3 p{0.0, 0.0, 0.0};
        double* out[3] = {&p.x, &p.y, &p.z};
        // Row layout: (N rows) x (RSIZE = 2 + 3*(DEG+1) columns); the first two
        // columns of every row are that row's own MID/RADIUS copies, the rest
        // are the X, Y, Z coefficient blocks of length DEG+1 each.
        const std::size_t stride = static_cast<std::size_t>(rsize) * 8;
        const std::size_t row = head + static_cast<std::size_t>(record) * stride;
        for (int axis = 0; axis < 3; ++axis) {
            const std::size_t off = row + 16 +
                static_cast<std::size_t>(axis) *
                    static_cast<std::size_t>(coeffs) * 8;
            *out[axis] = chebyshev_rev(off, coeffs, t);
        }
        return p;
    }

private:
    std::vector<std::uint8_t> buf_;
    int nd_ = 0;
    int ni_ = 0;
    int summary_ = 0;

    float read_f32(std::size_t offset) const {
        if (offset + 4 > buf_.size()) throw SpkError("SPK read past end of file");
        std::uint32_t bits = static_cast<std::uint32_t>(buf_[offset]) |
                             (static_cast<std::uint32_t>(buf_[offset + 1]) << 8) |
                             (static_cast<std::uint32_t>(buf_[offset + 2]) << 16) |
                             (static_cast<std::uint32_t>(buf_[offset + 3]) << 24);
        float v;
        std::memcpy(&v, &bits, sizeof(v));
        return v;
    }

    double read_f64(std::size_t offset) const {
        if (offset + 8 > buf_.size()) throw SpkError("SPK read past end of file");
        std::uint64_t bits = 0;
        for (int i = 7; i >= 0; --i) bits = (bits << 8) | buf_[offset + static_cast<std::size_t>(i)];
        double v;
        std::memcpy(&v, &bits, sizeof(v));
        return v;
    }

    int read_i32(std::size_t offset) const {
        if (offset + 4 > buf_.size()) throw SpkError("SPK read past end of file");
        std::uint32_t v = static_cast<std::uint32_t>(buf_[offset]) |
                          (static_cast<std::uint32_t>(buf_[offset + 1]) << 8) |
                          (static_cast<std::uint32_t>(buf_[offset + 2]) << 16) |
                          (static_cast<std::uint32_t>(buf_[offset + 3]) << 24);
        return static_cast<int>(v);
    }

    // Clenshaw recurrence over the coefficients in the exact jplephem order:
    // the stored triple (X-block, Y-block, Z-block) is read with the highest
    // coefficient first per block, then the evaluation is the standard
    // Clenshaw sum.
    double chebyshev_rev(std::size_t offset, int n, double t) const {
        const double s2 = 2.0 * t;
        double w0 = 0.0, w1 = 0.0;
        // jplephem: for coefficient in coefficients[:-1] (highest first).
        for (int i = n - 1; i >= 1; --i) {
            const double c = read_f64(offset + static_cast<std::size_t>(i) * 8);
            const double w2 = w1;
            w1 = w0;
            w0 = c + (s2 * w1 - w2);
        }
        const double vlast = read_f64(offset);
        return vlast + (t * w0 - w1);
    }

};

}  // namespace vyas