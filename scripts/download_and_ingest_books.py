# -*- coding: utf-8 -*-
"""
scripts/download_and_ingest_books.py
Downloads books specified by user and prepares ingestion pipeline.
"""
import os
import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

TARGET_DIR = r"G:\software\simpa\VYAS\books"
os.makedirs(TARGET_DIR, exist_ok=True)

URLS = [
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/16250879-the-art-of-astrology-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/16446933-seven-aspects-of-life-or-saptavarga-phala-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/16489503-a-complete-guide-to-palmistry-by-psychos-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/22637446-reincarnation-and-the-law-of-karma-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/33202687-daivagna-kamadhenu.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/33494212-the-astrologer-s-apprentice-issue-2.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/33495006-the-astrologer-s-apprentice-issue-3.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/33496667-the-astrologer-s-apprentice-issue-4-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/43326993-simplified-scientific-astrology-a-complete-textbook-on-the-art-of-erecting-a-horoscope-with-philosophic-encyclopedia-and-tables-of-planetary-hours.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/44291202-lal-kitab-edited-part-ii.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/46045723-prasna-application-by-v-k-choudry.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/46045951-predictions-through-horary-by-dr-s-c-kursija.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/62910471-john-cox-mark-rubinstein-1985-options-markets.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jaimini_astrology.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_a-glimpse-of-kerala-astrology.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_a-manual-of-jamini-astrology.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_a-text-book-of-astrology_basis.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_advanced-medical-astrology_chatterjee-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_advanced-study-of-vimshottari-dasha_kk-pathak.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_advanced-techniques-of-astrological-predictions.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_aifas_prediction-through-dasha-yogini.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_aifas_saral-ashtak-varg-siddhant.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_aifas_timing-of-events-through-dasha-and-transit.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_an-analysis-of-longevity_aifas.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_an-insight-into-kuja-dosha_trivedi.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_analysis-of-marriage-through-astrology_basistha-tiwari-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_anga-vidya_varahamihira.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_annual-horoscope_varshaphala_m-s-mehta.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_arudha-system-of-prediction_c-s-patel.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_ashtakavarga_c-s-patel.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_ashtakavarga_m-s-mehta.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_astro-sutras_j-n-bhasin.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_astrolocality-astrology_martin-davis.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_astrology-and-diagnosis_sg-khot.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_astrology-and-the-hoax-of-scientific-temper_gayatri-devi.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_astrology-and-timing-of-marriage_-k-n-rao_-english_hindi.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_astrology-in-marriage-counselling_manik-chand-jain.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_basic-lessons-on-indian-astrology.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_best-way-to-use-shad-bala_k-jaya-sekhar.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_bhrigu-on-predictive-astrology_-kk-pathak-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_bhrigu-samhita_shanker-adawal-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_bhrigu-samhita_t-m-rao-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_bhrigu-sutram_shankar-kapoor-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_bhrigu-sutras_retyped-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_bhrigu-sutras_verses-only-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_birth-chart_mathematics-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_brighu-naadi-sangraha_srinivasan-shastry-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_brighu-prashna-nadi_rg-rao-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_brihat-samhita_m-r-bhat_part-1-of-2_1981.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_brihat-samhita_m-r-bhat_part-2-of-2_1981.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_brihat-samhita_p-s-sastri-vol-1-2_full_1946.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_collected-papers-in-vedic-astrology_-s-rath.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_commentary-on-sapta-rishi-nadi-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_daivajna-vallabha_prasna_varaha-mihira_retypedaaa-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_dasha-nirnay-e28093-vimsottari-dasha_kn-rao_-z-anzari-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_delayed-marriage-of-girls_-kn-rao-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_eastern-astrology-for-western-minds_joni-patry-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_electional-astrology_arun-kumar-bansal-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_elements-of-astronomy_v-p-jain-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_elements-of-vedic-astrology_k-s-charak-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_encyclopedia-of-astrological-remedies_arun-kumar-bansal-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_esoteric-principles-of-vedic-astrology-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_essentials-of-medical-astrology_k-s-charak-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_essentials-of-predictive-hindu-astrology_r-santhanam-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_explore-the-power-of-astrology_dr-a-p-parasara-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_explore-the-power-of-astrology_trikona-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_forecasting-prices_t-g-butaney-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_foretelling-widowhood_trivedi-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_four-trines-in-vedic-astrology-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_from-here-to-there_astromapping_martin-davis-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_fundamentals-of-astrology_m-ramakrishna-bhat-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_jyotish-manthan_shah_-anil-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/roots-of-nadi-astrology.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/bhrigu-nandi-nadi.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/prediction-secrets-naadi-astrology.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/core-of-nadi-astrology.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/c-s-_patel_-_nadi_astrology.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/naadi-maga-secret.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/naadi-research.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/practical-naadi.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/prt-appln-naadi.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/r-gopalakrishna-row-meena-nadi-jyothisha-or-the-stellar-system-of-astrology-3-vols.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/revelation-from-naadi-jyotisha.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/roots-of-nadi.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/orbital-providence-nadi.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/essence-of-nadi-r-g-rao.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/secrets-of-nadi-astrology.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish_fundamentals-of-raos-system-of-nadi-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/house-grouping-kp-astrology.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jyotish-kp-the-times-horary-astrology.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/kp-astrology-basics.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/k-p-basics-of-nakshatra-padhathi.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/k-p-dynamics.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/k-p-muhurat.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/kp-new-dimensions-of-kp-astro.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/k-p-progeny-romance.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/how-to-judge-longevity.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/01-casting-the-horoscope-1-fount-bad-quality.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/02-fundamental-principles-of-astrology-2-kp-system-by-prof-k-s-krishnamurty.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/03-predictive-stellar-astrology-3-kp-system-by-prof-k-s-krishnamurty-good-quality.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/04-jyotish-kp-reader-4-marriage-married-life-children.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/05-kp-reader-5-transits.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/0-1-naksatra-cintamani.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/0-2-further-lights-on-nak-chintamani.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jataka-parijata-vol-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jataka-parijata-vol-2.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/jataka-parijata-vol-3.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/raman-how-to-judge-horoscope-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/raman-how-to-judge-horoscope-2.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/hindu-predictive-astrology-bv-raman.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/planetary-influences-on-human-affairs-by-bv-raman.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/prasna-marga-1.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/prasna-marga-2.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/127930441-studies-in-jaimini-astrology-by-b-v-raman.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/my-exp-b-v-raman.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/muhurtha-jyotish-vedic-astrology.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/prashna-tantra-jyotish-vedic-astrology.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/key-to-learn-k-p-cuspal-system.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/kp-kalamsa-and-cuspal-interlinks.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/kp-true-astrology.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/astrology-destiny-and-the-wheel-of-time.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/finer-techniques-of-astrological-predictions.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/karma-rebirth-in-astrology.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/kn-rao-s-astrology-lessons.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/learn-hindu-astrology-easily.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/predicting-through-jaimini-chara-dasha.pdf",
    "https://astrofoxx.wordpress.com/wp-content/uploads/2018/11/yogis-destiny-and-the-wheel-of-time-k-n-rao.pdf"
]

def download_file(url):
    fname = os.path.basename(url)
    dest_path = os.path.join(TARGET_DIR, fname)
    
    # Check if exists and valid (>1000 bytes and starts with %PDF)
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        try:
            with open(dest_path, "rb") as fp:
                head = fp.read(4)
                if head == b"%PDF":
                    return fname, "ALREADY_EXISTS", os.path.getsize(dest_path)
        except Exception:
            pass

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://astrofoxx.wordpress.com/"
    }
    
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                if len(data) > 500:
                    with open(dest_path, "wb") as out:
                        out.write(data)
                    return fname, "DOWNLOADED", len(data)
                else:
                    return fname, "EMPTY_DATA", len(data)
        except Exception as e:
            if attempt == 2:
                return fname, f"FAILED: {str(e)[:50]}", 0
            time.sleep(1.5)

def main():
    print(f"Total books to process: {len(URLS)}")
    results = {"ALREADY_EXISTS": 0, "DOWNLOADED": 0, "FAILED": 0}
    
    # Use 6 threads for courteous concurrent download
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(download_file, url): url for url in URLS}
        for future in as_completed(futures):
            fname, status, size = future.result()
            if status == "ALREADY_EXISTS":
                results["ALREADY_EXISTS"] += 1
                print(f"[EXISTS] {fname} ({size//1024} KB)")
            elif status == "DOWNLOADED":
                results["DOWNLOADED"] += 1
                print(f"[DOWNLOADED] {fname} ({size//1024} KB)")
            else:
                results["FAILED"] += 1
                print(f"[ERR] {fname}: {status}")

    print("\n=== DOWNLOAD SUMMARY ===")
    print(f"Already exists: {results['ALREADY_EXISTS']}")
    print(f"Newly downloaded: {results['DOWNLOADED']}")
    print(f"Failed: {results['FAILED']}")
    print(f"Total: {len(URLS)}")

if __name__ == "__main__":
    main()

