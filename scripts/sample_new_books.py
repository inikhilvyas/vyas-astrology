import glob
import os

new_md_books = glob.glob('books/*.md')
print(f"Total md files in books: {len(new_md_books)}")
interesting = [
    'books/0_Astrology-Yogas-Collection-_Hindi-Version__0B8PLpDKw1NhKYllJVEtWSmJFNGs.md',
    'books/0_Bhartiya_Jyotish_Vigyan_ह_द_म_ज_य_त_स_क_प_र_म_भ_क_ज_ञ_न_-उत_त_तम_क_त_ब__0B8PLpDKw1NhKRVZ5ZFI5cTdlbms.md',
    'books/0_Jyotish-Swayam-Shikshak-Fal-Jyotish-in-HINDI__0B8PLpDKw1NhKbExYWFd5NXZhS0U.md',
    'books/0_Jyotish_dwara_rog_upachar_ज_य_त_ष_द_व_र_र_ग_उपच_र__0B8PLpDKw1NhKMnRid3ZNV3ZueXM.md',
    'books/0_Jyotisha_Ratnakar_सभ_तथ_य_-स_खन_क_ल_ए_उत_तम__0B8PLpDKw1NhKSTJvMFhJRVVmZTA.md',
    'books/0_Kalyana_Varma_saravali__0B8PLpDKw1NhKRzZtRk1mUlpUZGs.md',
    'books/0_Ratna-Upratna-Nag-Nagina-Sampurna-Gyan-001749__0B8PLpDKw1NhKRi1jUnk0eERXSzg.md',
    'books/0_ज_य_त_ष-रत_न_कर__0B8PLpDKw1NhKQVdfS1JhSnM4RHM.md',
    'books/Bhartiya_jyotish_vigyan__0B8PLpDKw1NhKX25BZDRVdEUyOFk.md',
    'books/Bhrigu_Sutras-Planetsin_12_Houses_-vasant__0B8PLpDKw1NhKQWowY0tCbHlZcTA.md',
    'books/Brhatparasarahorasastra_JYOTISH_VEDIC_ASTROLOGY__0B8PLpDKw1NhKNWNIMmlGc2hkak0.md',
    'books/Sachitra-Jyotish-Shiksha-4_-_Varshfhal_Khand__0B8PLpDKw1NhKVzZ2QVRYLTY0STQ.md',
    'books/Sachitra-jyotish-shiksha-2_1_-_Ganit_Khand__0B8PLpDKw1NhKQy1hVkJZQjFXQUE.md',
    'books/Sachitra-jyotish-shiksha-2_2_-_Ganit_Khand__0B8PLpDKw1NhKUGs5M19mVE1FWUU.md',
    'books/Sachitra-jyotish-shiksha-6_-_Muharat_Khand__0B8PLpDKw1NhKem9ZZzlVTmNENGc.md',
    'books/Sachitra-jyotish-shiksha-8_-_Sanhita_Khand__0B8PLpDKw1NhKLTZFd1V4aTVzc2c.md',
    'books/Saral_Jyotish__0B8PLpDKw1NhKS2d5b0ZCa3lucWs.md',
    'books/Satya_Jataka_JYOTISH_VEDIC_ASTROLOGY-vasant__0B8PLpDKw1NhKTG0ySTB3bExJVW8.md',
    'books/vasant-Bhavartha_Ratnakara_JYOTISH_VEDIC_ASTROLOGY__0B8PLpDKw1NhKQ3ZTNWg4WkpMdmc.md',
    'books/vasant-Bhrigu_Sutras_JYOTISH_VEDIC_ASTROLOGY__0B8PLpDKw1NhKTXNMdU5UWE8wUXM.md',
    'books/vasant-Garga_Hora_JYOTISH_VEDIC_ASTROLOGY__0B8PLpDKw1NhKQ0I4Y2JNYkNxcWs.md',
    'books/vasant-Horasara_of_Prithuyasas_-VISMOTTARI_DASA__0B8PLpDKw1NhKMFVVSTNOenFfWm8.md',
    'books/vasant-Prashna_Tantra_JYOTISH_VEDIC_ASTROLOGY__0B8PLpDKw1NhKQzB5WU52X3FmNHM.md',
    'books/vasant-STRI_JATAKA_JYOTISH_VEDIC_ASTROLOGY__0B8PLpDKw1NhKOWZxRmJSaUIwTWM.md',
    'books/vasant-THE_YAVANAJATAKA_OF_SPHUJIDHVAJA_JYOTISH_VEDIC_ASTROLOGY__0B8PLpDKw1NhKTVBrR3hQcml1NWs.md'
]
print("Interesting classical books count:", len(interesting))
for b in interesting[:5]:
    if os.path.exists(b):
        with open(b, 'r', encoding='utf-8', errors='ignore') as fl:
            first_lines = fl.read(300)
            print(f"\n--- {os.path.basename(b)} ---")
            print(first_lines.strip())

