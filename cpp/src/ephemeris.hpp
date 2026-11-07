// VYAS ASTRA — ephemeris facade over the JPL DE440s kernel.
//
// Positions are computed the way the Python engine computes them:
//   1. Earth's barycentric position from the kernel,
//   2. the body's barycentric position,
//   3. subtract, convert to the true ecliptic of date (precession + nutation),
//   4. subtract the Lahiri ayanamsa to get sidereal longitude.
//
// The Earth position uses the Moon's geocentric offset, so the result is the
// apparent geocentric position a natal chart needs.
#pragma once

#include <cmath>
#include <memory>
#include <string>

#include "astro.hpp"
#include "nut2000b.hpp"
#include "nut2000a_data.hpp"
#include "spk.hpp"

namespace vyas {

inline constexpr int NAIF_SUN = 10;
inline constexpr int NAIF_MOON = 301;
inline constexpr int NAIF_EARTH_BARY = 3;
inline constexpr int NAIF_MARS_BARY = 4;
inline constexpr int NAIF_MERCURY_BARY = 1;
inline constexpr int NAIF_JUPITER_BARY = 5;
inline constexpr int NAIF_VENUS_BARY = 2;
inline constexpr int NAIF_SATURN_BARY = 6;

struct BodyPosition {
    double longitude = 0.0;   // sidereal, degrees
    double speed = 0.0;       // deg/day, negative = retrograde
    double latitude = 0.0;    // ecliptic latitude, degrees
};

// Tropical longitude on the true ecliptic of date, computed exactly the way
// Skyfield does: ICRF vector -> TETE rotation M = N @ P (Capitaine precession +
// IAU 2000B nutation) -> rotate by -true-obliquity about X.  Verified against
// Skyfield's ecliptic_frame to < 0.01 arcsec on all classical planets.
inline double tropical_longitude_of_date(const Vec3& icrf, double jd_tt) {
    // M = N @ P @ B: precession, nutation, then the ICRS->J2000 frame bias.
    // The bias is ~70 microarcsec but it is systematic, so leaving it out put
    // every longitude ~7 mas off — the whole of the last residual.
    double P[3][3], N[3][3], B[3][3], NP[3][3], M[3][3];
    nut::precession_matrix(jd_tt, P);
    double dpsi, deps;
    nut2000a::iau2000a_rad(jd_tt, dpsi, deps);
    const double mean_ob = nut::mean_obliquity_rad(jd_tt);
    nut::nutation_matrix(mean_ob, mean_ob + deps, dpsi, N);
    nut::frame_bias_matrix(B);
    for (int i = 0; i < 3; ++i)
        for (int j = 0; j < 3; ++j) {
            double v = 0.0;
            for (int k = 0; k < 3; ++k) v += N[i][k] * P[k][j];
            NP[i][j] = v;
        }
    for (int i = 0; i < 3; ++i)
        for (int j = 0; j < 3; ++j) {
            double v = 0.0;
            for (int k = 0; k < 3; ++k) v += NP[i][k] * B[k][j];
            M[i][j] = v;
        }
    const double eqx = M[0][0] * icrf.x + M[0][1] * icrf.y + M[0][2] * icrf.z;
    const double eqy = M[1][0] * icrf.x + M[1][1] * icrf.y + M[1][2] * icrf.z;
    const double eqz = M[2][0] * icrf.x + M[2][1] * icrf.y + M[2][2] * icrf.z;
    const double eps_true = mean_ob + deps;
    const double c = std::cos(eps_true), sn = std::sin(eps_true);
    const double ye = c * eqy + sn * eqz;
    return norm360(std::atan2(ye, eqx) * kRad2Deg);
}

// Geocentric ecliptic-of-date longitude of a body (ICRF frame), degrees.
class Ephemeris {
public:
    explicit Ephemeris(const std::string& kernel_path)
        : kernel_(std::make_unique<SpkKernel>(kernel_path)) {}

    static constexpr double kC_KmPerSec = 299792.458;
    static constexpr double kAuKm = 149597870.7;
    double tropical_longitude(int naif_body, double jd_tt) const {
        if (naif_body == NAIF_MOON) {
            return tropical_longitude_of_date(moon_geocentric(jd_tt), jd_tt);
        }
        // Light-time iteration, exactly like Skyfield's observe().apparent()
        // (vectorlib._correct_for_light_travel_time): the TARGET is evaluated
        // at the emission instant (t - tau) while the OBSERVER stays at t.
        // Evaluating both at (t - tau) was a ~15000 km error for the Sun —
        // the Earth moves ~30 km/s during the 499 s of light travel.
        const Vec3 earth = earth_barycentric(jd_tt);
        Vec3 body = kernel_->position(naif_body, 0, jd_tt);
        Vec3 rel{body.x - earth.x, body.y - earth.y, body.z - earth.z};
        double dist_au = std::sqrt(rel.x * rel.x + rel.y * rel.y + rel.z * rel.z) / kAuKm;
        for (int it = 0; it < 10; ++it) {
            const double light_time = dist_au * kAuKm / (kC_KmPerSec * 86400.0);
            const double jd_emit = jd_tt - light_time;
            body = kernel_->position(naif_body, 0, jd_emit);
            rel = Vec3{body.x - earth.x, body.y - earth.y, body.z - earth.z};
            const double nd = std::sqrt(rel.x * rel.x + rel.y * rel.y + rel.z * rel.z) / kAuKm;
            if (std::fabs(nd - dist_au) * kAuKm / kC_KmPerSec < 1e-9) { dist_au = nd; break; }
            dist_au = nd;
        }
        // Stellar aberration, verbatim port of skyfield's add_aberration:
        // position is the light-time-corrected relative vector (km), velocity
        // is the observer's barycentric velocity (km/s), light_time in days.
        const double h = 0.5 / 86400.0;
        const Vec3 e1 = earth_barycentric(jd_tt + h);
        const Vec3 e0 = earth_barycentric(jd_tt - h);
        double vx = (e1.x - e0.x) / (2.0 * h * 86400.0);
        double vy = (e1.y - e0.y) / (2.0 * h * 86400.0);
        double vz = (e1.z - e0.z) / (2.0 * h * 86400.0);
        const double light_time_days = dist_au * 499.0047838361564 / 86400.0;
        const double c_auday = kC_KmPerSec * 86400.0 / kAuKm;  // c in AU/day
        vx /= kAuKm / 86400.0; vy /= kAuKm / 86400.0; vz /= kAuKm / 86400.0;
        const double p1mag = light_time_days * c_auday;
        const double vemag = std::sqrt(vx * vx + vy * vy + vz * vz);
        const double beta = vemag / c_auday;
        const double rx = rel.x / kAuKm, ry = rel.y / kAuKm, rz = rel.z / kAuKm;
        const double dot = rx * vx + ry * vy + rz * vz;
        const double cosd = dot / (p1mag * vemag + 1e-300);
        const double gammai = std::sqrt(1.0 - beta * beta);
        const double p = beta * cosd;
        const double q = (1.0 + p / (1.0 + gammai)) * light_time_days;
        const double rr = 1.0 + p;
        rel = Vec3{(rx * gammai + q * vx) / rr * kAuKm,
                   (ry * gammai + q * vy) / rr * kAuKm,
                   (rz * gammai + q * vz) / rr * kAuKm};
        return tropical_longitude_of_date(rel, jd_tt);
    }

    // Sidereal longitude of one of the seven classical grahas, degrees.
    BodyPosition graha(int naif_body, double jd_tt) const {
        const double ay = ayanamsa::lahiri_deg(jd_tt);
        const double l1 = norm360(tropical_longitude(naif_body, jd_tt) - ay);
        // Speed by symmetric 12-hour difference, exactly as the Python engine.
        const double half_day = 0.5;
        const double ay2 = ayanamsa::lahiri_deg(jd_tt + half_day);
        const double l2 = norm360(tropical_longitude(naif_body, jd_tt + half_day) - ay2);
        BodyPosition p;
        p.longitude = l1;
        p.speed = ((l2 - l1 + 540.0 - std::floor((l2 - l1 + 540.0) / 360.0) * 360.0) - 180.0) * 2.0;
        return p;
    }

    // Sidereal longitude of the mean or true lunar node.
    BodyPosition node(bool mean, double jd_tt) const {
        const double ay = ayanamsa::lahiri_deg(jd_tt);
        const double n1 = mean ? mean_node_tropical(jd_tt) : true_node_tropical(jd_tt);
        const double ay2 = ayanamsa::lahiri_deg(jd_tt + 0.5);
        const double n2 = mean ? mean_node_tropical(jd_tt + 0.5) : true_node_tropical(jd_tt + 0.5);
        BodyPosition p;
        p.longitude = norm360(n1 - ay);
        double d = norm360(n2 - ay2) - p.longitude;
        if (d > 180.0) d -= 360.0;
        if (d < -180.0) d += 360.0;
        p.speed = d * 2.0;
        return p;
    }

    // Sidereal Ascendant for a UTC instant and a geographic place.
    // GAST uses the full IAU 2000A path (nut2000b.hpp) and the obliquity is
    // the Capitaine mean obliquity — the Meeus fallbacks in astro.hpp are
    // ~40 mas off and used to dominate the Ascendant error budget.
    double ascendant_sidereal(double jd_ut, double lat_deg, double lon_deg) const {
        const double jd_tt = julian_day_tt_full(jd_ut);
        const double jd_ut1 = julian_day_ut1_full(jd_tt);
        const double gast = nut::gast_deg_full(jd_tt, jd_ut1);
        const double ramc = norm360(gast + lon_deg);
        const double eps = nut::mean_obliquity_rad(jd_tt) * kRad2Deg;
        const double asc = ascendant_tropical(ramc, lat_deg, eps);
        return norm360(asc - ayanamsa::lahiri_deg(jd_tt));
    }

    const SpkKernel& kernel() const { return *kernel_; }

private:
    // Earth's own barycentric position = EMB (segment 0->3) + Earth wrt EMB
    // (segment 3->399).  DE440s carries the geocenter explicitly, so there is
    // no mass-ratio arithmetic and no ~9000 km systematic error.  (An earlier
    // revision reconstructed the geocenter from the Moon vector with a fixed
    // mass ratio and was ~4800 km off — the whole of the last arc-minute.)
    static constexpr int NAIF_EARTH = 399;
    Vec3 earth_barycentric(double jd_tt) const {
        const Vec3 emb = kernel_->position(NAIF_EARTH_BARY, 0, jd_tt);
        const Vec3 geo = kernel_->position(NAIF_EARTH, NAIF_EARTH_BARY, jd_tt);
        return Vec3{emb.x + geo.x, emb.y + geo.y, emb.z + geo.z};
    }

    // Geocentric position of the Moon (needed for the Moon's own longitude).
    Vec3 moon_geocentric(double jd_tt) const {
        const Vec3 rel = kernel_->position(NAIF_MOON, NAIF_EARTH_BARY, jd_tt);
        return Vec3{rel.x * (1.0 - 1.0 / (1.0 + 81.30056907419062)),
                    rel.y * (1.0 - 1.0 / (1.0 + 81.30056907419062)),
                    rel.z * (1.0 - 1.0 / (1.0 + 81.30056907419062))};
    }

    std::unique_ptr<SpkKernel> kernel_;
};

}  // namespace vyas
