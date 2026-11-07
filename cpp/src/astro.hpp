// VYAS ASTRA — core astronomical/time primitives (C++20, no dependencies)
//
// This is the C++ twin of src/vyas/ephem.py.  Everything here is deterministic
// and unit-testable: Julian day, ΔT, sidereal time, obliquity, nutation, the
// Lahiri (Chitrapaksha) ayanamsa, the Ascendant/MC formulae and the lunar nodes.
//
// The planetary positions themselves come from the JPL DE440s kernel through
// jplephem (see ephemeris.hpp) — the same kernel the Python engine uses, so
// both engines share one source of truth for the solar system.
#pragma once

#include "dut1_table.hpp"

#include <array>
#include <cmath>
#include <cstdint>
#include <string>

namespace vyas {

inline constexpr double kPi = 3.14159265358979323846;
inline constexpr double kTwoPi = 2.0 * kPi;
inline constexpr double kDeg2Rad = kPi / 180.0;
inline constexpr double kRad2Deg = 180.0 / kPi;

inline double norm360(double x) {
    double r = std::fmod(x, 360.0);
    if (r < 0.0) r += 360.0;
    return r;
}

// ---------------------------------------------------------------------------
// Calendar <-> Julian Day
// ---------------------------------------------------------------------------

// Gregorian calendar date + fractional UTC hours -> Julian Day (UTC scale).
inline double julian_day_utc(int year, int month, int day, double hour_utc) {
    int y = year;
    int m = month;
    if (m <= 2) { y -= 1; m += 12; }
    const int a = static_cast<int>(std::floor(y / 100.0));
    const int b = 2 - a + static_cast<int>(std::floor(a / 4.0));
    return std::floor(365.25 * (y + 4716)) + std::floor(30.6001 * (m + 1)) +
           day + b - 1524.5 + hour_utc / 24.0;
}

// ---------------------------------------------------------------------------
// ΔT = TT - UT1  (Espenak & Meeus polynomial fits, as used by Skyfield/NASA)
// ---------------------------------------------------------------------------

inline double delta_t_seconds(double jd_ut) {
    const double y = 2000.0 + (jd_ut - 2451545.0) / 365.25;
    if (y < -500) {
        const double u = (y - 1820.0) / 100.0;
        return -20.0 + 32.0 * u * u;
    }
    if (y < 500) {
        const double u = y / 100.0;
        return 10583.6 + u * (-1014.41 + u * (33.78311 + u * (-5.952053 +
               u * (-0.1798452 + u * (0.022174192 + u * 0.0090316521)))));
    }
    if (y < 1600) {
        const double u = (y - 1000.0) / 100.0;
        return 1574.2 + u * (-556.01 + u * (71.23472 + u * (0.319781 +
               u * (-0.8503463 + u * (-0.005050998 + u * 0.0083572073)))));
    }
    if (y < 1700) {
        const double t = y - 1600.0;
        return 120.0 + t * (-0.9808 + t * (-0.01532 + t / 7129.0));
    }
    if (y < 1800) {
        const double t = y - 1700.0;
        return 8.83 + t * (0.1603 + t * (-0.0059285 + t * (0.00013336 - t / 1174000.0)));
    }
    if (y < 1860) {
        const double t = y - 1800.0;
        return 13.72 + t * (-0.332447 + t * (0.0068612 + t * (0.0041116 +
               t * (-0.00037436 + t * (0.0000121272 + t * (-0.0000001699 +
               t * 0.000000000875))))));
    }
    if (y < 1900) {
        const double t = y - 1860.0;
        return 7.62 + t * (0.5737 + t * (-0.251754 + t * (0.01680668 +
               t * (-0.0004473624 + t / 233174.0))));
    }
    if (y < 1920) {
        const double t = y - 1900.0;
        return -2.79 + t * (1.494119 + t * (-0.0598939 + t * (0.0061966 - t * 0.000197)));
    }
    if (y < 1941) {
        const double t = y - 1920.0;
        return 21.20 + t * (0.84493 + t * (-0.076100 + t * 0.0020936));
    }
    if (y < 1961) {
        const double t = y - 1950.0;
        return 29.07 + t * (0.407 + t * (-1.0 / 233.0 + t / 2547.0));
    }
    if (y < 1986) {
        const double t = y - 1975.0;
        return 45.45 + t * (1.067 + t * (-1.0 / 260.0 - t / 718.0));
    }
    if (y < 2005) {
        const double t = y - 2000.0;
        return 63.86 + t * (0.3345 + t * (-0.060374 + t * (0.0017275 +
               t * (0.000651814 + t * 0.00002373599))));
    }
    if (y < 2050) {
        const double t = y - 2000.0;
        return 62.92 + t * (0.32217 + t * 0.005589);
    }
    if (y < 2150) {
        const double u = (y - 1820.0) / 100.0;
        return -20.0 + 32.0 * u * u - 0.5628 * (2150.0 - y);
    }
    const double u = (y - 1820.0) / 100.0;
    return -20.0 + 32.0 * u * u;
}

inline double julian_day_tt(double jd_ut) {
    return jd_ut + delta_t_seconds(jd_ut) / 86400.0;
}

// Full-precision pair, matching Skyfield's timescale: the IERS daily table
// gives delta_T as a function of TT, so UTC->TT iterates twice and TT->UT1
// subtracts the tabulated value.  Outside 1973..2027 the Espenak-Meeus
// polynomial is used (same as Skyfield's long-term parabola to < 1 s).
inline double dut1_delta_t(double jd_tt) {
    const double v = dut1::delta_t_interp(jd_tt);
    if (v < 1e299) return v;
    // Fall back: convert TT->UT1 approximately, then the polynomial.
    return delta_t_seconds(jd_tt - 65.0 / 86400.0);
}
inline double julian_day_tt_full(double jd_utc) {
    // UTC == UT1 to ms before 1973 (no leap seconds); inside the table era
    // invert delta_T(TT) with two fixed-point passes.
    double jd_tt = jd_utc + 60.0 / 86400.0;
    for (int i = 0; i < 3; ++i) jd_tt = jd_utc + dut1_delta_t(jd_tt) / 86400.0;
    return jd_tt;
}
inline double julian_day_ut1_full(double jd_tt) {
    return jd_tt - dut1_delta_t(jd_tt) / 86400.0;
}

// ---------------------------------------------------------------------------
// Obliquity, precession, nutation
// ---------------------------------------------------------------------------

// Mean obliquity of the ecliptic (IAU 1980, Meeus eq. 22.2), degrees.
inline double mean_obliquity_deg(double jd_tt) {
    const double t = (jd_tt - 2451545.0) / 36525.0;
    return 23.439291111 - 0.0130042 * t - 1.64e-7 * t * t + 5.04e-7 * t * t * t;
}

// General precession in longitude, arcseconds.
inline double precession_arcsec(double t) {
    return 5029.0966 * t + 1.11113 * t * t;
}

// Δψ, nutation in longitude, degrees (Meeus ch. 22, five leading terms + lunar M).
inline double nutation_longitude_deg(double jd_tt) {
    const double t = (jd_tt - 2451545.0) / 36525.0;
    const double d = (297.85036 + 445267.111480 * t - 0.0019142 * t * t +
                      t * t * t / 189474.0) * kDeg2Rad;
    const double m = (357.52772 + 35999.050340 * t - 0.0001603 * t * t -
                      t * t * t / 300000.0) * kDeg2Rad;
    const double mp = (134.96298 + 477198.867398 * t + 0.0086972 * t * t +
                       t * t * t / 56250.0) * kDeg2Rad;
    const double f = (93.27191 + 483202.017538 * t - 0.0036825 * t * t +
                      t * t * t / 327270.0) * kDeg2Rad;
    const double om = (125.04452 - 1934.136261 * t + 0.0020708 * t * t +
                       t * t * t / 450000.0) * kDeg2Rad;
    const double dpsi_arcsec =
        -17.20 * std::sin(om)
        - 1.32 * std::sin(2.0 * (f - d + om))
        - 0.23 * std::sin(2.0 * (f + om))
        + 0.21 * std::sin(2.0 * om)
        - 0.20 * std::sin(2.0 * d)
        + 0.14 * std::sin(m);
    return dpsi_arcsec / 3600.0;
}

// ---------------------------------------------------------------------------
// Ayanamsa — Lahiri / Chitrapaksha on the Swiss Ephemeris definition
// ---------------------------------------------------------------------------
// Mean Lahiri value at J2000.0 is 23.8570240°; the Swiss Ephemeris prints
// 23°51'11.4153" = 23.8531709167° there because its value is the *apparent*
// ayanamsa (mean + Δψ of that instant).  The annual rate is the empirical
// 0.0140742°/yr that reproduces the Swiss 1956 anchor to 0.01".
namespace ayanamsa {

inline constexpr double kMeanJ2000 = 23.8570240;
inline constexpr double kRateDegPerYear = 0.0140742;

inline double lahiri_deg(double jd_tt) {
    const double t = (jd_tt - 2451545.0) / 36525.0;
    return kMeanJ2000 + kRateDegPerYear * (t * 100.0) + nutation_longitude_deg(jd_tt);
}

}  // namespace ayanamsa

// ---------------------------------------------------------------------------
// Sidereal time
// ---------------------------------------------------------------------------

// Greenwich Mean Sidereal Time in degrees (IAU 1982).
inline double gmst_deg(double jd_ut1) {
    const double d = jd_ut1 - 2451545.0;
    const double t = d / 36525.0;
    double theta = 280.46061837 + 360.98564736629 * d +
                   0.000387933 * t * t - t * t * t / 38710000.0;
    return norm360(theta);
}

// Greenwich Apparent Sidereal Time in degrees (GMST + equation of the equinoxes).
inline double gast_deg_full(double jd_tt, double jd_ut1);
inline double gast_deg(double jd_tt, double jd_ut1) {
    // Full-precision path lives in nut2000b.hpp (IAU 2000A + complementary
    // terms); this Meeus fallback stays for header-only use without it.
    const double dpsi = nutation_longitude_deg(jd_tt);
    const double eps = mean_obliquity_deg(jd_tt) * kDeg2Rad;
    const double t = (jd_tt - 2451545.0) / 36525.0;
    const double om = (125.04452 - 1934.136261 * t) * kDeg2Rad;
    const double c_terms_arcsec = 0.00264 * std::sin(om) + 0.000063 * std::sin(2.0 * om);
    const double eq_eq = dpsi * std::cos(eps) + c_terms_arcsec / 3600.0;
    return norm360(gmst_deg(jd_ut1) + eq_eq);
}

// ---------------------------------------------------------------------------
// Angles
// ---------------------------------------------------------------------------

inline double ascendant_tropical(double ramc_deg, double lat_deg, double eps_deg) {
    const double r = ramc_deg * kDeg2Rad;
    const double phi = lat_deg * kDeg2Rad;
    const double e = eps_deg * kDeg2Rad;
    const double y = std::cos(r);
    const double x = -(std::sin(r) * std::cos(e) + std::tan(phi) * std::sin(e));
    return norm360(std::atan2(y, x) * kRad2Deg);
}

inline double midheaven_tropical(double ramc_deg, double eps_deg) {
    const double r = ramc_deg * kDeg2Rad;
    const double e = eps_deg * kDeg2Rad;
    return norm360(std::atan2(std::sin(r), std::cos(r) * std::cos(e)) * kRad2Deg);
}

// Mean lunar node, tropical, degrees.
inline double mean_node_tropical(double jd_tt) {
    const double t = (jd_tt - 2451545.0) / 36525.0;
    return norm360(125.0445479 - 1934.1362891 * t + 0.0020754 * t * t +
                   t * t * t / 467441.0);
}

// True lunar node, tropical (Meeus high-order periodic terms).
inline double true_node_tropical(double jd_tt) {
    const double t = (jd_tt - 2451545.0) / 36525.0;
    const double d = (297.85036 + 445267.111480 * t - 0.0019142 * t * t +
                      t * t * t / 189474.0) * kDeg2Rad;
    const double m = (357.52772 + 35999.050340 * t - 0.0001603 * t * t -
                      t * t * t / 300000.0) * kDeg2Rad;
    const double mp = (134.96298 + 477198.867398 * t + 0.0086972 * t * t +
                       t * t * t / 56250.0) * kDeg2Rad;
    const double f = (93.27191 + 483202.017538 * t - 0.0036825 * t * t +
                      t * t * t / 327270.0) * kDeg2Rad;
    const double omega = 125.04455 - 1934.13618 * t + 0.002075 * t * t +
                         t * t * t / 467440.0;
    const double corr =
        -1.4979 * std::sin(2.0 * (d - f))
        - 0.4416 * std::sin(2.0 * d)
        - 0.1498 * std::sin(m)
        + 0.1255 * std::sin(2.0 * (d - mp))
        + 0.0641 * std::sin(2.0 * (d - f + mp))
        - 0.0638 * std::sin(2.0 * f)
        + 0.0469 * std::sin(2.0 * (d + f))
        - 0.0447 * std::sin(2.0 * (d - f - m))
        + 0.0384 * std::sin(2.0 * (d - m))
        + 0.0264 * std::sin(2.0 * (d + m));
    return norm360(omega + corr);
}

}  // namespace vyas
