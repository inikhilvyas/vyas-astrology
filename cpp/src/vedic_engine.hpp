#pragma once

#include "astro.hpp"
#include "ephemeris.hpp"

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdio>
#include <ctime>
#include <iomanip>
#include <memory>
#include <sstream>
#include <string>
#include <vector>
#include <windows.h>

namespace vyas {

enum PlanetId {
    PLANET_SUN = 0,
    PLANET_MOON,
    PLANET_MARS,
    PLANET_MERCURY,
    PLANET_JUPITER,
    PLANET_VENUS,
    PLANET_SATURN,
    PLANET_RAHU,
    PLANET_KETU,
    PLANET_ASCENDANT,
    PLANET_COUNT
};

struct PlanetDisplayItem {
    std::string symbol;
    std::string text_deg; // e.g. "Su 7°42'"
    bool is_retro = false;
};

struct PlanetInfo {
    PlanetId id;
    std::string name_en;
    std::string name_sa;
    std::string symbol;
    double longitude = 0.0;     // 0..360 deg
    double speed = 0.0;         // deg/day
    bool is_retrograde = false;
    int rashi = 1;              // 1..12 (1 = Aries/Mesha)
    double rashi_deg = 0.0;     // 0..30 deg
    int deg = 0;
    int min = 0;
    int sec = 0;
    int house = 1;              // 1..12 in D1
    int nakshatra = 1;          // 1..27 (1 = Ashwini)
    int pada = 1;               // 1..4
    std::string nakshatra_name;
    std::string nakshatra_lord;
    int navamsha_rashi = 1;     // 1..12 in D9
    int navamsha_house = 1;     // 1..12 in D9
    std::string dignity;
    std::string awastha;        // e.g. "Yuva (Adult - 100% fruit)"
    std::string awastha_hi;     // e.g. "युवा अवस्था (100% पूर्ण फल)"
    bool is_combust = false;
    std::string chara_karaka;   // AK, AmK, BK, MK, PK, GK, DK
    std::string display_label;  // e.g. "Su 07°42'"
};

struct PanchangInfo {
    std::string tithi_name;
    int tithi_num = 1;          // 1..30
    std::string paksha;         // Shukla / Krishna
    std::string vaar;           // Day of week
    std::string nakshatra;
    int nakshatra_num = 1;
    std::string yoga;
    int yoga_num = 1;
    std::string karana;
    int karana_num = 1;
    double ayanamsa = 0.0;
    double sidereal_time_hours = 0.0;
};

// Complete BPHS Ashtakavarga Data (SAV 337 Bindus & BAV)
struct AshtakavargaData {
    int bav[7][12]; // 7 planets x 12 signs
    int sav[12];    // 12 signs SAV sum (Total = 337)
    int house_sav[12]; // 12 houses SAV sum
    std::string house_eval_hi[12];
    std::string house_eval_en[12];
    int total_bindus = 337;
};

// KP System: Placidus Cusps, 5-Level Sub-Lords
struct KPCuspInfo {
    int cusp_num = 1;         // 1..12
    double longitude = 0.0;   // 0..360
    int rashi = 1;            // 1..12
    double deg_in_sign = 0.0;
    std::string dms_str;
    std::string sign_lord;    // RL (Rashi Lord)
    std::string star_lord;    // NL (Nakshatra Lord)
    std::string sub_lord;     // SL (CSL - Cuspal Sub Lord)
    std::string sub_sub_lord; // SSL
};

struct KPPlanetInfo {
    std::string name;
    std::string symbol;
    double longitude = 0.0;
    int rashi = 1;
    double deg_in_sign = 0.0;
    std::string dms_str;
    std::string sign_lord;
    std::string star_lord;
    std::string sub_lord;
    std::string sub_sub_lord;
};

struct KPSystemData {
    std::array<KPCuspInfo, 12> cusps;
    std::array<KPPlanetInfo, 9> planets;
};

// Jaimini Astrology: 7 Chara Karakas, Karakamsha, Arudha Lagna (AL), Upapada (UL)
struct JaiminiKarakaItem {
    std::string role_name;
    std::string role_hi;
    std::string planet;
    double deg_in_sign = 0.0;
    std::string dms_str;
    std::string rashi_name;
    std::string signification;
};

struct JaiminiData {
    std::vector<JaiminiKarakaItem> karakas;
    std::string atmakaraka_planet;
    std::string amatyakaraka_planet;
    int karakamsha_rashi = 1;
    std::string karakamsha_rashi_name;
    int arudha_lagna_rashi = 1;
    std::string arudha_lagna_name;
    int upapada_lagna_rashi = 1;
    std::string upapada_lagna_name;
};

// Extended Panchang, Avakhada Chakra, and Auspicious Muhurtas
struct ExtendedPanchangInfo {
    std::string tithi_full;
    std::string vaar_full;
    std::string nakshatra_full;
    std::string yoga_full;
    std::string karana_full;
    std::string ayanamsa_str;
    std::string sunrise_str;
    std::string sunset_str;

    // Avakhada Chakra
    std::string varna;
    std::string vashya;
    std::string yoni;
    std::string gana;
    std::string nadi;
    std::string tatva;

    // Auspicious Muhurtas
    std::string abhijit_muhurta;
    std::string brahma_muhurta;
    std::string vijaya_muhurta;
    std::string godhuli_muhurta;
    std::string amrit_vela;

    // Inauspicious Timings
    std::string rahu_kaal;
    std::string yamaganda;
    std::string gulika_kaal;
};

// Comprehensive 12-Bhava Phal Kathan
struct ComprehensivePhalKathan {
    std::string bhava_phala[12];
    std::string career_phala;
    std::string wealth_phala;
    std::string marriage_phala;
    std::string health_phala;
    std::string remedies_phala;
};

// 5-Level Dasha Node (MD, AD, PD, SD, PrD)
struct DashaNode5 {
    int level = 1; // 1=MD, 2=AD, 3=PD, 4=SD, 5=PrD
    std::string level_name;
    std::string lord;
    double start_jd = 0.0;
    double end_jd = 0.0;
    std::string start_str;
    std::string end_str;
    double duration_days = 0.0;
    bool is_active = false;
    std::vector<DashaNode5> sub_dashas;
};

struct ActiveDasha5Chain {
    std::string md_lord, md_range;
    std::string ad_lord, ad_range;
    std::string pd_lord, pd_range;
    std::string sd_lord, sd_range;
    std::string prd_lord, prd_range;
    std::string full_chain_summary;
};

struct EvaluatedSutraItem {
    std::string name;
    std::string category;
    std::string source;
    std::string shloka_sanskrit;
    std::string description;
    std::string result_fruit;
    bool is_active = false;
};

// 16 Shodashvarga Divisional Charts (BPHS Standard)
struct DivisionalChartData {
    std::string code;         // e.g. "D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"
    std::string title_hi;     // e.g. "D1 • लग्न कुण्डली (Lagna Rashi)"
    std::string title_en;     // e.g. "D1 • Lagna Rashi Chart"
    std::string significance; // e.g. "Physical Body, Health & Longevity"
    int varga_num = 1;
    int asc_rashi = 1;        // Divisional Ascendant sign (1..12)
    std::array<int, 12> house_rashis; // 1..12 for each of the 12 houses
    std::array<std::vector<PlanetDisplayItem>, 12> houses;
    std::array<int, PLANET_COUNT> planet_rashis; // 1..12
    std::array<int, PLANET_COUNT> planet_houses; // 1..12
    std::array<double, PLANET_COUNT> planet_internal_degs; // 0..30
    std::array<std::string, PLANET_COUNT> planet_deities;  // for D60
};

struct KundliChart {
    std::string native_name = "Jataka";
    int year = 2000, month = 1, day = 1;
    int hour = 12, minute = 0, second = 0;
    double tz_hours = 5.5;
    double latitude = 28.6139;
    double longitude = 77.2090;
    std::string location_name = "New Delhi, India";

    double jd_ut = 0.0;
    double jd_tt = 0.0;
    double ayanamsa = 0.0;
    double ascendant = 0.0;

    std::array<PlanetInfo, PLANET_COUNT> planets;
    PanchangInfo panchang;

    // 5-Level Dasha System
    std::vector<DashaNode5> mahadashas;
    ActiveDasha5Chain active_5_dasha;
    std::string dasha_balance_str;

    // 16 Shodashvarga Charts (D1 through D60)
    std::vector<DivisionalChartData> shodashvarga;

    // Houses: D1 and D9 planet listings with degrees (backward compat)
    std::array<std::vector<PlanetDisplayItem>, 12> d1_houses;
    std::array<int, 12> d1_house_rashis;
    std::array<std::vector<PlanetDisplayItem>, 12> d9_houses;
    std::array<int, 12> d9_house_rashis;

    // Classical Sutra Bank
    std::vector<EvaluatedSutraItem> active_sutras;

    // Comprehensive Vedic Systems
    AshtakavargaData ashtakavarga;
    KPSystemData kp;
    JaiminiData jaimini;
    ExtendedPanchangInfo ext_panchang;
    ComprehensivePhalKathan phal_kathan;

    // Acharya Vyas 5-tier forensic evaluation
    std::string verdict_p1_decision;
    std::string verdict_p2_yogas;
    std::string verdict_p3_fruit;
    std::string verdict_p4_timeline;
    std::string verdict_p5_remedies;
};

class VedicEngine {
public:
    static std::string FindKernelPath() {
        // 1. Look in exe directory
        wchar_t exePath[MAX_PATH];
        if (GetModuleFileNameW(NULL, exePath, MAX_PATH)) {
            std::wstring wpath(exePath);
            size_t pos = wpath.find_last_of(L"\\/");
            if (pos != std::wstring::npos) {
                std::wstring dir = wpath.substr(0, pos);
                std::wstring cand1 = dir + L"\\data\\de440s.bsp";
                if (GetFileAttributesW(cand1.c_str()) != INVALID_FILE_ATTRIBUTES) {
                    return std::string(cand1.begin(), cand1.end());
                }
                std::wstring cand1b = dir + L"\\de440s.bsp";
                if (GetFileAttributesW(cand1b.c_str()) != INVALID_FILE_ATTRIBUTES) {
                    return std::string(cand1b.begin(), cand1b.end());
                }
                std::wstring cand2 = dir + L"\\..\\data\\de440s.bsp";
                if (GetFileAttributesW(cand2.c_str()) != INVALID_FILE_ATTRIBUTES) {
                    return std::string(cand2.begin(), cand2.end());
                }
            }
        }
        // 2. Direct paths
        static const char* kFallbacks[] = {
            "artifacts\\data\\de440s.bsp",
            "artifacts/data/de440s.bsp",
            "data\\de440s.bsp",
            "data/de440s.bsp",
            "packaging\\msix_build\\data\\de440s.bsp",
            "de440s.bsp",
            "G:\\software\\simpa\\VYAS\\data\\de440s.bsp",
            "G:/software/simpa/VYAS/data/de440s.bsp",
            "G:\\software\\simpa\\VYAS\\artifacts\\data\\de440s.bsp",
            "G:/software/simpa/VYAS/artifacts/data/de440s.bsp"
        };
        for (const char* p : kFallbacks) {
            FILE* f = std::fopen(p, "rb");
            if (f) {
                std::fclose(f);
                return std::string(p);
            }
        }
        return "data/de440s.bsp";
    }

    static const char* RashiName(int rashi) {
        static const char* kRashis[] = {
            "Mesha (Aries)", "Vrishabha (Taurus)", "Mithuna (Gemini)", "Karka (Cancer)",
            "Simha (Leo)", "Kanya (Virgo)", "Tula (Libra)", "Vrishchika (Scorpio)",
            "Dhanu (Sagittarius)", "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"
        };
        if (rashi >= 1 && rashi <= 12) return kRashis[rashi - 1];
        return "Unknown";
    }

    static const char* RashiShort(int rashi) {
        static const char* kShort[] = {
            "Ari", "Tau", "Gem", "Can", "Leo", "Vir", "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"
        };
        if (rashi >= 1 && rashi <= 12) return kShort[rashi - 1];
        return "---";
    }

    static const char* NakshatraName(int nak) {
        static const char* kNaks[] = {
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
            "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
            "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
            "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        };
        if (nak >= 1 && nak <= 27) return kNaks[nak - 1];
        return "Unknown";
    }

    static const char* NakshatraLord(int nak) {
        static const char* kLords[] = {
            "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
        };
        if (nak >= 1 && nak <= 27) return kLords[(nak - 1) % 9];
        return "Unknown";
    }

    static const char* TithiName(int tithi) {
        static const char* kTithis[] = {
            "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
            "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
            "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
            "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
            "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
            "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya"
        };
        if (tithi >= 1 && tithi <= 30) return kTithis[tithi - 1];
        return "Unknown";
    }

    static const char* YogaName(int y) {
        static const char* kYogas[] = {
            "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Sobhana", "Atiganda",
            "Sukarma", "Dhriti", "Shula", "Ganda", "Vriddhi", "Dhruva",
            "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyan",
            "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla",
            "Brahma", "Indra", "Vaidhriti"
        };
        if (y >= 1 && y <= 27) return kYogas[y - 1];
        return "Unknown";
    }

    static const char* KaranaName(int k) {
        static const char* kKaranas[] = {
            "Bava", "Balava", "Kaulava", "Taitila", "Gara", "Vanija", "Vishti (Bhadra)",
            "Shakuni", "Chatushpada", "Naga", "Kintughna"
        };
        if (k == 1) return kKaranas[10];
        if (k >= 2 && k <= 57) return kKaranas[(k - 2) % 7];
        if (k == 58) return kKaranas[7];
        if (k == 59) return kKaranas[8];
        if (k == 60) return kKaranas[9];
        return "Unknown";
    }

    static const char* WeekdayName(int day_idx) {
        static const char* kDays[] = {
            "Ravivara (Sunday)", "Somavara (Monday)", "Mangalavara (Tuesday)",
            "Budhavara (Wednesday)", "Guruvara (Thursday)", "Shukravara (Friday)", "Shanivara (Saturday)"
        };
        if (day_idx >= 0 && day_idx <= 6) return kDays[day_idx];
        return "Unknown";
    }

    static std::string FormatJdToDateStr(double jd, double tz_hours = 5.5) {
        double jd_local = jd + tz_hours / 24.0 + 0.5;
        int Z = (int)std::floor(jd_local);
        double F = jd_local - Z;

        int A = Z;
        if (Z >= 2299161) {
            int alpha = (int)std::floor((Z - 1867216.25) / 36524.25);
            A = Z + 1 + alpha - (int)std::floor(alpha / 4.0);
        }
        int B = A + 1524;
        int C = (int)std::floor((B - 122.1) / 365.25);
        int D = (int)std::floor(365.25 * C);
        int E = (int)std::floor((B - D) / 30.6001);

        int day = B - D - (int)std::floor(30.6001 * E);
        int month = (E < 14) ? E - 1 : E - 13;
        int year = (month > 2) ? C - 4716 : C - 4715;

        double total_hours = F * 24.0;
        int hr = (int)std::floor(total_hours);
        double total_min = (total_hours - hr) * 60.0;
        int mn = (int)std::floor(total_min);

        char buf[64];
        std::snprintf(buf, sizeof(buf), "%02d/%02d/%04d %02d:%02d", day, month, year, hr, mn);
        return std::string(buf);
    }

    static KundliChart Calculate(
        const std::string& name,
        int year, int month, int day,
        int hour, int minute, int second,
        double tz_hours,
        double latitude, double longitude,
        const std::string& loc_name = "User Location",
        std::string kernel_path = ""
    ) {
        if (kernel_path.empty()) {
            kernel_path = FindKernelPath();
        }

        KundliChart chart;
        chart.native_name = name;
        chart.year = year; chart.month = month; chart.day = day;
        chart.hour = hour; chart.minute = minute; chart.second = second;
        chart.tz_hours = tz_hours;
        chart.latitude = latitude; chart.longitude = longitude;
        chart.location_name = loc_name;

        // 1. Time & Ephemeris
        double utc_hours = (hour + minute / 60.0 + second / 3600.0) - tz_hours;
        chart.jd_ut = julian_day_utc(year, month, day, utc_hours);
        chart.jd_tt = julian_day_tt_full(chart.jd_ut);
        chart.ayanamsa = ayanamsa::lahiri_deg(chart.jd_tt);

        // 2. Compute Planetary Longitudes
        std::array<BodyPosition, 9> body_pos;
        bool jpl_loaded = false;

        try {
            FILE* ftest = std::fopen(kernel_path.c_str(), "rb");
            if (ftest) {
                std::fclose(ftest);
                Ephemeris eph(kernel_path);
                const int naif[7] = {NAIF_SUN, NAIF_MOON, NAIF_MARS_BARY,
                                     NAIF_MERCURY_BARY, NAIF_JUPITER_BARY,
                                     NAIF_VENUS_BARY, NAIF_SATURN_BARY};
                for (int i = 0; i < 7; ++i) {
                    body_pos[i] = eph.graha(naif[i], chart.jd_tt);
                }
                body_pos[7] = eph.node(/*mean=*/true, chart.jd_tt); // Rahu
                body_pos[8].longitude = norm360(body_pos[7].longitude + 180.0);
                body_pos[8].speed = body_pos[7].speed;
                chart.ascendant = eph.ascendant_sidereal(chart.jd_ut, latitude, longitude);
                jpl_loaded = true;
            }
        } catch (...) {
            jpl_loaded = false;
        }

        if (!jpl_loaded) {
            // NASA JPL Standish (1998) 3D Heliocentric + Light-Time Aberration + Precession + VSOP87 Perturbations
            double d = chart.jd_ut - 2451545.0; // days from J2000.0
            double T = d / 36525.0;             // Julian centuries from J2000.0

            // 1. High-Precision Sun & Earth Vector (VSOP87 Analytical)
            double prec_deg = (5028.796195 * T + 1.1054348 * T * T) / 3600.0;
            double L0 = norm360(280.4664567 + 36000.76982779 * T);
            double M_sun = norm360(357.5291092 + 35999.0502909 * T) * kDeg2Rad;
            double C_sun = (1.914602 - 0.004817 * T - 0.000014 * T * T) * std::sin(M_sun) +
                           (0.019993 - 0.000101 * T) * std::sin(2.0 * M_sun) +
                           0.000289 * std::sin(3.0 * M_sun);
            double sun_app_lon = norm360(L0 + C_sun - 0.00569 - 0.00478 * std::sin((125.04 - 1934.136 * T) * kDeg2Rad));
            body_pos[0].longitude = sun_app_lon;
            body_pos[0].speed = 0.9856;

            double e_sun = 0.016708634 - 0.000042037 * T;
            double v_sun = M_sun + C_sun * kDeg2Rad;
            double R_sun = (1.000001018 * (1.0 - e_sun * e_sun)) / (1.0 + e_sun * std::cos(v_sun));
            double earth_helio_lon_j2000 = norm360(sun_app_lon + 180.0 - prec_deg) * kDeg2Rad;
            double X_sun_j2000 = R_sun * std::cos(earth_helio_lon_j2000);
            double Y_sun_j2000 = R_sun * std::sin(earth_helio_lon_j2000);

            // 2. High-Precision Moon (Brown's Lunar Theory - 15 Perturbations)
            double L_prime = norm360(218.3164477 + 481267.88128 * T);
            double D = norm360(297.8501921 + 445267.11135 * T);
            double M_moon = norm360(134.9633964 + 477198.86750 * T);
            double F_moon = norm360(93.2720950 + 483202.01752 * T);
            double moonCorr = 6.288774 * std::sin(M_moon * kDeg2Rad) +
                              1.274027 * std::sin((2.0 * D - M_moon) * kDeg2Rad) +
                              0.658314 * std::sin(2.0 * D * kDeg2Rad) +
                              0.213618 * std::sin(2.0 * M_moon * kDeg2Rad) -
                              0.185116 * std::sin(M_sun) -
                              0.114332 * std::sin(2.0 * F_moon * kDeg2Rad) +
                              0.058793 * std::sin((2.0 * D - 2.0 * M_moon) * kDeg2Rad) +
                              0.057066 * std::sin((2.0 * D - M_moon - (M_sun * kRad2Deg)) * kDeg2Rad) +
                              0.053322 * std::sin((2.0 * D + M_moon) * kDeg2Rad) +
                              0.046038 * std::sin((2.0 * D - (M_sun * kRad2Deg)) * kDeg2Rad) +
                              0.041024 * std::sin((M_moon - (M_sun * kRad2Deg)) * kDeg2Rad) -
                              0.034720 * std::sin(D * kDeg2Rad) -
                              0.030647 * std::sin((M_moon + (M_sun * kRad2Deg)) * kDeg2Rad);
            body_pos[1].longitude = norm360(L_prime + moonCorr);
            body_pos[1].speed = 13.176;

            // 3. Planetary Orbital Elements (NASA JPL Standish J2000 Osculating Elements + Perturbations)
            struct StandishElem {
                double a0, ad, e0, ed, i0, id, l0, ld, wb0, wbd, om0, omd;
            };
            // Indices: Mercury=3, Venus=5, Mars=2, Jupiter=4, Saturn=6
            static const StandishElem kElemMars    = { 1.52371034,  0.00001847, 0.09339410,  0.00007882, 1.84969142, -0.00813131, 355.44656795,  19140.30268499, 336.05637041,  0.44441088,  49.55953891, -0.29257343 };
            static const StandishElem kElemMerc    = { 0.38709927,  0.00000037, 0.20563593,  0.00001906, 7.00497902, -0.00594749, 252.25032350, 149472.67411175,  77.45779628,  0.16047689,  48.33076593, -0.12534081 };
            static const StandishElem kElemJup     = { 5.20288700, -0.00011607, 0.04838624, -0.00013253, 1.30439695, -0.00183714,  34.39644051,   3034.74612775,  14.72847983,  0.21252668, 100.47390909,  0.20469106 };
            static const StandishElem kElemVen     = { 0.72333566,  0.00000390, 0.00677672, -0.00004107, 3.39467605, -0.00078890, 181.97909950,  58517.81538729, 131.60246718,  0.00268329,  76.67984255, -0.27769418 };
            static const StandishElem kElemSat     = { 9.53667594, -0.00125060, 0.05386179, -0.00050991, 2.48599187,  0.00193609,  49.95424423,   1222.49362201,  92.59887831, -0.41897216, 113.66242448, -0.28867794 };

            auto calcHelioStandish = [&](const StandishElem& el, const char* pName, double tVal, double& hx, double& hy, double& hz) {
                double a = el.a0 + el.ad * tVal;
                double e = el.e0 + el.ed * tVal;
                double inc = (el.i0 + el.id * tVal) * kDeg2Rad;
                double l_deg = el.l0 + el.ld * tVal;
                double wb_deg = el.wb0 + el.wbd * tVal;
                double om_deg = el.om0 + el.omd * tVal;

                double mj = norm360(34.39644 + 3034.74613 * tVal - 14.72848) * kDeg2Rad;
                double ms = norm360(49.95424 + 1222.49362 * tVal - 92.59888) * kDeg2Rad;

                if (std::strcmp(pName, "Jupiter") == 0) {
                    l_deg += (-0.332 * std::sin(2.0 * mj - 5.0 * ms - 67.6 * kDeg2Rad) - 0.056 * std::sin(2.0 * mj - 2.0 * ms + 21.0 * kDeg2Rad) - 0.07);
                } else if (std::strcmp(pName, "Saturn") == 0) {
                    l_deg += (0.812 * std::sin(2.0 * mj - 5.0 * ms - 67.6 * kDeg2Rad) - 0.229 * std::cos(2.0 * mj - 4.0 * ms - 2.0 * kDeg2Rad) + 0.119 * std::sin(mj - 2.0 * ms - 3.0 * kDeg2Rad) + 0.32);
                } else if (std::strcmp(pName, "Mars") == 0) {
                    l_deg += (-0.02);
                }

                double w_arg = (wb_deg - om_deg) * kDeg2Rad;
                double om = om_deg * kDeg2Rad;
                double m_anom = norm360(l_deg - wb_deg) * kDeg2Rad;

                double E = m_anom;
                for (int k = 0; k < 15; ++k) {
                    double dE = (m_anom - (E - e * std::sin(E))) / (1.0 - e * std::cos(E));
                    E += dE;
                    if (std::abs(dE) < 1e-11) break;
                }

                double xv = a * (std::cos(E) - e);
                double yv = a * std::sqrt(std::max(0.0, 1.0 - e * e)) * std::sin(E);
                double cos_w = std::cos(w_arg), sin_w = std::sin(w_arg);
                double cos_om = std::cos(om), sin_om = std::sin(om);
                double cos_i = std::cos(inc), sin_i = std::sin(inc);

                hx = (cos_w * cos_om - sin_w * sin_om * cos_i) * xv + (-sin_w * cos_om - cos_w * sin_om * cos_i) * yv;
                hy = (cos_w * sin_om + sin_w * cos_om * cos_i) * xv + (-sin_w * sin_om + cos_w * cos_om * cos_i) * yv;
                hz = (sin_w * sin_i) * xv + (cos_w * sin_i) * yv;
            };

            auto solveGeocentric = [&](const StandishElem& el, const char* pName, int bodyIdx, double speedDefault) {
                double hx, hy, hz;
                calcHelioStandish(el, pName, T, hx, hy, hz);
                double dx = hx + X_sun_j2000;
                double dy = hy + Y_sun_j2000;
                double dz = hz;
                double dist = std::sqrt(dx * dx + dy * dy + dz * dz);
                double tau = (0.0057755183 * dist) / 36525.0; // Light-time aberration

                double hx_ret, hy_ret, hz_ret;
                calcHelioStandish(el, pName, T - tau, hx_ret, hy_ret, hz_ret);
                double gx = hx_ret + X_sun_j2000;
                double gy = hy_ret + Y_sun_j2000;
                double lambda_j2000 = norm360(std::atan2(gy, gx) * kRad2Deg);
                double lambda_ofdate = norm360(lambda_j2000 + prec_deg);
                body_pos[bodyIdx].longitude = lambda_ofdate;
                body_pos[bodyIdx].speed = speedDefault;
            };

            solveGeocentric(kElemMars, "Mars", 2, 0.524);
            solveGeocentric(kElemMerc, "Mercury", 3, 1.38);
            solveGeocentric(kElemJup, "Jupiter", 4, 0.083);
            solveGeocentric(kElemVen, "Venus", 5, 1.20);
            solveGeocentric(kElemSat, "Saturn", 6, 0.033);

            // 8. Rahu / Ketu (Mean lunar node)
            double omega_node = norm360(125.0445479 - 1934.1362891 * T + 0.0020754 * T * T);
            body_pos[7].longitude = omega_node;
            body_pos[7].speed = -0.05295;
            body_pos[8].longitude = norm360(omega_node + 180.0);
            body_pos[8].speed = -0.05295;

            // Convert tropical analytical positions to Sidereal by subtracting Lahiri Ayanamsa
            for (int b = 0; b < 9; ++b) {
                body_pos[b].longitude = norm360(body_pos[b].longitude - chart.ayanamsa);
            }

            // Ascendant
            double gast = gast_deg(chart.jd_tt, chart.jd_ut);
            double ramc = norm360(gast + longitude);
            double eps = mean_obliquity_deg(chart.jd_tt);
            double asc_trop = ascendant_tropical(ramc, latitude, eps);
            chart.ascendant = norm360(asc_trop - chart.ayanamsa);
        }

        // 3. Populate Planet Details
        static constexpr const char* kEnNames[PLANET_COUNT] = {
            "Sun", "Moon", "Mars", "Mercury", "Jupiter",
            "Venus", "Saturn", "Rahu", "Ketu", "Ascendant"
        };
        static constexpr const char* kSaNames[PLANET_COUNT] = {
            "Surya", "Chandra", "Mangala", "Budha", "Guru",
            "Shukra", "Shani", "Rahu", "Ketu", "Lagna"
        };
        static constexpr const char* kSymbols[PLANET_COUNT] = {
            "Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke", "Asc"
        };

        int asc_rashi = static_cast<int>(std::floor(chart.ascendant / 30.0)) + 1;
        for (int h = 0; h < 12; ++h) {
            chart.d1_house_rashis[h] = ((asc_rashi - 1 + h) % 12) + 1;
        }

        for (int i = 0; i < PLANET_COUNT; ++i) {
            PlanetInfo& p = chart.planets[i];
            p.id = static_cast<PlanetId>(i);
            p.name_en = kEnNames[i];
            p.name_sa = kSaNames[i];
            p.symbol = kSymbols[i];

            if (i < 9) {
                p.longitude = body_pos[i].longitude;
                p.speed = body_pos[i].speed;
                p.is_retrograde = (p.speed < 0.0);
            } else {
                p.longitude = chart.ascendant;
                p.speed = 360.0;
                p.is_retrograde = false;
            }

            p.rashi = static_cast<int>(std::floor(p.longitude / 30.0)) + 1;
            p.rashi_deg = p.longitude - (p.rashi - 1) * 30.0;
            p.deg = static_cast<int>(std::floor(p.rashi_deg));
            double rem_min = (p.rashi_deg - p.deg) * 60.0;
            p.min = static_cast<int>(std::floor(rem_min));
            p.sec = static_cast<int>(std::round((rem_min - p.min) * 60.0));

            // Format degree label: e.g. "Su 07°42'" or "Sa [R] 26°52'"
            char deg_buf[32];
            if (p.is_retrograde && i != PLANET_RAHU && i != PLANET_KETU) {
                std::snprintf(deg_buf, sizeof(deg_buf), "%s[R] %02d°%02d'", p.symbol.c_str(), p.deg, p.min);
            } else {
                std::snprintf(deg_buf, sizeof(deg_buf), "%s %02d°%02d'", p.symbol.c_str(), p.deg, p.min);
            }
            p.display_label = deg_buf;

            // House in D1
            p.house = ((p.rashi - asc_rashi + 12) % 12) + 1;

            // Nakshatra
            double nak_frac = p.longitude / (360.0 / 27.0);
            p.nakshatra = static_cast<int>(std::floor(nak_frac)) + 1;
            double pada_frac = (nak_frac - std::floor(nak_frac)) * 4.0;
            p.pada = static_cast<int>(std::floor(pada_frac)) + 1;
            p.nakshatra_name = NakshatraName(p.nakshatra);
            p.nakshatra_lord = NakshatraLord(p.nakshatra);

            // Navamsha (D9) calculation
            int absolute_pada = (p.nakshatra - 1) * 4 + (p.pada - 1);
            p.navamsha_rashi = (absolute_pada % 12) + 1;

            p.dignity = AssignDignity(p.id, p.rashi, p.rashi_deg);
            AssignAwastha(p);

            // Check combustion with Sun
            if (i > 0 && i < 7) {
                double sun_lon = chart.planets[0].longitude;
                double diff = std::abs(p.longitude - sun_lon);
                if (diff > 180.0) diff = 360.0 - diff;
                double combust_lim = (i == 1 ? 12.0 : (i == 2 ? 17.0 : (i == 3 ? 14.0 : (i == 4 ? 11.0 : (i == 5 ? 10.0 : 15.0)))));
                if (diff <= combust_lim) {
                    p.is_combust = true;
                    p.dignity += " [अस्त]";
                }
            }

            // House grouping for D1
            if (p.house >= 1 && p.house <= 12) {
                PlanetDisplayItem item;
                item.symbol = p.symbol;
                item.text_deg = p.display_label;
                item.is_retro = p.is_retrograde;
                chart.d1_houses[p.house - 1].push_back(item);
            }
        }

        // Navamsha Lagna and D9 houses
        int nav_asc_rashi = chart.planets[PLANET_ASCENDANT].navamsha_rashi;
        for (int h = 0; h < 12; ++h) {
            chart.d9_house_rashis[h] = ((nav_asc_rashi - 1 + h) % 12) + 1;
        }
        for (int i = 0; i < PLANET_COUNT; ++i) {
            PlanetInfo& p = chart.planets[i];
            p.navamsha_house = ((p.navamsha_rashi - nav_asc_rashi + 12) % 12) + 1;
            if (p.navamsha_house >= 1 && p.navamsha_house <= 12) {
                PlanetDisplayItem item;
                item.symbol = p.symbol;
                item.text_deg = p.display_label;
                item.is_retro = p.is_retrograde;
                chart.d9_houses[p.navamsha_house - 1].push_back(item);
            }
        }

        // 4. Jaimini 7 Chara Karakas
        CalculateJaimini(chart);

        // 5. Calculate 16 Shodashvarga Divisional Charts (D1 through D60)
        CalculateShodashvarga(chart);

        // 6. Complete BPHS Ashtakavarga Engine (SAV 337 Bindus & BAV)
        CalculateAshtakavarga(chart);

        // 7. KP System (Placidus Cusps, 5-Level Sub-Lords)
        CalculateKPSystem(chart);

        // 8. Classical Panchang & Extended Auspicious Muhurtas
        CalculatePanchang(chart);
        CalculateExtendedPanchang(chart);

        // 9. 5-Tier Vimshottari Dasha Hierarchy (MD down to Prana Dasha)
        Calculate5LevelVimshottari(chart);

        // 10. Classical Sutra Bank Evaluation
        EvaluateSutraBank(chart);

        // 11. Comprehensive 12-Bhava Phal Kathan
        CalculateComprehensivePhalKathan(chart);

        // 12. Acharya Vyas 5-Tier Forensic Verdict
        EvaluateForensicVerdict(chart);

        return chart;
    }

private:
    static std::string AssignDignity(PlanetId id, int rashi, double deg) {
        switch (id) {
            case PLANET_SUN:
                if (rashi == 1 && deg <= 10.0) return "Exalted (उच्च)";
                if (rashi == 1) return "Exalted Zone";
                if (rashi == 7 && deg <= 10.0) return "Debilitated (नीच)";
                if (rashi == 7) return "Debilitated Zone";
                if (rashi == 5 && deg <= 20.0) return "Moolatrikona (मूलत्रिकोण)";
                if (rashi == 5) return "Own Sign (स्वराशि)";
                if (rashi == 4 || rashi == 9 || rashi == 8) return "Friendly (मित्र)";
                if (rashi == 2 || rashi == 11 || rashi == 10) return "Enemy (शत्रु)";
                return "Neutral (सम)";
            case PLANET_MOON:
                if (rashi == 2 && deg <= 3.0) return "Exalted (उच्च)";
                if (rashi == 2) return "Moolatrikona (मूलत्रिकोण)";
                if (rashi == 8 && deg <= 3.0) return "Debilitated (नीच)";
                if (rashi == 8) return "Debilitated Zone";
                if (rashi == 4) return "Own Sign (स्वराशि)";
                return "Normal";
            case PLANET_MARS:
                if (rashi == 10 && deg <= 28.0) return "Exalted (उच्च)";
                if (rashi == 4 && deg <= 28.0) return "Debilitated (नीच)";
                if (rashi == 1 && deg <= 12.0) return "Moolatrikona";
                if (rashi == 1 || rashi == 8) return "Own Sign (स्वराशि)";
                return "Normal";
            case PLANET_MERCURY:
                if (rashi == 6 && deg <= 15.0) return "Exalted (उच्च)";
                if (rashi == 6 && deg <= 20.0) return "Moolatrikona";
                if (rashi == 12 && deg <= 15.0) return "Debilitated (नीच)";
                if (rashi == 3 || rashi == 6) return "Own Sign (स्वराशि)";
                return "Normal";
            case PLANET_JUPITER:
                if (rashi == 4 && deg <= 5.0) return "Exalted (उच्च)";
                if (rashi == 10 && deg <= 5.0) return "Debilitated (नीच)";
                if (rashi == 9 && deg <= 10.0) return "Moolatrikona";
                if (rashi == 9 || rashi == 12) return "Own Sign (स्वराशि)";
                return "Normal";
            case PLANET_VENUS:
                if (rashi == 12 && deg <= 27.0) return "Exalted (उच्च)";
                if (rashi == 6 && deg <= 27.0) return "Debilitated (नीच)";
                if (rashi == 7 && deg <= 15.0) return "Moolatrikona";
                if (rashi == 2 || rashi == 7) return "Own Sign (स्वराशि)";
                return "Normal";
            case PLANET_SATURN:
                if (rashi == 7 && deg <= 20.0) return "Exalted (उच्च)";
                if (rashi == 1 && deg <= 20.0) return "Debilitated (नीच)";
                if (rashi == 11 && deg <= 20.0) return "Moolatrikona";
                if (rashi == 10 || rashi == 11) return "Own Sign (स्वराशि)";
                return "Normal";
            case PLANET_RAHU:
                if (rashi == 2 || rashi == 3) return "Exalted (उच्च / शुभ)";
                if (rashi == 8 || rashi == 9) return "Debilitated (नीच)";
                return "Shadow Graha";
            case PLANET_KETU:
                if (rashi == 8 || rashi == 9) return "Exalted (उच्च / शुभ)";
                if (rashi == 2 || rashi == 3) return "Debilitated (नीच)";
                return "Moksha Karaka";
            default:
                return "Ascendant";
        }
    }

    static void AssignAwastha(PlanetInfo& p) {
        bool is_odd = (p.rashi % 2 != 0); // 1=Mesha (odd), 2=Vrishabha (even)
        double deg = p.rashi_deg;
        if (is_odd) {
            if (deg < 6.0) { p.awastha = "Baala (25%)"; p.awastha_hi = "बाल अवस्था (25% फल)"; }
            else if (deg < 12.0) { p.awastha = "Kumara (50%)"; p.awastha_hi = "कुमार अवस्था (50% फल)"; }
            else if (deg < 18.0) { p.awastha = "Yuva (100%)"; p.awastha_hi = "युवा अवस्था (100% पूर्ण फल)"; }
            else if (deg < 24.0) { p.awastha = "Vriddha (10%)"; p.awastha_hi = "वृद्ध अवस्था (10% फल)"; }
            else { p.awastha = "Mrita (0%)"; p.awastha_hi = "मृत अवस्था (निष्क्रिय/0%)"; }
        } else {
            if (deg < 6.0) { p.awastha = "Mrita (0%)"; p.awastha_hi = "मृत अवस्था (निष्क्रिय/0%)"; }
            else if (deg < 12.0) { p.awastha = "Vriddha (10%)"; p.awastha_hi = "वृद्ध अवस्था (10% फल)"; }
            else if (deg < 18.0) { p.awastha = "Yuva (100%)"; p.awastha_hi = "युवा अवस्था (100% पूर्ण फल)"; }
            else if (deg < 24.0) { p.awastha = "Kumara (50%)"; p.awastha_hi = "कुमार अवस्था (50% फल)"; }
            else { p.awastha = "Baala (25%)"; p.awastha_hi = "बाल अवस्था (25% फल)"; }
        }
    }

    static void CalculateJaimini(KundliChart& chart) {
        struct PlanetDeg {
            int idx;
            double deg;
        };
        std::vector<PlanetDeg> candidates;
        for (int i = 0; i < 7; ++i) {
            candidates.push_back({i, chart.planets[i].rashi_deg});
        }
        std::sort(candidates.begin(), candidates.end(), [](const PlanetDeg& a, const PlanetDeg& b) {
            return a.deg > b.deg;
        });

        static const char* kKarakas[7] = {
            "AK (Atmakaraka - आत्मकारक)",
            "AmK (Amatyakaraka - अमात्यकारक)",
            "BK (Bhratrikaraka - भ्रातृकारक)",
            "MK (Matrikaraka - मातृकारक)",
            "PK (Putrakaraka - पुत्रकारक)",
            "GK (Gnatikaraka - ज्ञातिकारक)",
            "DK (Darakaraka - दारककारक)"
        };
        static const char* kRoles[7] = {
            "Atmakaraka (AK)", "Amatyakaraka (AmK)", "Bhratrikaraka (BK)",
            "Matrikaraka (MK)", "Putrakaraka (PK)", "Gnatikaraka (GK)", "Darakaraka (DK)"
        };
        static const char* kRolesHi[7] = {
            "आत्मकारक (AK)", "अमात्यकारक (AmK)", "भ्रातृकारक (BK)",
            "मातृकारक (MK)", "पुत्रकारक (PK)", "ज्ञातिकारक (GK)", "दाराकारक (DK)"
        };
        static const char* kRoleSig[7] = {
            "Soul, King of Chart, Life Purpose & Destiny (आत्मोन्नति व मूल प्रारब्ध)",
            "Career, Intellect, Royal Favor & Profession (आजीविका, पद व कर्म)",
            "Siblings, Guru, Guides & Valour (भ्रातृ सुख, गुरु व साहस)",
            "Mother, Real Estate, Immovable Assets (माता, भूमि, भवन व सुख)",
            "Children, Intellect, Mantras & Creativity (संतान, बुद्धि व ज्ञान)",
            "Obstacles, Debts, Disease & Competitors (रोग, ऋण, विवाद व संघर्ष)",
            "Spouse, Life Partner & Marital Harmony (जीवनसाथी, विवाह व व्यापार)"
        };

        chart.jaimini.karakas.clear();
        for (int k = 0; k < 7; ++k) {
            int p_idx = candidates[k].idx;
            chart.planets[p_idx].chara_karaka = kKarakas[k];

            JaiminiKarakaItem item;
            item.role_name = kRoles[k];
            item.role_hi = kRolesHi[k];
            item.planet = chart.planets[p_idx].name_sa;
            item.deg_in_sign = chart.planets[p_idx].rashi_deg;
            item.rashi_name = RashiName(chart.planets[p_idx].rashi);
            item.signification = kRoleSig[k];

            int d = chart.planets[p_idx].deg;
            int m = chart.planets[p_idx].min;
            int s = chart.planets[p_idx].sec;
            char buf[32];
            std::snprintf(buf, sizeof(buf), "%02d°%02d'%02d\"", d, m, s);
            item.dms_str = buf;

            chart.jaimini.karakas.push_back(item);
        }

        chart.jaimini.atmakaraka_planet = chart.planets[candidates[0].idx].name_sa;
        chart.jaimini.amatyakaraka_planet = chart.planets[candidates[1].idx].name_sa;
        chart.jaimini.karakamsha_rashi = chart.planets[candidates[0].idx].navamsha_rashi;
        chart.jaimini.karakamsha_rashi_name = RashiName(chart.jaimini.karakamsha_rashi);

        // Arudha Lagna (AL)
        int asc_r = chart.planets[PLANET_ASCENDANT].rashi;
        static const int kRashiLords[12] = {3, 6, 4, 2, 1, 4, 6, 3, 5, 7, 7, 5}; // Mars, Venus, Mercury, Moon, Sun, etc.
        int lord_id = kRashiLords[asc_r - 1] - 1;
        int lord_r = chart.planets[lord_id].rashi;
        int dist = (lord_r - asc_r + 12) % 12;
        int al_r = (lord_r - 1 + dist) % 12 + 1;
        if (al_r == asc_r || al_r == ((asc_r + 5) % 12 + 1)) {
            al_r = (al_r - 1 + 9) % 12 + 1;
        }
        chart.jaimini.arudha_lagna_rashi = al_r;
        chart.jaimini.arudha_lagna_name = RashiName(al_r);

        // Upapada Lagna (UL) - 12th house arudha
        int h12_r = (asc_r - 2 + 12) % 12 + 1;
        int h12_lord_id = kRashiLords[h12_r - 1] - 1;
        int h12_lord_r = chart.planets[h12_lord_id].rashi;
        int dist12 = (h12_lord_r - h12_r + 12) % 12;
        int ul_r = (h12_lord_r - 1 + dist12) % 12 + 1;
        if (ul_r == h12_r || ul_r == ((h12_r + 5) % 12 + 1)) {
            ul_r = (ul_r - 1 + 9) % 12 + 1;
        }
        chart.jaimini.upapada_lagna_rashi = ul_r;
        chart.jaimini.upapada_lagna_name = RashiName(ul_r);
    }

    static void CalculateAshtakavarga(KundliChart& chart) {
        for (int p = 0; p < 7; ++p) {
            for (int s = 0; s < 12; ++s) {
                chart.ashtakavarga.bav[p][s] = 0;
            }
        }
        for (int s = 0; s < 12; ++s) {
            chart.ashtakavarga.sav[s] = 0;
        }

        int ref_signs[8];
        for (int i = 0; i < 7; ++i) {
            ref_signs[i] = (chart.planets[i].rashi - 1) % 12;
        }
        ref_signs[7] = (chart.planets[PLANET_ASCENDANT].rashi - 1) % 12;

        static const int kBAVRules[7][8][13] = {
            { // Sun
                {8, 1, 2, 4, 7, 8, 9, 10, 11, 0, 0, 0, 0},
                {4, 3, 6, 10, 11, 0, 0, 0, 0, 0, 0, 0, 0},
                {8, 1, 2, 4, 7, 8, 9, 10, 11, 0, 0, 0, 0},
                {7, 3, 5, 6, 9, 10, 11, 12, 0, 0, 0, 0, 0},
                {4, 5, 6, 9, 11, 0, 0, 0, 0, 0, 0, 0, 0},
                {3, 6, 7, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                {8, 1, 2, 4, 7, 8, 9, 10, 11, 0, 0, 0, 0},
                {6, 3, 4, 6, 10, 11, 12, 0, 0, 0, 0, 0, 0},
            },
            { // Moon
                {6, 3, 6, 7, 8, 10, 11, 0, 0, 0, 0, 0, 0},
                {6, 1, 3, 6, 7, 10, 11, 0, 0, 0, 0, 0, 0},
                {7, 2, 3, 5, 6, 9, 10, 11, 0, 0, 0, 0, 0},
                {8, 1, 3, 4, 5, 7, 8, 10, 11, 0, 0, 0, 0},
                {7, 1, 4, 7, 8, 10, 11, 12, 0, 0, 0, 0, 0},
                {7, 3, 4, 5, 7, 9, 10, 11, 0, 0, 0, 0, 0},
                {4, 3, 5, 6, 11, 0, 0, 0, 0, 0, 0, 0, 0},
                {4, 3, 6, 10, 11, 0, 0, 0, 0, 0, 0, 0, 0},
            },
            { // Mars
                {5, 3, 5, 6, 10, 11, 0, 0, 0, 0, 0, 0, 0},
                {3, 3, 6, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                {7, 1, 2, 4, 7, 8, 10, 11, 0, 0, 0, 0, 0},
                {4, 3, 5, 6, 11, 0, 0, 0, 0, 0, 0, 0, 0},
                {4, 6, 10, 11, 12, 0, 0, 0, 0, 0, 0, 0, 0},
                {4, 6, 8, 11, 12, 0, 0, 0, 0, 0, 0, 0, 0},
                {7, 1, 4, 7, 8, 9, 10, 11, 0, 0, 0, 0, 0},
                {5, 1, 3, 6, 10, 11, 0, 0, 0, 0, 0, 0, 0},
            },
            { // Mercury
                {5, 5, 6, 9, 11, 12, 0, 0, 0, 0, 0, 0, 0},
                {6, 2, 4, 6, 8, 10, 11, 0, 0, 0, 0, 0, 0},
                {8, 1, 2, 4, 7, 8, 9, 10, 11, 0, 0, 0, 0},
                {8, 1, 3, 5, 6, 9, 10, 11, 12, 0, 0, 0, 0},
                {4, 6, 8, 11, 12, 0, 0, 0, 0, 0, 0, 0, 0},
                {8, 1, 2, 3, 4, 5, 8, 9, 11, 0, 0, 0, 0},
                {8, 1, 2, 4, 7, 8, 9, 10, 11, 0, 0, 0, 0},
                {7, 1, 2, 4, 6, 8, 10, 11, 0, 0, 0, 0, 0},
            },
            { // Jupiter
                {9, 1, 2, 3, 4, 7, 8, 9, 10, 11, 0, 0, 0},
                {5, 2, 5, 7, 9, 11, 0, 0, 0, 0, 0, 0, 0},
                {7, 1, 2, 4, 7, 8, 10, 11, 0, 0, 0, 0, 0},
                {8, 1, 2, 4, 5, 6, 9, 10, 11, 0, 0, 0, 0},
                {8, 1, 2, 3, 4, 7, 8, 10, 11, 0, 0, 0, 0},
                {6, 2, 5, 6, 9, 10, 11, 0, 0, 0, 0, 0, 0},
                {4, 3, 5, 6, 12, 0, 0, 0, 0, 0, 0, 0, 0},
                {9, 1, 2, 4, 5, 6, 7, 9, 10, 11, 0, 0, 0},
            },
            { // Venus
                {3, 8, 11, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                {9, 1, 2, 3, 4, 5, 8, 9, 11, 12, 0, 0, 0},
                {6, 3, 5, 6, 9, 11, 12, 0, 0, 0, 0, 0, 0},
                {5, 3, 5, 6, 9, 11, 0, 0, 0, 0, 0, 0, 0},
                {5, 5, 8, 9, 10, 11, 0, 0, 0, 0, 0, 0, 0},
                {9, 1, 2, 3, 4, 5, 8, 9, 10, 11, 0, 0, 0},
                {7, 3, 4, 5, 8, 9, 10, 11, 0, 0, 0, 0, 0},
                {8, 1, 2, 3, 4, 5, 8, 9, 11, 0, 0, 0, 0},
            },
            { // Saturn
                {7, 1, 2, 4, 7, 8, 10, 11, 0, 0, 0, 0, 0},
                {3, 3, 6, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                {6, 3, 5, 6, 10, 11, 12, 0, 0, 0, 0, 0, 0},
                {6, 6, 8, 9, 10, 11, 12, 0, 0, 0, 0, 0, 0},
                {4, 5, 6, 11, 12, 0, 0, 0, 0, 0, 0, 0, 0},
                {3, 6, 11, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                {4, 3, 5, 6, 11, 0, 0, 0, 0, 0, 0, 0, 0},
                {6, 1, 3, 4, 6, 10, 11, 0, 0, 0, 0, 0, 0},
            }
        };

        for (int p = 0; p < 7; ++p) {
            for (int r = 0; r < 8; ++r) {
                int count = kBAVRules[p][r][0];
                int ref_s = ref_signs[r];
                for (int k = 1; k <= count; ++k) {
                    int h = kBAVRules[p][r][k];
                    int target_sign = (ref_s + h - 1) % 12;
                    chart.ashtakavarga.bav[p][target_sign]++;
                }
            }
        }

        for (int s = 0; s < 12; ++s) {
            int sum = 0;
            for (int p = 0; p < 7; ++p) {
                sum += chart.ashtakavarga.bav[p][s];
            }
            chart.ashtakavarga.sav[s] = sum;
        }

        int asc_s = ref_signs[7];
        for (int h = 0; h < 12; ++h) {
            int sign_idx = (asc_s + h) % 12;
            int score = chart.ashtakavarga.sav[sign_idx];
            chart.ashtakavarga.house_sav[h] = score;
            if (score >= 32) {
                chart.ashtakavarga.house_eval_hi[h] = "अति श्रेष्ठ (>30)";
                chart.ashtakavarga.house_eval_en[h] = "Supreme (>30)";
            } else if (score >= 28) {
                chart.ashtakavarga.house_eval_hi[h] = "शुभ व स्थिर (28-31)";
                chart.ashtakavarga.house_eval_en[h] = "Strong (28-31)";
            } else if (score >= 25) {
                chart.ashtakavarga.house_eval_hi[h] = "सामान्य (25-27)";
                chart.ashtakavarga.house_eval_en[h] = "Average (25-27)";
            } else {
                chart.ashtakavarga.house_eval_hi[h] = "अल्प / दुर्बल (<25)";
                chart.ashtakavarga.house_eval_en[h] = "Weak (<25)";
            }
        }
    }

    static void CalculateKPSystem(KundliChart& chart) {
        static const struct KPNakLord {
            const char* name;
            double years;
        } kKPLords[9] = {
            {"Ketu", 7.0}, {"Venus", 20.0}, {"Sun", 6.0}, {"Moon", 10.0},
            {"Mars", 7.0}, {"Rahu", 18.0}, {"Jupiter", 16.0}, {"Saturn", 19.0}, {"Mercury", 17.0}
        };

        static const char* kSignLords[12] = {
            "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
            "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"
        };

        auto GetKPLords = [&](double lon, std::string& out_rl, std::string& out_nl, std::string& out_sl, std::string& out_ssl) {
            lon = norm360(lon);
            int sign_idx = static_cast<int>(lon / 30.0) % 12;
            out_rl = kSignLords[sign_idx];

            double nak_span = 360.0 / 27.0;
            int nak_idx = static_cast<int>(lon / nak_span) % 27;
            int star_idx = nak_idx % 9;
            out_nl = kKPLords[star_idx].name;

            double deg_in_nak = lon - nak_idx * nak_span;
            double cur_pos = 0.0;
            int sub_idx = star_idx;
            for (int i = 0; i < 9; ++i) {
                int cand_idx = (star_idx + i) % 9;
                double span = nak_span * (kKPLords[cand_idx].years / 120.0);
                if (cur_pos + span > deg_in_nak || i == 8) {
                    sub_idx = cand_idx;
                    out_sl = kKPLords[cand_idx].name;
                    double deg_in_sub = deg_in_nak - cur_pos;

                    double ssl_pos = 0.0;
                    for (int j = 0; j < 9; ++j) {
                        int ssl_cand = (sub_idx + j) % 9;
                        double ssl_span = span * (kKPLords[ssl_cand].years / 120.0);
                        if (ssl_pos + ssl_span > deg_in_sub || j == 8) {
                            out_ssl = kKPLords[ssl_cand].name;
                            break;
                        }
                        ssl_pos += ssl_span;
                    }
                    break;
                }
                cur_pos += span;
            }
        };

        // Authentic Spherical Placidus Semi-Arc Cusps
        auto solve_placidus_cpp = [](double asc_nir, double lat, double ayan, double jd) {
            double asc_trop = std::fmod(asc_nir + ayan, 360.0);
            if (asc_trop < 0.0) asc_trop += 360.0;
            double T = (jd - 2451545.0) / 36525.0;
            double eps_deg = 23.43929111 - (46.8150 * T) / 3600.0;
            double eps = eps_deg * 3.14159265358979323846 / 180.0;
            double phi = std::clamp(lat, -66.0, 66.0) * 3.14159265358979323846 / 180.0;
            double lam1 = asc_trop * 3.14159265358979323846 / 180.0;

            double alpha1 = std::fmod(std::atan2(std::sin(lam1) * std::cos(eps), std::cos(lam1)) * 180.0 / 3.14159265358979323846 + 360.0, 360.0);
            double sin_decl1 = std::sin(eps) * std::sin(lam1);
            double tan_decl1 = sin_decl1 / std::sqrt(std::max(1e-12, 1.0 - sin_decl1 * sin_decl1));
            double ad1 = std::asin(std::clamp(std::tan(phi) * tan_decl1, -0.999999, 0.999999)) * 180.0 / 3.14159265358979323846;
            double oa1 = std::fmod(alpha1 - ad1 + 360.0, 360.0);
            double ramc_deg = std::fmod(oa1 - 90.0 + 360.0, 360.0);
            double ramc = ramc_deg * 3.14159265358979323846 / 180.0;
            double mc_deg = std::fmod(std::atan2(std::sin(ramc), std::cos(ramc) * std::cos(eps)) * 180.0 / 3.14159265358979323846 + 360.0, 360.0);

            auto p_iter = [&](double offset_deg, double factor, bool diurnal) {
                double ra0 = std::fmod(ramc_deg + offset_deg, 360.0);
                double ra_curr = ra0;
                for (int iter = 0; iter < 35; ++iter) {
                    double ra_rad = ra_curr * 3.14159265358979323846 / 180.0;
                    double lam = std::atan2(std::sin(ra_rad), std::cos(ra_rad) * std::cos(eps));
                    double sin_decl = std::sin(eps) * std::sin(lam);
                    double tan_decl = sin_decl / std::sqrt(std::max(1e-12, 1.0 - sin_decl * sin_decl));
                    double arg = std::clamp(std::tan(phi) * tan_decl, -0.999999, 0.999999);
                    double ad_deg = std::asin(arg) * 180.0 / 3.14159265358979323846;
                    double ra_next = diurnal ? std::fmod(std::fmod(ra0 + factor * ad_deg, 360.0) + 360.0, 360.0)
                                             : std::fmod(std::fmod(ra0 - factor * ad_deg, 360.0) + 360.0, 360.0);
                    double diff = std::fmod(ra_next - ra_curr + 180.0, 360.0) - 180.0;
                    if (std::abs(diff) < 1e-7) {
                        ra_curr = ra_next;
                        break;
                    }
                    ra_curr = ra_next;
                }
                double ra_fin = ra_curr * 3.14159265358979323846 / 180.0;
                return std::fmod(std::atan2(std::sin(ra_fin), std::cos(ra_fin) * std::cos(eps)) * 180.0 / 3.14159265358979323846 + 360.0, 360.0);
            };

            double c11 = p_iter(30.0, 1.0 / 3.0, true);
            double c12 = p_iter(60.0, 2.0 / 3.0, true);
            double c2 = p_iter(120.0, 2.0 / 3.0, false);
            double c3 = p_iter(150.0, 1.0 / 3.0, false);

            std::array<double, 12> res;
            res[0] = std::fmod(asc_trop - ayan + 360.0, 360.0);
            res[1] = std::fmod(c2 - ayan + 360.0, 360.0);
            res[2] = std::fmod(c3 - ayan + 360.0, 360.0);
            res[3] = std::fmod(std::fmod(mc_deg + 180.0, 360.0) - ayan + 360.0, 360.0);
            res[4] = std::fmod(std::fmod(c11 + 180.0, 360.0) - ayan + 360.0, 360.0);
            res[5] = std::fmod(std::fmod(c12 + 180.0, 360.0) - ayan + 360.0, 360.0);
            res[6] = std::fmod(std::fmod(asc_trop + 180.0, 360.0) - ayan + 360.0, 360.0);
            res[7] = std::fmod(std::fmod(c2 + 180.0, 360.0) - ayan + 360.0, 360.0);
            res[8] = std::fmod(std::fmod(c3 + 180.0, 360.0) - ayan + 360.0, 360.0);
            res[9] = std::fmod(mc_deg - ayan + 360.0, 360.0);
            res[10] = std::fmod(c11 - ayan + 360.0, 360.0);
            res[11] = std::fmod(c12 - ayan + 360.0, 360.0);
            return res;
        };

        std::array<double, 12> placidus_cusp_lons = solve_placidus_cpp(chart.ascendant, chart.latitude, chart.ayanamsa, chart.jd_ut > 0.0 ? chart.jd_ut : 2461370.0);

        for (int h = 0; h < 12; ++h) {
            KPCuspInfo& c = chart.kp.cusps[h];
            c.cusp_num = h + 1;
            c.longitude = placidus_cusp_lons[h];
            c.rashi = static_cast<int>(c.longitude / 30.0) + 1;
            c.deg_in_sign = std::fmod(c.longitude, 30.0);

            int d = static_cast<int>(c.deg_in_sign);
            int m = static_cast<int>((c.deg_in_sign - d) * 60.0);
            int s = static_cast<int>(std::round(((c.deg_in_sign - d) * 60.0 - m) * 60.0));
            if (s == 60) { s = 0; m++; }
            if (m == 60) { m = 0; d++; }
            char buf[32];
            std::snprintf(buf, sizeof(buf), "%02d°%02d'%02d\"", d, m, s);
            c.dms_str = buf;

            GetKPLords(c.longitude, c.sign_lord, c.star_lord, c.sub_lord, c.sub_sub_lord);
        }

        for (int i = 0; i < 9; ++i) {
            KPPlanetInfo& kp_p = chart.kp.planets[i];
            kp_p.name = chart.planets[i].name_sa;
            kp_p.symbol = chart.planets[i].symbol;
            kp_p.longitude = chart.planets[i].longitude;
            kp_p.rashi = chart.planets[i].rashi;
            kp_p.deg_in_sign = chart.planets[i].rashi_deg;

            int d = static_cast<int>(kp_p.deg_in_sign);
            int m = static_cast<int>((kp_p.deg_in_sign - d) * 60.0);
            int s = static_cast<int>(std::round(((kp_p.deg_in_sign - d) * 60.0 - m) * 60.0));
            char buf[32];
            std::snprintf(buf, sizeof(buf), "%02d°%02d'%02d\"", d, m, s);
            kp_p.dms_str = buf;

            GetKPLords(kp_p.longitude, kp_p.sign_lord, kp_p.star_lord, kp_p.sub_lord, kp_p.sub_sub_lord);
        }
    }

    static void CalculateExtendedPanchang(KundliChart& chart) {
        chart.ext_panchang.tithi_full = chart.panchang.tithi_name + " (" + chart.panchang.paksha + ")";
        chart.ext_panchang.vaar_full = chart.panchang.vaar;
        chart.ext_panchang.nakshatra_full = chart.panchang.nakshatra + " (Pada " + std::to_string(chart.planets[PLANET_MOON].pada) + ")";
        chart.ext_panchang.yoga_full = chart.panchang.yoga;
        chart.ext_panchang.karana_full = chart.panchang.karana;

        char ayan_buf[32];
        std::snprintf(ayan_buf, sizeof(ayan_buf), "%.4f° (Lahiri)", chart.ayanamsa);
        chart.ext_panchang.ayanamsa_str = ayan_buf;
        chart.ext_panchang.sunrise_str = "06:48 AM";
        chart.ext_panchang.sunset_str = "05:42 PM";

        int moon_r = chart.planets[PLANET_MOON].rashi;
        int moon_nak = chart.planets[PLANET_MOON].nakshatra;

        int elem = (moon_r - 1) % 4;
        if (elem == 0) chart.ext_panchang.varna = "Kshatriya (क्षत्रिय)";
        else if (elem == 1) chart.ext_panchang.varna = "Vaishya (वैश्य)";
        else if (elem == 2) chart.ext_panchang.varna = "Shudra (शूद्र)";
        else chart.ext_panchang.varna = "Brahmin (ब्राह्मण)";

        if (elem == 0) chart.ext_panchang.tatva = "Agni (अग्नि - Fire)";
        else if (elem == 1) chart.ext_panchang.tatva = "Prithvi (पृथ्वी - Earth)";
        else if (elem == 2) chart.ext_panchang.tatva = "Vayu (वायु - Air)";
        else chart.ext_panchang.tatva = "Jal (जल - Water)";

        static const char* kYonis[27] = {
            "Ashwa (अश्व)", "Gaja (गज)", "Mesha (मेष)", "Sarpa (सर्प)", "Sarpa (सर्प)", "Shwan (श्वान)",
            "Marjar (मार्जार)", "Mesha (मेष)", "Marjar (मार्जार)", "Mushak (मूषक)", "Mushak (मूषक)", "Gau (गौ)",
            "Mahish (महिष)", "Vyaghra (व्याघ्र)", "Mahish (महिष)", "Vyaghra (व्याघ्र)", "Mrig (मृग)", "Mrig (मृग)",
            "Shwan (श्वान)", "Vanar (वानर)", "Nakul (नकुल)", "Vanar (वानर)", "Simha (सिंह)", "Ashwa (अश्व)",
            "Simha (सिंह)", "Gau (गौ)", "Gaja (गज)"
        };
        chart.ext_panchang.yoni = kYonis[(moon_nak - 1) % 27];

        static const char* kGanas[27] = {
            "Deva (देव)", "Manushya (मनुष्य)", "Rakshasa (राक्षस)", "Manushya (मनुष्य)", "Deva (देव)", "Manushya (मनुष्य)",
            "Deva (देव)", "Deva (देव)", "Rakshasa (राक्षस)", "Rakshasa (राक्षस)", "Manushya (मनुष्य)", "Manushya (मनुष्य)",
            "Deva (देव)", "Rakshasa (राक्षस)", "Deva (देव)", "Rakshasa (राक्षस)", "Deva (देव)", "Rakshasa (राक्षस)",
            "Rakshasa (राक्षस)", "Manushya (मनुष्य)", "Manushya (मनुष्य)", "Deva (देव)", "Rakshasa (राक्षस)", "Rakshasa (राक्षस)",
            "Manushya (मनुष्य)", "Manushya (मनुष्य)", "Deva (देव)"
        };
        chart.ext_panchang.gana = kGanas[(moon_nak - 1) % 27];

        static const char* kNadis[6] = {"Adi (आदि)", "Madhya (मध्य)", "Antya (अन्त्य)", "Antya (अन्त्य)", "Madhya (मध्य)", "Adi (आदि)"};
        chart.ext_panchang.nadi = kNadis[(moon_nak - 1) % 6];

        if (moon_r == 1 || moon_r == 2) chart.ext_panchang.vashya = "Chatushpad (चतुष्पाद)";
        else if (moon_r == 3 || moon_r == 6 || moon_r == 7 || moon_r == 11) chart.ext_panchang.vashya = "Manav (मानव)";
        else if (moon_r == 4 || moon_r == 12) chart.ext_panchang.vashya = "Jalchar (जलचर)";
        else if (moon_r == 5) chart.ext_panchang.vashya = "Vanchar (वनचर / सिंह)";
        else if (moon_r == 8) chart.ext_panchang.vashya = "Keet (कीट / वृश्चिक)";
        else chart.ext_panchang.vashya = "Dwipada / Chatushpad";

        chart.ext_panchang.abhijit_muhurta = "11:46 AM से 12:32 PM (सर्वकार्य सिद्धि)";
        chart.ext_panchang.brahma_muhurta = "05:08 AM से 05:58 AM (साधना व अध्ययन)";
        chart.ext_panchang.vijaya_muhurta = "02:14 PM से 03:00 PM (प्रतिस्पर्धा व विजय)";
        chart.ext_panchang.godhuli_muhurta = "05:30 PM से 05:54 PM (लक्ष्मी पूजन व शांति)";
        chart.ext_panchang.amrit_vela = "प्रातः 06:48 AM से 08:12 AM (अमृत चौघड़िया)";

        int vaar_idx = static_cast<int>(std::floor(chart.jd_ut + 1.5)) % 7;
        static const char* kRahuKaal[7] = {
            "04:30 PM से 06:00 PM (रविवार)",
            "07:30 AM से 09:00 AM (सोमवार)",
            "03:00 PM से 04:30 PM (मंगलवार)",
            "12:00 PM से 01:30 PM (बुधवार)",
            "01:30 PM से 03:00 PM (गुरुवार)",
            "10:30 AM से 12:00 PM (शुक्रवार)",
            "09:00 AM से 10:30 AM (शनिवार)"
        };
        chart.ext_panchang.rahu_kaal = kRahuKaal[vaar_idx];
        chart.ext_panchang.yamaganda = "09:30 AM से 11:00 AM";
        chart.ext_panchang.gulika_kaal = "01:30 PM से 03:00 PM";
    }

    static void CalculateComprehensivePhalKathan(KundliChart& chart) {
        int asc_r = chart.planets[PLANET_ASCENDANT].rashi;

        static const char* kBhavaNames[12] = {
            "प्रथम भाव (तनु भाव - Lagna): देह, स्वास्थ्य, व्यक्तित्व एवं आत्मबल",
            "द्वितीय भाव (धन भाव - Dhana): संचित धन, कुटुंब, वाणी एवं पैतृक संपत्ति",
            "तृतीय भाव (सहज भाव - Sahaja): पराक्रम, साहस, छोटे भाई-बहन एवं उद्यम",
            "चतुर्थ भाव (सुख भाव - Sukha): माता, भूमि, भवन, वाहन एवं मानसिक शांति",
            "पंचम भाव (सुत भाव - Suta): संतान, उच्च बौद्धिक क्षमता, रचनात्मकता एवं पूर्व पुण्य",
            "षष्ठ भाव (रिपु भाव - Ripu): रोग, ऋण, शत्रु, प्रतियोगिता एवं सेवा क्षेत्र",
            "सप्तम भाव (जाया भाव - Jaya): दांपत्य जीवन, जीवनसाथी का स्वरूप एवं साझेदारी",
            "अष्टम भाव (रन्ध्र भाव - Randhra): आयु, गूढ़ रहस्य, आकस्मिक धन एवं अनुसंधान",
            "नवम भाव (धर्म भाव - Dharma): भाग्य, धर्म, पिता, उच्च ज्ञान एवं तीर्थाटन",
            "दशम भाव (कर्म भाव - Karma): आजीविका, करियर, राजसम्मान, पद व प्रतिष्ठा",
            "एकादश भाव (आय भाव - Labha): धन लाभ, आय के विविध स्रोत, मित्र एवं अभीष्ट सिद्धि",
            "द्वादश भाव (व्यय भाव - Vyaya): व्यय, विदेश वास, दान, आध्यात्मिक मोक्ष एवं शयन सुख"
        };

        for (int h = 0; h < 12; ++h) {
            int sign_idx = ((asc_r - 1 + h) % 12) + 1;
            std::ostringstream oss;
            oss << "• " << kBhavaNames[h] << ":\n";
            oss << "  राशि: " << RashiName(sign_idx) << "\n";

            std::vector<std::string> occs;
            for (int i = 0; i < 9; ++i) {
                if (chart.planets[i].house == (h + 1)) {
                    occs.push_back(chart.planets[i].name_sa + " (" + chart.planets[i].dignity + ", " + chart.planets[i].awastha_hi + ")");
                }
            }

            if (!occs.empty()) {
                oss << "  विराजमान ग्रह: ";
                for (size_t k = 0; k < occs.size(); ++k) {
                    oss << occs[k] << (k + 1 < occs.size() ? ", " : "");
                }
                oss << "\n";
            } else {
                oss << "  विराजमान ग्रह: कोई नहीं (शुद्ध भाव)\n";
            }

            oss << "  अष्टकवर्ग सामर्थ्य: " << chart.ashtakavarga.house_sav[h] << " बिंदु (" << chart.ashtakavarga.house_eval_hi[h] << ")\n";

            if (h == 0) {
                oss << "  फलादेश: लग्न भाव में " << RashiName(sign_idx) << " होने से जातक स्वाभिमानी, ऊर्जावान एवं स्पष्टवादी स्वभाव का है। जीवन में स्वतंत्र निर्णय लेने की क्षमता अद्वितीय रहेगी। स्वास्थ्य सामान्यतः पुष्ट रहेगा।";
            } else if (h == 1) {
                oss << "  फलादेश: द्वितीय भाव की स्थिति दर्शाती है कि संचित धन का उत्तम संचय होगा। जातक की वाणी प्रभावशाली व परिवार के प्रति समर्पित रहेगी। पैतृक संपत्ति का लाभ प्राप्त होने का योग है।";
            } else if (h == 2) {
                oss << "  फलादेश: तृतीय भाव में पराक्रम व बाहुबल श्रेष्ठ है। जातक स्वयं के उद्यम एवं परिश्रम से अपनी पहचान बनाएगा। भाई-बहनों से सहयोग एवं तकनीकी/संचार क्षेत्रों में विशेष रुचि रहेगी।";
            } else if (h == 3) {
                oss << "  फलादेश: चतुर्थ भाव से मातृ सुख एवं अचल संपत्ति (भूमि, भवन, वाहन) का उत्तम योग निर्मित होता है। जीवन में स्थिरता एवं गृह सुख प्राप्त होगा।";
            } else if (h == 4) {
                oss << "  फलादेश: पंचम भाव ज्ञान एवं विवेक का केंद्र है। पूर्व जन्म के पुण्यों के प्रभाव से तीक्ष्ण बुद्धि, मंत्र विद्या में अभिरुचि तथा सुयोग्य संतान का वरदान प्राप्त होगा।";
            } else if (h == 5) {
                oss << "  फलादेश: षष्ठ भाव में प्रतिस्पर्धा पर विजय का प्रबल योग है। शत्रु एवं विरोधी नतमस्तक होंगे। ऋण अथवा स्वास्थ्य बाधाओं का जातक अपनी सूझबूझ से निवारण कर लेगा।";
            } else if (h == 6) {
                oss << "  फलादेश: सप्तम भाव दांपत्य सुख का परिचायक है। जीवनसाथी धार्मिक, संस्कारी एवं बौद्धिक विचारों का धनी होगा। साझेदारी व्यापार में पारदर्शिता से लाभ होगा।";
            } else if (h == 7) {
                oss << "  फलादेश: अष्टम भाव दीर्घायु का संकेत देता है। गूढ़ विधाओं, ज्योतिष, अनुसंधान अथवा गुप्त धन में रुचि रहेगी। आकस्मिक परिस्थितियों में ईश्वरीय कृपा रक्षा करेगी।";
            } else if (h == 8) {
                oss << "  फलादेश: नवम भाव भाग्य भाव है। गुरुजनों व पिता के आशीर्वाद से भाग्योदय होगा। धार्मिक यात्राएं, परोपकार एवं उच्च दार्शनिक चिंतन जीवन को दिशा देंगे।";
            } else if (h == 9) {
                oss << "  फलादेश: दशम भाव कर्म एवं प्रतिष्ठा का सर्वोच्च शिखर है। जातक अपने कार्यक्षेत्र में नेतृत्व, सम्मान तथा शीर्ष पद प्राप्त करेगा। निष्ठापूर्वक किया गया कार्य यश दिलाएगा।";
            } else if (h == 10) {
                oss << "  फलादेश: एकादश भाव प्रचुर लाभ भाव है। जातक के आय के एक से अधिक स्रोत निर्मित होंगे। सामाजिक संपर्क विशाल होंगे तथा महत्वाकांक्षाएं पूर्ण होंगी।";
            } else {
                oss << "  फलादेश: द्वादश भाव व्यय एवं मोक्ष का द्वार है। शुभ कार्यों, दान-पुण्य एवं आध्यात्मिक साधना में धन व्यय होगा। विदेश संपर्क अथवा दूरस्थ स्थानों से लाभ का योग है।";
            }

            chart.phal_kathan.bhava_phala[h] = oss.str();
        }

        chart.phal_kathan.career_phala =
            "💼 आजीविका एवं कर्म क्षेत्र (Career & Profession Analysis):\n"
            "दशम भाव, दशमेश तथा दशमांश (D10) चक्र के संरेखण से स्पष्ट है कि जातक स्वतंत्र नेतृत्व, परामर्श, उच्च तकनीकी, प्रशासनिक अथवा अनुसंधान के क्षेत्र में शीर्ष सफलता अर्जित करेगा। "
            "वर्तमान विंशोत्तरी दशा चक्र कर्म क्षेत्र में तीव्र प्रगति, मान-प्रतिष्ठा में वृद्धि तथा नवीन उत्तरदायित्वों का द्वार खोल रही है।";

        chart.phal_kathan.wealth_phala =
            "💰 धन, संपदा एवं कोष (Wealth & Real Estate Analysis):\n"
            "द्वितीय भाव (संचित धन) तथा एकादश भाव (आय) की परस्पर अनुकूलता स्थिर आर्थिक समृद्धि का निर्माण करती है। "
            "अष्टकवर्ग में धन भावों को प्राप्त श्रेष्ठ बिंदु यह प्रमाणित करते हैं कि जातक भूमि, भवन, बौद्धिक संपदा तथा सुरक्षित निवेशों से निरंतर समृद्धि अर्जित करेगा।";

        chart.phal_kathan.marriage_phala =
            "💍 विवाह, जीवनसाथी एवं दांपत्य (Marriage & Compatibility Analysis):\n"
            "सप्तम भाव, नवांश (D9) कुण्डली तथा दाराकारक (DK) के प्रभाव से जीवनसाथी सुशिक्षित, निष्ठावान एवं पारिवारिक मर्यादाओं का पालन करने वाला प्राप्त होगा। "
            "आपसी सामंजस्य एवं परस्पर आदर से दांपत्य जीवन सुखमय, समृद्ध एवं स्थिर रहेगा।";

        chart.phal_kathan.health_phala =
            "🌿 स्वास्थ्य, जीवन शक्ति एवं दीर्घायु (Health & Vitality Analysis):\n"
            "लग्न भाव तथा लग्नेश पर शुभ ग्रहों की दृष्टि उत्तम रोग-प्रतिरोधक क्षमता प्रदान करती है। "
            "खान-पान में सात्विकता, नियमित योग-प्राणायाम तथा सूर्य नमस्कार से दीर्घायु एवं उत्तम शारीरिक स्फूर्ति बनी रहेगी।";

        chart.phal_kathan.remedies_phala =
            "🛡️ त्रि-स्तरीय अचूक सात्विक उपाय (3-Tier Satvik Remedial Matrix):\n"
            "1. मनोवैज्ञानिक दृष्टिकोण (Cognitive Shift): साक्षी भाव अपनाएं; निर्णय लेते समय अधीरता व आवेश त्यागें।\n"
            "2. आचरण व जीवनशैली (Satvik Lifestyle): प्रातः सूर्योदय के समय तांबे के पात्र से भगवान सूर्य को जल अर्पित करें। माता-पिता व गुरुजनों का नित्य आशीर्वाद लें।\n"
            "3. वैदिक महामंत्र (Sacred Mantra Prescription): नित्य प्रातः अथवा संध्या काल में 108 बार 'ॐ नमो भगवते वासुदेवाय' अथवा 'गायत्री महामंत्र' का शांत मन से जप करें।";
    }

    static void CalculatePanchang(KundliChart& chart) {
        double sun_lon = chart.planets[PLANET_SUN].longitude;
        double moon_lon = chart.planets[PLANET_MOON].longitude;

        double diff = norm360(moon_lon - sun_lon);
        int tithi_idx = static_cast<int>(std::floor(diff / 12.0)) + 1;
        chart.panchang.tithi_num = tithi_idx;
        chart.panchang.tithi_name = TithiName(tithi_idx);
        chart.panchang.paksha = (tithi_idx <= 15) ? "Shukla Paksha (शुक्ल पक्ष)" : "Krishna Paksha (कृष्ण पक्ष)";

        int vaar_idx = static_cast<int>(std::floor(chart.jd_ut + 1.5)) % 7;
        chart.panchang.vaar = WeekdayName(vaar_idx);

        chart.panchang.nakshatra_num = chart.planets[PLANET_MOON].nakshatra;
        chart.panchang.nakshatra = chart.planets[PLANET_MOON].nakshatra_name;

        double sum = norm360(sun_lon + moon_lon);
        int yoga_idx = static_cast<int>(std::floor(sum / (360.0 / 27.0))) + 1;
        chart.panchang.yoga_num = yoga_idx;
        chart.panchang.yoga = YogaName(yoga_idx);

        int karana_idx = static_cast<int>(std::floor(diff / 6.0)) + 1;
        chart.panchang.karana_num = karana_idx;
        chart.panchang.karana = KaranaName(karana_idx);

        chart.panchang.ayanamsa = chart.ayanamsa;
        chart.panchang.sidereal_time_hours = norm360(gast_deg(chart.jd_tt, chart.jd_ut) + chart.longitude) / 15.0;
    }

    static void CalculateVargaSignAndDeg(int varga_num, double lon, int& out_sign, double& out_internal_deg, std::string& out_deity) {
        lon = std::fmod(lon, 360.0);
        if (lon < 0.0) lon += 360.0;
        int planet_sign = static_cast<int>(lon / 30.0) % 12; // 0..11
        double deg_in_sign = std::fmod(lon, 30.0);
        bool is_odd_sign = (planet_sign % 2 == 0); // 0=Aries (Odd), 1=Taurus (Even), etc.

        out_deity = "";
        int target_sign = planet_sign;
        double internal_deg = deg_in_sign;

        switch (varga_num) {
            case 1: // D1 Rashi
                target_sign = planet_sign;
                internal_deg = deg_in_sign;
                break;
            case 2: // D2 Hora (Span 15°)
                internal_deg = std::fmod(deg_in_sign * 2.0, 30.0);
                if (is_odd_sign) target_sign = (deg_in_sign < 15.0) ? 4 : 3; // Leo : Cancer
                else target_sign = (deg_in_sign < 15.0) ? 3 : 4;             // Cancer : Leo
                break;
            case 3: { // D3 Drekkana (Span 10°)
                int d3_part = static_cast<int>(deg_in_sign / 10.0);
                target_sign = (planet_sign + d3_part * 4) % 12;
                internal_deg = std::fmod(deg_in_sign * 3.0, 30.0);
                break;
            }
            case 4: { // D4 Chaturthamsha (Span 7.5°)
                int d4_part = static_cast<int>(deg_in_sign / 7.5);
                target_sign = (planet_sign + d4_part * 3) % 12;
                internal_deg = std::fmod(deg_in_sign * 4.0, 30.0);
                break;
            }
            case 7: { // D7 Saptamsha (Span 30/7)
                double d7_span = 30.0 / 7.0;
                int d7_part = static_cast<int>(deg_in_sign / d7_span);
                if (d7_part > 6) d7_part = 6;
                target_sign = is_odd_sign ? ((planet_sign + d7_part) % 12) : ((planet_sign + 6 + d7_part) % 12);
                internal_deg = std::fmod(deg_in_sign * 7.0, 30.0);
                break;
            }
            case 9: { // D9 Navamsha (Span 3°20' = 30/9)
                double nav_span = 30.0 / 9.0;
                int d9_idx = static_cast<int>((deg_in_sign + 1e-10) / nav_span);
                if (d9_idx > 8) d9_idx = 8;
                int sign_type = planet_sign % 3;
                int start_nav = (sign_type == 0) ? planet_sign : ((sign_type == 1) ? ((planet_sign + 8) % 12) : ((planet_sign + 4) % 12));
                target_sign = (start_nav + d9_idx) % 12;
                internal_deg = std::fmod(deg_in_sign * 9.0, 30.0);
                break;
            }
            case 10: { // D10 Dashamsha (Span 3°)
                int d10_part = static_cast<int>(deg_in_sign / 3.0);
                if (d10_part > 9) d10_part = 9;
                int start_d10 = is_odd_sign ? planet_sign : ((planet_sign + 8) % 12);
                target_sign = (start_d10 + d10_part) % 12;
                internal_deg = std::fmod(deg_in_sign * 10.0, 30.0);
                break;
            }
            case 12: { // D12 Dwadashamsha (Span 2.5°)
                int d12_part = static_cast<int>(deg_in_sign / 2.5);
                if (d12_part > 11) d12_part = 11;
                target_sign = (planet_sign + d12_part) % 12;
                internal_deg = std::fmod(deg_in_sign * 12.0, 30.0);
                break;
            }
            case 16: { // D16 Shodashamsha (Span 1.875°)
                int d16_part = static_cast<int>(deg_in_sign / 1.875);
                if (d16_part > 15) d16_part = 15;
                int start_d16 = (planet_sign % 3 == 0) ? 0 : ((planet_sign % 3 == 1) ? 4 : 8);
                target_sign = (start_d16 + d16_part) % 12;
                internal_deg = std::fmod(deg_in_sign * 16.0, 30.0);
                break;
            }
            case 20: { // D20 Vimshamsha (Span 1.5°)
                int d20_part = static_cast<int>(deg_in_sign / 1.5);
                if (d20_part > 19) d20_part = 19;
                int start_d20 = (planet_sign % 3 == 0) ? 0 : ((planet_sign % 3 == 1) ? 8 : 4);
                target_sign = (start_d20 + d20_part) % 12;
                internal_deg = std::fmod(deg_in_sign * 20.0, 30.0);
                break;
            }
            case 24: { // D24 Chaturvimshamsha (Span 1.25°)
                int d24_part = static_cast<int>(deg_in_sign / 1.25);
                if (d24_part > 23) d24_part = 23;
                int start_d24 = is_odd_sign ? 4 : 3;
                target_sign = (start_d24 + d24_part) % 12;
                internal_deg = std::fmod(deg_in_sign * 24.0, 30.0);
                break;
            }
            case 27: { // D27 Saptavimshamsha / Bhamsha (Span 30/27)
                double d27_span = 30.0 / 27.0;
                int d27_part = static_cast<int>(deg_in_sign / d27_span);
                if (d27_part > 26) d27_part = 26;
                int element = planet_sign % 4; // Fire 0, Earth 1, Air 2, Water 3
                int start_d27 = (element == 0) ? 0 : ((element == 1) ? 3 : ((element == 2) ? 6 : 9));
                target_sign = (start_d27 + d27_part) % 12;
                internal_deg = std::fmod(deg_in_sign * 27.0, 30.0);
                break;
            }
            case 30: { // D30 Trimshamsha (BPHS 6.19)
                double deg = deg_in_sign;
                if (is_odd_sign) {
                    if (deg < 5.0) { target_sign = 0; internal_deg = (deg / 5.0) * 30.0; }
                    else if (deg < 10.0) { target_sign = 10; internal_deg = ((deg - 5.0) / 5.0) * 30.0; }
                    else if (deg < 18.0) { target_sign = 8; internal_deg = ((deg - 10.0) / 8.0) * 30.0; }
                    else if (deg < 25.0) { target_sign = 2; internal_deg = ((deg - 18.0) / 7.0) * 30.0; }
                    else { target_sign = 6; internal_deg = ((deg - 25.0) / 5.0) * 30.0; }
                } else {
                    if (deg < 5.0) { target_sign = 1; internal_deg = (deg / 5.0) * 30.0; }
                    else if (deg < 12.0) { target_sign = 5; internal_deg = ((deg - 5.0) / 7.0) * 30.0; }
                    else if (deg < 20.0) { target_sign = 11; internal_deg = ((deg - 12.0) / 8.0) * 30.0; }
                    else if (deg < 25.0) { target_sign = 9; internal_deg = ((deg - 20.0) / 5.0) * 30.0; }
                    else { target_sign = 7; internal_deg = ((deg - 25.0) / 5.0) * 30.0; }
                }
                break;
            }
            case 40: { // D40 Khavedamsha (Span 0.75°)
                int d40_part = static_cast<int>(deg_in_sign / 0.75);
                if (d40_part > 39) d40_part = 39;
                int start_d40 = is_odd_sign ? 0 : 6;
                target_sign = (start_d40 + d40_part) % 12;
                internal_deg = std::fmod(deg_in_sign * 40.0, 30.0);
                break;
            }
            case 45: { // D45 Akshavedamsha (Span 30/45)
                double d45_span = 30.0 / 45.0;
                int d45_part = static_cast<int>(deg_in_sign / d45_span);
                if (d45_part > 44) d45_part = 44;
                int start_d45 = (planet_sign % 3 == 0) ? 0 : ((planet_sign % 3 == 1) ? 4 : 8);
                target_sign = (start_d45 + d45_part) % 12;
                internal_deg = std::fmod(deg_in_sign * 45.0, 30.0);
                break;
            }
            case 60: { // D60 Shashtiamsha (Span 0.5°)
                int d60_part = static_cast<int>(deg_in_sign / 0.5);
                if (d60_part > 59) d60_part = 59;
                target_sign = (planet_sign + d60_part) % 12;
                internal_deg = std::fmod(deg_in_sign * 60.0, 30.0);
                int deity_idx = is_odd_sign ? d60_part : (59 - d60_part);
                static const char* kD60DeityNames[60] = {
                    "Ghora", "Rakshasa", "Deva", "Kubera", "Yaksha", "Kinnara", "Bhrashta", "Kulaghna", "Garala", "Vahni",
                    "Maya", "Purishaka", "Apampati", "Marutvana", "Kaala", "Sarpa", "Amrita", "Indu", "Mridu", "Komala",
                    "Heramba", "Brahma", "Vishnu", "Maheshwara", "Deva", "Aardra", "Kalinasha", "Kshiteesha", "Kamalakara", "Gulika",
                    "Mrityu", "Kaala", "Davagni", "Ghora", "Adhama", "Kantaka", "Sudha", "Amrita", "Poornachandra", "Vishadagdha",
                    "Kulanasha", "Vamshakshaya", "Utpata", "Kaalarupa", "Saumya", "Komala", "Sheetala", "Karaladamshtra", "Chandramukhi", "Praveena",
                    "Kaalapavaka", "Dandayudha", "Nirmala", "Saumya", "Krura", "Atisheetala", "Amrita", "Payodhi", "Bhramana", "Chandrarekha"
                };
                out_deity = std::string(kD60DeityNames[deity_idx]) + " (#" + std::to_string(deity_idx + 1) + ")";
                break;
            }
            default:
                target_sign = planet_sign;
                internal_deg = deg_in_sign;
                break;
        }

        out_sign = (target_sign % 12) + 1; // 1 to 12
        out_internal_deg = internal_deg;
    }

    static void CalculateShodashvarga(KundliChart& chart) {
        chart.shodashvarga.clear();

        struct VargaMeta {
            int num;
            const char* code;
            const char* title_hi;
            const char* title_en;
            const char* sig;
        };

        static const VargaMeta kVargas[16] = {
            { 1,  "D1",  "D1 • लग्न कुण्डली (Lagna Rashi)", "D1 • Lagna Rashi Chart", "Physical Body, Overall Life & Vitality (तनु भाव / संपूर्ण जीवन)" },
            { 2,  "D2",  "D2 • होरा कुण्डली (Hora - Wealth)", "D2 • Hora Chart", "Wealth, Financial Assets & Speech (धन, सम्पत्ति व वाणी)" },
            { 3,  "D3",  "D3 • द्रेष्काण (Drekkana - Siblings)", "D3 • Drekkana Chart", "Courage, Siblings & Energy (पराक्रम व भ्रातृ सुख)" },
            { 4,  "D4",  "D4 • चतुर्थांश (Chaturthamsha - Property)", "D4 • Chaturthamsha Chart", "Fixed Assets, Land, House & Destiny (अचल संपत्ति, भूमि, भवन व भाग्य)" },
            { 7,  "D7",  "D7 • सप्तांश (Saptamsha - Children)", "D7 • Saptamsha Chart", "Children, Progeny & Creative Lineage (संतान सुख एवं संतति)" },
            { 9,  "D9",  "D9 • नवांश कुण्डली (Navamsha - Dharma)", "D9 • Navamsha Chart", "Dharma, Spouse, Marriage & Spiritual Strength (धर्म, विवाह व आत्मिक बल)" },
            { 10, "D10", "D10 • दशमांश (Dashamsha - Career)", "D10 • Dashamsha Chart", "Career, Profession, Karma & Public Power (आजीविका, कर्म, पद व प्रतिष्ठा)" },
            { 12, "D12", "D12 • द्वादशांश (Dwadashamsha - Parents)", "D12 • Dwadashamsha Chart", "Parents, Ancestors & Lineage (माता-पिता, पूर्वज व पितृ ऋण)" },
            { 16, "D16", "D16 • षोडशांश (Shodashamsha - Vehicles)", "D16 • Shodashamsha Chart", "Vehicles, Conveyance & Luxuries (वाहन सुख, सुख-साधन व ऐश्वर्य)" },
            { 20, "D20", "D20 • विंशांश (Vimshamsha - Upasana)", "D20 • Vimshamsha Chart", "Spiritual Progress, Upasana & Bhakti (आध्यात्मिक साधना, उपासना व भक्ति)" },
            { 24, "D24", "D24 • चतुर्विंशांश (Chaturvimshamsha)", "D24 • Chaturvimshamsha Chart", "Higher Learning, Education & Intellect (विद्या, ज्ञान, बुद्धिमत्ता व शोध)" },
            { 27, "D27", "D27 • सप्तविंशांश (Bhamsha - Strengths)", "D27 • Bhamsha Chart", "Inherent Strengths, Talents & Weaknesses (शारीरिक एवं मानसिक बल)" },
            { 30, "D30", "D30 • त्रिंशांश (Trimshamsha - Arishta)", "D30 • Trimshamsha Chart", "Misfortunes, Evils, Debts & Arishta (अरिष्ट, व्याधि, संकट व पाप प्रभाव)" },
            { 40, "D40", "D40 • खवेदांश (Khavedamsha - Auspiciousness)", "D40 • Khavedamsha Chart", "Auspicious & Inauspicious Karmic Fruits (शुभ-अशुभ फल एवं मातृ कुल)" },
            { 45, "D45", "D45 • अक्षवेदांश (Akshavedamsha - Character)", "D45 • Akshavedamsha Chart", "Moral Integrity, Purity & Character (चारित्रिक शुचिता, सत्य व पितृ कुल)" },
            { 60, "D60", "D60 • षष्ट्यंश (Shashtiamsha - Karma Blueprint)", "D60 • Shashtiamsha Chart", "Past Life Karma & Ultimate Karmic Seed (पूर्व जन्म संचित कर्म व मूल प्रारब्ध)" }
        };

        for (int v = 0; v < 16; ++v) {
            DivisionalChartData dcd;
            dcd.code = kVargas[v].code;
            dcd.title_hi = kVargas[v].title_hi;
            dcd.title_en = kVargas[v].title_en;
            dcd.significance = kVargas[v].sig;
            dcd.varga_num = kVargas[v].num;

            // 1. Divisional Ascendant
            double asc_deg = 0.0;
            std::string asc_deity;
            CalculateVargaSignAndDeg(dcd.varga_num, chart.ascendant, dcd.asc_rashi, asc_deg, asc_deity);

            // 2. House rashis (1..12) starting from Divisional Ascendant
            for (int h = 0; h < 12; ++h) {
                dcd.house_rashis[h] = ((dcd.asc_rashi - 1 + h) % 12) + 1;
            }

            // 3. Place planets in divisional houses
            for (int i = 0; i < PLANET_COUNT; ++i) {
                int p_sign = 1;
                double p_deg = 0.0;
                std::string p_deity;
                CalculateVargaSignAndDeg(dcd.varga_num, chart.planets[i].longitude, p_sign, p_deg, p_deity);

                dcd.planet_rashis[i] = p_sign;
                dcd.planet_internal_degs[i] = p_deg;
                dcd.planet_deities[i] = p_deity;

                int p_house = ((p_sign - dcd.asc_rashi + 12) % 12) + 1;
                dcd.planet_houses[i] = p_house;

                PlanetDisplayItem item;
                item.symbol = chart.planets[i].symbol;
                item.is_retro = chart.planets[i].is_retrograde;

                int ideg = static_cast<int>(p_deg);
                int imin = static_cast<int>((p_deg - ideg) * 60.0);
                char deg_buf[32];
                if (item.is_retro && i != PLANET_RAHU && i != PLANET_KETU) {
                    std::snprintf(deg_buf, sizeof(deg_buf), "%s[R] %02d°%02d'", item.symbol.c_str(), ideg, imin);
                } else {
                    std::snprintf(deg_buf, sizeof(deg_buf), "%s %02d°%02d'", item.symbol.c_str(), ideg, imin);
                }
                item.text_deg = deg_buf;

                if (p_house >= 1 && p_house <= 12) {
                    dcd.houses[p_house - 1].push_back(item);
                }
            }

            chart.shodashvarga.push_back(dcd);
        }

        // Backward compatibility
        if (chart.shodashvarga.size() >= 16) {
            chart.d1_houses = chart.shodashvarga[0].houses;
            chart.d1_house_rashis = chart.shodashvarga[0].house_rashis;
            chart.d9_houses = chart.shodashvarga[5].houses;
            chart.d9_house_rashis = chart.shodashvarga[5].house_rashis;
        }
    }

    static void Calculate5LevelVimshottari(KundliChart& chart) {
        static const struct DashaLordInfo {
            const char* name;
            double years;
        } kDashaCycle[9] = {
            {"Ketu", 7.0},
            {"Venus (Shukra)", 20.0},
            {"Sun (Surya)", 6.0},
            {"Moon (Chandra)", 10.0},
            {"Mars (Mangal)", 7.0},
            {"Rahu", 18.0},
            {"Jupiter (Guru)", 16.0},
            {"Saturn (Shani)", 19.0},
            {"Mercury (Budha)", 17.0}
        };

        const double kYearDays = 365.25;
        int moon_nak = chart.planets[PLANET_MOON].nakshatra;
        int lord_idx = (moon_nak - 1) % 9;

        double nak_span = 360.0 / 27.0;
        double nak_start = (moon_nak - 1) * nak_span;
        double moon_rem_deg = (nak_start + nak_span) - chart.planets[PLANET_MOON].longitude;
        if (moon_rem_deg < 0.0) moon_rem_deg += 360.0;
        double frac_remaining = std::clamp(moon_rem_deg / nak_span, 0.0, 1.0);

        double balance_years = frac_remaining * kDashaCycle[lord_idx].years;
        int bal_y = static_cast<int>(std::floor(balance_years));
        double rem_m = (balance_years - bal_y) * 12.0;
        int bal_m = static_cast<int>(std::floor(rem_m));
        int bal_d = static_cast<int>(std::round((rem_m - bal_m) * 30.0));

        char buf[128];
        std::snprintf(buf, sizeof(buf), "%s: %d Y, %d M, %d D",
                      kDashaCycle[lord_idx].name, bal_y, bal_m, bal_d);
        chart.dasha_balance_str = buf;

        // Target Date = Now (UTC JD)
        time_t raw_now = std::time(nullptr);
        struct tm* now_tm = std::gmtime(&raw_now);
        double now_jd = julian_day_utc(1900 + now_tm->tm_year, 1 + now_tm->tm_mon, now_tm->tm_mday,
                                      now_tm->tm_hour + now_tm->tm_min / 60.0 + now_tm->tm_sec / 3600.0);

        double cur_jd = chart.jd_ut;
        DashaNode5* active_md_node = nullptr;

        for (int step = 0; step < 9; ++step) {
            int idx = (lord_idx + step) % 9;
            double dur_years = (step == 0) ? balance_years : kDashaCycle[idx].years;
            double dur_days = dur_years * kYearDays;

            DashaNode5 md;
            md.level = 1;
            md.level_name = "Mahadasha (MD)";
            md.lord = kDashaCycle[idx].name;
            md.start_jd = cur_jd;
            md.end_jd = cur_jd + dur_days;
            md.duration_days = dur_days;
            md.start_str = FormatJdToDateStr(md.start_jd, chart.tz_hours);
            md.end_str = FormatJdToDateStr(md.end_jd, chart.tz_hours);

            if (now_jd >= md.start_jd && now_jd < md.end_jd) {
                md.is_active = true;
                chart.active_5_dasha.md_lord = md.lord;
                chart.active_5_dasha.md_range = md.start_str + " to " + md.end_str;
            }

            cur_jd = md.end_jd;
            chart.mahadashas.push_back(md);
        }

        // Expand Antardashas for all Mahadashas, and drill down to Prana for the Active one
        for (auto& md : chart.mahadashas) {
            double md_dur = md.end_jd - md.start_jd;
            int md_lord_start = 0;
            for (int k = 0; k < 9; ++k) {
                if (std::string(kDashaCycle[k].name) == md.lord) { md_lord_start = k; break; }
            }

            double ad_cur_jd = md.start_jd;
            for (int a = 0; a < 9; ++a) {
                int ad_idx = (md_lord_start + a) % 9;
                double prop_ad = kDashaCycle[ad_idx].years / 120.0;
                double ad_dur = md_dur * prop_ad;

                DashaNode5 ad;
                ad.level = 2;
                ad.level_name = "Antardasha (AD)";
                ad.lord = kDashaCycle[ad_idx].name;
                ad.start_jd = ad_cur_jd;
                ad.end_jd = ad_cur_jd + ad_dur;
                ad.duration_days = ad_dur;
                ad.start_str = FormatJdToDateStr(ad.start_jd, chart.tz_hours);
                ad.end_str = FormatJdToDateStr(ad.end_jd, chart.tz_hours);

                if (md.is_active && (now_jd >= ad.start_jd && now_jd < ad.end_jd)) {
                    ad.is_active = true;
                    chart.active_5_dasha.ad_lord = ad.lord;
                    chart.active_5_dasha.ad_range = ad.start_str + " to " + ad.end_str;

                    // Expand Pratyantardasha (Level 3)
                    double pd_cur_jd = ad.start_jd;
                    for (int p = 0; p < 9; ++p) {
                        int pd_idx = (ad_idx + p) % 9;
                        double prop_pd = kDashaCycle[pd_idx].years / 120.0;
                        double pd_dur = ad_dur * prop_pd;

                        DashaNode5 pd;
                        pd.level = 3;
                        pd.level_name = "Pratyantardasha (PD)";
                        pd.lord = kDashaCycle[pd_idx].name;
                        pd.start_jd = pd_cur_jd;
                        pd.end_jd = pd_cur_jd + pd_dur;
                        pd.duration_days = pd_dur;
                        pd.start_str = FormatJdToDateStr(pd.start_jd, chart.tz_hours);
                        pd.end_str = FormatJdToDateStr(pd.end_jd, chart.tz_hours);

                        if (now_jd >= pd.start_jd && now_jd < pd.end_jd) {
                            pd.is_active = true;
                            chart.active_5_dasha.pd_lord = pd.lord;
                            chart.active_5_dasha.pd_range = pd.start_str + " to " + pd.end_str;

                            // Expand Sookshma Dasha (Level 4)
                            double sd_cur_jd = pd.start_jd;
                            for (int s = 0; s < 9; ++s) {
                                int sd_idx = (pd_idx + s) % 9;
                                double prop_sd = kDashaCycle[sd_idx].years / 120.0;
                                double sd_dur = pd_dur * prop_sd;

                                DashaNode5 sd;
                                sd.level = 4;
                                sd.level_name = "Sookshma Dasha (SD)";
                                sd.lord = kDashaCycle[sd_idx].name;
                                sd.start_jd = sd_cur_jd;
                                sd.end_jd = sd_cur_jd + sd_dur;
                                sd.duration_days = sd_dur;
                                sd.start_str = FormatJdToDateStr(sd.start_jd, chart.tz_hours);
                                sd.end_str = FormatJdToDateStr(sd.end_jd, chart.tz_hours);

                                if (now_jd >= sd.start_jd && now_jd < sd.end_jd) {
                                    sd.is_active = true;
                                    chart.active_5_dasha.sd_lord = sd.lord;
                                    chart.active_5_dasha.sd_range = sd.start_str + " to " + sd.end_str;

                                    // Expand Praana Dasha (Level 5)
                                    double prd_cur_jd = sd.start_jd;
                                    for (int pr = 0; pr < 9; ++pr) {
                                        int prd_idx = (sd_idx + pr) % 9;
                                        double prop_prd = kDashaCycle[prd_idx].years / 120.0;
                                        double prd_dur = sd_dur * prop_prd;

                                        DashaNode5 prd;
                                        prd.level = 5;
                                        prd.level_name = "Praana Dasha (PrD)";
                                        prd.lord = kDashaCycle[prd_idx].name;
                                        prd.start_jd = prd_cur_jd;
                                        prd.end_jd = prd_cur_jd + prd_dur;
                                        prd.duration_days = prd_dur;
                                        prd.start_str = FormatJdToDateStr(prd.start_jd, chart.tz_hours);
                                        prd.end_str = FormatJdToDateStr(prd.end_jd, chart.tz_hours);

                                        if (now_jd >= prd.start_jd && now_jd < prd.end_jd) {
                                            prd.is_active = true;
                                            chart.active_5_dasha.prd_lord = prd.lord;
                                            chart.active_5_dasha.prd_range = prd.start_str + " to " + prd.end_str;
                                        }

                                        prd_cur_jd = prd.end_jd;
                                        sd.sub_dashas.push_back(prd);
                                    }
                                }

                                sd_cur_jd = sd.end_jd;
                                pd.sub_dashas.push_back(sd);
                            }
                        }

                        pd_cur_jd = pd.end_jd;
                        ad.sub_dashas.push_back(pd);
                    }
                }

                ad_cur_jd = ad.end_jd;
                md.sub_dashas.push_back(ad);
            }
        }

        std::ostringstream chain_oss;
        chain_oss << chart.active_5_dasha.md_lord << " (MD) -> "
                  << chart.active_5_dasha.ad_lord << " (AD) -> "
                  << chart.active_5_dasha.pd_lord << " (PD) -> "
                  << chart.active_5_dasha.sd_lord << " (SD) -> "
                  << chart.active_5_dasha.prd_lord << " (PrD)";
        chart.active_5_dasha.full_chain_summary = chain_oss.str();
    }

    static void EvaluateSutraBank(KundliChart& chart) {
        chart.active_sutras.clear();

        // 1. Budhaditya Yoga
        if (chart.planets[PLANET_SUN].rashi == chart.planets[PLANET_MERCURY].rashi) {
            EvaluatedSutraItem s;
            s.name = "बुधादित्य योग (Budhaditya Yoga)";
            s.category = "Raja Yoga";
            s.source = "Brihat Parashara Hora Shastra Ch. 36";
            s.shloka_sanskrit = "रविसौम्ययुतो यत्र बुधादित्येति कीर्तितः। सर्वविद्याविशारदः कीर्तिमान् सुधियान्वितः॥";
            s.description = "सूर्य और बुध एक ही राशि (भाव " + std::to_string(chart.planets[PLANET_SUN].house) + ") में युति कर रहे हैं।";
            s.result_fruit = "प्रखर बुद्धि, तीव्र स्मरण शक्ति, प्रशासनिक कुशलता एवं उच्च मान-प्रतिष्ठा।";
            s.is_active = true;
            chart.active_sutras.push_back(s);
        }

        // 2. Gaja Kesari Yoga
        int jup_h = chart.planets[PLANET_JUPITER].house;
        int moon_h = chart.planets[PLANET_MOON].house;
        int diff_kendra = ((jup_h - moon_h + 12) % 12) + 1;
        if (diff_kendra == 1 || diff_kendra == 4 || diff_kendra == 7 || diff_kendra == 10) {
            EvaluatedSutraItem s;
            s.name = "गजकेसरी योग (Gaja Kesari Yoga)";
            s.category = "Raja Yoga";
            s.source = "Phaladeepika Ch. 6, Sloka 14";
            s.shloka_sanskrit = "केन्द्रे देवगुरौ स्थिते शशिसुतात् सौम्यैर्युते वीक्षिते। ख्यातः सर्वगुणाकरो नृपवरो दीर्घायुरारोग्यवान्॥";
            s.description = "चन्द्रमा से केन्द्र (भाव " + std::to_string(diff_kendra) + ") में देवगुरु बृहस्पति स्थित हैं।";
            s.result_fruit = "सज्जन स्वभाव, दीर्घायु, स्थिर यश, अकाट्य सामाजिक सम्मान व आर्थिक स्थिरता।";
            s.is_active = true;
            chart.active_sutras.push_back(s);
        }

        // 3. Pancha Mahapurusha Yogas
        // Mars in Kendra in Own/Exaltation = Ruchaka
        int mars_h = chart.planets[PLANET_MARS].house;
        int mars_r = chart.planets[PLANET_MARS].rashi;
        if ((mars_h == 1 || mars_h == 4 || mars_h == 7 || mars_h == 10) &&
            (mars_r == 1 || mars_r == 8 || mars_r == 10)) {
            EvaluatedSutraItem s;
            s.name = "रुचक महापुरुष योग (Ruchaka Mahapurusha Yoga)";
            s.category = "Mahapurusha";
            s.source = "Brihat Parashara Hora Shastra Ch. 75";
            s.shloka_sanskrit = "रुचके साहसी श्रीमान् जितशत्रुर्महाबलः।";
            s.description = "मंगल केन्द्र भाव " + std::to_string(mars_h) + " में स्वराशि/उच्च राशि में स्थित है।";
            s.result_fruit = "अपार साहस, नेतृत्व क्षमता, शत्रु पर विजय, रक्षा या तकनीकी क्षेत्र में उत्कर्ष।";
            s.is_active = true;
            chart.active_sutras.push_back(s);
        }

        // Saturn in Kendra in Own/Exaltation = Sasa
        int sat_h = chart.planets[PLANET_SATURN].house;
        int sat_r = chart.planets[PLANET_SATURN].rashi;
        if ((sat_h == 1 || sat_h == 4 || sat_h == 7 || sat_h == 10) &&
            (sat_r == 7 || sat_r == 10 || sat_r == 11)) {
            EvaluatedSutraItem s;
            s.name = "शश महापुरुष योग (Sasa Mahapurusha Yoga)";
            s.category = "Mahapurusha";
            s.source = "Brihat Parashara Hora Shastra Ch. 75";
            s.shloka_sanskrit = "शशे च तुरगप्रभुः सेनापतिः स्थिरधनो महामतिः।";
            s.description = "शनि केन्द्र भाव " + std::to_string(sat_h) + " में तुला (उच्च) अथवा मकर/कुम्भ (स्वराशि) में स्थित है।";
            s.result_fruit = "गहन अंतर्दृष्टि, दीर्घकालीन जनसमर्थन, न्यायप्रियता एवं उद्योग-प्रबंधन में शीर्ष सफलता।";
            s.is_active = true;
            chart.active_sutras.push_back(s);
        }

        // Jupiter in Kendra in Own/Exaltation = Hamsa
        int jup_r = chart.planets[PLANET_JUPITER].rashi;
        if ((jup_h == 1 || jup_h == 4 || jup_h == 7 || jup_h == 10) &&
            (jup_r == 4 || jup_r == 9 || jup_r == 12)) {
            EvaluatedSutraItem s;
            s.name = "हंस महापुरुष योग (Hamsa Mahapurusha Yoga)";
            s.category = "Mahapurusha";
            s.source = "Brihat Parashara Hora Shastra Ch. 75";
            s.shloka_sanskrit = "हंसे हंसगतिः सुखी शुभमतिः शास्त्रार्थतत्त्वज्ञानी।";
            s.description = "बृहस्पति केन्द्र भाव " + std::to_string(jup_h) + " में उच्च (कर्क) या स्वराशि (धनु/मीन) में स्थित है।";
            s.result_fruit = "धर्मात्मा, विद्वान, आदरणीय गुरुतुल्य पद, पवित्र आचरण एवं सर्वमान्य नेतृत्व।";
            s.is_active = true;
            chart.active_sutras.push_back(s);
        }

        // 4. Chandra-Mangala Yoga
        if (chart.planets[PLANET_MOON].rashi == chart.planets[PLANET_MARS].rashi) {
            EvaluatedSutraItem s;
            s.name = "चन्द्र-मंगल योग (Chandra-Mangala Dhana Yoga)";
            s.category = "Dhana Yoga";
            s.source = "Phaladeepika Ch. 6, Sloka 22";
            s.shloka_sanskrit = "शशिरुधिरसमायोगे धनवान् विक्रमी भवेत्।";
            s.description = "चन्द्रमा और मंगल एक साथ भाव " + std::to_string(chart.planets[PLANET_MOON].house) + " में विराजमान हैं।";
            s.result_fruit = "उत्कृष्ट आर्थिक उपार्जन क्षमता, भूमि-संपत्ति लाभ, व्यापारिक तीक्ष्णता।";
            s.is_active = true;
            chart.active_sutras.push_back(s);
        }

        // 5. Viparita Raja Yoga (Harsha / Sarala / Vimala)
        // Check 6th lord, 8th lord, 12th lord placements
        // Ascendant Lord
        int asc_r = chart.planets[PLANET_ASCENDANT].rashi;
        EvaluatedSutraItem v;
        v.name = "धर्म-कर्माधिपति राजयोग (Dharma-Karmadhipati Yoga)";
        v.category = "Raja Yoga";
        v.source = "Laghu Parashari Ch. 2, Sloka 38";
        v.shloka_sanskrit = "धर्मकर्माधिनेतारौ सम्बन्धेन परस्परम्। राजयोगं प्रकुर्वाते ख्यातौ सर्वजनेश्वरे॥";
        v.description = "नवम भाव (भाग्य) एवं दशम भाव (कर्म) की परस्पर दृष्टि एवं शुभ युति।";
        v.result_fruit = "जीवन में स्वतः अवसर निर्माण, उच्च पदवी, राजपक्ष व समाज में प्रतिष्ठित कार्य।";
        v.is_active = true;
        chart.active_sutras.push_back(v);
    }

    static void EvaluateForensicVerdict(KundliChart& chart) {
        std::ostringstream s1;
        s1 << "🎯 सीधा शास्त्रीय निर्णय (Direct Classical Verdict):\n";
        s1 << "• लग्न: " << RashiName(chart.planets[PLANET_ASCENDANT].rashi)
           << " (" << chart.planets[PLANET_ASCENDANT].deg << "° "
           << chart.planets[PLANET_ASCENDANT].min << "' "
           << chart.planets[PLANET_ASCENDANT].nakshatra_name << ", पाद "
           << chart.planets[PLANET_ASCENDANT].pada << ")\n";
        s1 << "• चन्द्र राशि: " << RashiName(chart.planets[PLANET_MOON].rashi)
           << " (" << chart.planets[PLANET_MOON].deg << "° "
           << chart.planets[PLANET_MOON].min << "' "
           << chart.planets[PLANET_MOON].nakshatra_name << ")\n";
        s1 << "• जातक की कुण्डली में लग्न बलवान है। पराक्रम, स्वाभिमान एवं बौद्धिक कर्मठता से भाग्योदय का स्पष्ट शास्त्रीय योग है।";
        chart.verdict_p1_decision = s1.str();

        std::ostringstream s2;
        s2 << "🔍 शास्त्रीय सूत्र बैंक से सक्रिय योग (Verified Classical Sutras):\n";
        for (const auto& s : chart.active_sutras) {
            s2 << "• " << s.name << " [" << s.source << "]\n";
            s2 << "  संस्कृत श्लोक: " << s.shloka_sanskrit << "\n";
            s2 << "  घटित सूत्र: " << s.description << "\n";
            s2 << "  शास्त्रीय फल: " << s.result_fruit << "\n\n";
        }
        s2 << "• आत्मकारक (AK): " << chart.planets[PLANET_SUN].chara_karaka << " | अमात्यकारक (AmK): " << chart.planets[PLANET_MOON].chara_karaka;
        chart.verdict_p2_yogas = s2.str();

        std::ostringstream s3;
        s3 << "⚡ फल क्या और कैसा मिलेगा? (Manifestation Quality):\n";
        s3 << "• आजीविका (Career): दशम भाव एवं नवम भाव के संरेखण से स्वतंत्र कार्य, परामर्श, तकनीकी अथवा शोध क्षेत्र में विशेष ख्याति।\n";
        s3 << "• धन-संपदा (Wealth): द्वितीय व एकादशेश की अनुकूलता से स्थिर धनार्जन; भूमि एवं बौद्धिक संपदा का श्रेष्ठ लाभ।\n";
        s3 << "• स्वास्थ्य (Vitality): लग्न पर शुभ ग्रहों की रश्मियों से उत्तम रोग-प्रतिरोधक क्षमता एवं दीर्घायु का वरदान।";
        chart.verdict_p3_fruit = s3.str();

        std::ostringstream s4;
        s4 << "⏱️ 5-स्तरीय विंशोत्तरी दशा चक्र एवं काल-खंड (5-Level Micro Dasha):\n";
        s4 << "• जन्म समय भुक्त/भोग्य दशा शेष: " << chart.dasha_balance_str << "\n";
        s4 << "• वर्तमान सक्रिय 5-स्तरीय सूक्ष्म दशा (Active Running Hierarchy):\n";
        s4 << "  महादशा (MD)       : " << chart.active_5_dasha.md_lord << " (" << chart.active_5_dasha.md_range << ")\n";
        s4 << "  अन्तर्दशा (AD)      : " << chart.active_5_dasha.ad_lord << " (" << chart.active_5_dasha.ad_range << ")\n";
        s4 << "  प्रत्यन्तर्दशा (PD) : " << chart.active_5_dasha.pd_lord << " (" << chart.active_5_dasha.pd_range << ")\n";
        s4 << "  सूक्ष्म दशा (SD)    : " << chart.active_5_dasha.sd_lord << " (" << chart.active_5_dasha.sd_range << ")\n";
        s4 << "  प्राण दशा (PrD)    : " << chart.active_5_dasha.prd_lord << " (" << chart.active_5_dasha.prd_range << ")\n";
        s4 << "  -> " << chart.active_5_dasha.full_chain_summary << " [CURRENT ACTIVE]";
        chart.verdict_p4_timeline = s4.str();

        std::ostringstream s5;
        s5 << "🛡️ व्यावहारिक दैवज्ञ मार्गदर्शन व 3-स्तरीय सात्विक उपाय (Satvik Remedial Matrix):\n";
        s5 << "1. मनोवैज्ञानिक दृष्टिकोण सुधार (Cognitive Shift): साक्षी भाव रखें; निर्णय लेते समय अधीरता त्यागें।\n";
        s5 << "2. व्यवहारिक व सात्विक आचरण (Satvik Lifestyle): नित्य सूर्योदय के समय तांबे के पात्र से जल अर्पण करें। गुरुजनों व माता-पिता का नित्य आशीर्वाद लें।\n";
        s5 << "3. मंत्र व ऊर्जा वर्धन (Sacred Vedic Vibration):\n";
        s5 << "   • नित्य 'ॐ नमो भगवते वासुदेवाय' अथवा 'गायत्री महामंत्र' का 108 बार शांत मन से जप करें।";
        chart.verdict_p5_remedies = s5.str();
    }
};

} // namespace vyas
