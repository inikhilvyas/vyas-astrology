import json
from generate_kundli_pdf import build_pdf_dossier

sample_data = {
    'native_name': 'Nikhil Vyas',
    'year': 1984, 'month': 11, 'day': 23,
    'hour': 16, 'minute': 45, 'second': 0,
    'location_name': 'Pali, Rajasthan, India',
    'latitude': 25.7711, 'longitude': 73.3234, 'tz_hours': 5.5,
    'ayanamsa': 23.6401,
    'lagna_rashi_num': 1, 'lagna_rashi_name': 'मेष (Aries)',
    'moon_rashi_name': 'वृश्चिक (Scorpio)',
    'birth_nakshatra': 'अनुराधा (Anuradha Pada-4)',
    'navamsha_lagna_num': 8,
    'd1_house_planets': {1: ['Asc 21°32\''], 2: ['Ra 03°33\''], 7: ['Sa 26°53\''], 8: ['Su 07°42\'', 'Mo 14°35\'', 'Me 29°15\'', 'Ke 03°33\''], 9: ['Ju 19°21\'', 'Ve 17°44\''], 10: ['Ma 12°09\'']},
    'd9_house_planets': {7: ['Asc 13°54\''], 8: ['Mo 11°19\''], 6: ['Su 09°24\'', 'Ju 24°10\'', 'Ve 09°38\'', 'Ke 01°58\''], 12: ['Me 23°17\''], 1: ['Ma 19°23\''], 2: ['Sa 01°57\''], 11: ['Ra 01°58\'']},
    'planets_table': [
        {'name': 'Surya (सूर्य)', 'degree': '7° 42\' 40"', 'rashi': 'Scorpio', 'house': 8, 'nakshatra': 'Anuradha (P-2)', 'lord': 'Saturn', 'awastha': 'वृद्ध अवस्था', 'dignity': 'Friendly (मित्र)', 'karaka': 'DK'},
        {'name': 'Chandra (चन्द्र)', 'degree': '14° 35\' 31"', 'rashi': 'Scorpio', 'house': 8, 'nakshatra': 'Anuradha (P-4)', 'lord': 'Saturn', 'awastha': 'युवा अवस्था', 'dignity': 'Debilitated [नीच]', 'karaka': 'PK'},
        {'name': 'Mangala (मंगल)', 'degree': '12° 09\' 17"', 'rashi': 'Capricorn', 'house': 10, 'nakshatra': 'Shravana (P-1)', 'lord': 'Moon', 'awastha': 'युवा अवस्था', 'dignity': 'Exalted (उच्च)', 'karaka': 'GK'},
        {'name': 'Budha (बुध)', 'degree': '29° 15\' 17"', 'rashi': 'Scorpio', 'house': 8, 'nakshatra': 'Jyeshtha (P-4)', 'lord': 'Mercury', 'awastha': 'बाल अवस्था', 'dignity': 'Normal', 'karaka': 'AK'},
        {'name': 'Guru (गुरु)', 'degree': '19° 21\' 11"', 'rashi': 'Sagittarius', 'house': 9, 'nakshatra': 'P. Ashadha (P-2)', 'lord': 'Venus', 'awastha': 'वृद्ध अवस्था', 'dignity': 'Own Sign (स्वराशि)', 'karaka': 'BK'},
        {'name': 'Shukra (शुक्र)', 'degree': '17° 44\' 15"', 'rashi': 'Sagittarius', 'house': 9, 'nakshatra': 'P. Ashadha (P-2)', 'lord': 'Venus', 'awastha': 'युवा अवस्था', 'dignity': 'Friendly (मित्र)', 'karaka': 'MK'},
        {'name': 'Shani (शनि)', 'degree': '26° 53\' 00"', 'rashi': 'Libra', 'house': 7, 'nakshatra': 'Vishakha (P-3)', 'lord': 'Jupiter', 'awastha': 'मृत अवस्था', 'dignity': 'Exalted [अस्त]', 'karaka': 'AmK'},
        {'name': 'Rahu (राहु)', 'degree': '3° 33\' 07"', 'rashi': 'Taurus', 'house': 2, 'nakshatra': 'Krittika (P-3)', 'lord': 'Sun', 'awastha': 'मृत अवस्था', 'dignity': 'Exalted (उच्च)', 'karaka': 'Shadow'},
        {'name': 'Ketu (केतु)', 'degree': '3° 33\' 07"', 'rashi': 'Scorpio', 'house': 8, 'nakshatra': 'Anuradha (P-1)', 'lord': 'Saturn', 'awastha': 'मृत अवस्था', 'dignity': 'Exalted (उच्च)', 'karaka': 'Moksha'},
        {'name': 'Lagna (लग्न)', 'degree': '21° 40\' 23"', 'rashi': 'Aries', 'house': 1, 'nakshatra': 'Bharani (P-3)', 'lord': 'Venus', 'awastha': 'वृद्ध अवस्था', 'dignity': 'Ascendant', 'karaka': 'Self'}
    ],
    'panchang': {'tithi': 'प्रतिपदा (शुक्ल पक्ष)', 'vaar': 'शुक्रवार (Friday)', 'nakshatra': 'अनुराधा (चरण 4)', 'yoga': 'सुकर्मा', 'karana': 'बव', 'sunrise': '06:48 AM', 'sunset': '05:42 PM'},
    'avakhada': {'varna': 'Brahmin', 'vashya': 'Keet', 'yoni': 'Mrig', 'gana': 'Deva', 'nadi': 'Madhya', 'tattva': 'Jal (जल)'},
    'muhurtas': {'abhijit': '11:46 AM से 12:32 PM', 'brahma': '05:08 AM से 05:58 AM', 'rahu_kaal': '10:30 AM से 12:00 PM', 'yamaganda': '09:30 AM से 11:00 AM'},
    'ashtakavarga_rows': [
        ['सूर्य', 3, 3, 3, 4, 4, 4, 6, 4, 4, 5, 5, 3, 48],
        ['चन्द्र', 4, 3, 4, 6, 4, 3, 5, 4, 4, 4, 4, 4, 49],
        ['मंगल', 3, 3, 2, 4, 3, 3, 4, 3, 3, 5, 4, 2, 39],
        ['बुध', 5, 4, 4, 5, 4, 4, 5, 4, 5, 5, 5, 4, 54],
        ['गुरु', 5, 6, 5, 4, 5, 5, 4, 5, 4, 6, 4, 3, 56],
        ['शुक्र', 4, 4, 5, 4, 5, 4, 4, 5, 4, 4, 5, 4, 52],
        ['शनि', 2, 3, 2, 4, 2, 3, 3, 3, 3, 5, 5, 4, 39],
        ['SAV', 26, 26, 25, 31, 27, 26, 31, 28, 27, 34, 32, 24, 337]
    ],
    'kp_cusps_table': [
        [1, '21° 40\' 23"', 'Mesha', 'Mars', 'Venus', 'Jupiter', 'Saturn'],
        [2, '23° 10\' 12"', 'Vrishabha', 'Venus', 'Moon', 'Sun', 'Mars'],
        [3, '20° 05\' 44"', 'Mithuna', 'Mercury', 'Jupiter', 'Jupiter', 'Venus'],
        [4, '16° 45\' 02"', 'Karka', 'Moon', 'Saturn', 'Jupiter', 'Rahu'],
        [5, '15° 22\' 19"', 'Simha', 'Sun', 'Venus', 'Sun', 'Ketu'],
        [6, '18° 35\' 51"', 'Kanya', 'Mercury', 'Moon', 'Mercury', 'Venus'],
        [7, '21° 40\' 23"', 'Tula', 'Venus', 'Jupiter', 'Saturn', 'Mars'],
        [8, '23° 10\' 12"', 'Vrischika', 'Mars', 'Mercury', 'Moon', 'Sun'],
        [9, '20° 05\' 44"', 'Dhanu', 'Jupiter', 'Venus', 'Venus', 'Mercury'],
        [10, '16° 45\' 02"', 'Makara', 'Saturn', 'Moon', 'Saturn', 'Jupiter'],
        [11, '15° 22\' 19"', 'Kumbha', 'Saturn', 'Rahu', 'Rahu', 'Venus'],
        [12, '18° 35\' 51"', 'Meena', 'Jupiter', 'Mercury', 'Ketu', 'Sun']
    ],
    'jaimini_info': {'ak': 'बुध (Mercury) - 29°15\'', 'amk': 'शनि (Saturn) - 26°53\'', 'bk': 'गुरु (Jupiter) - 19°21\'', 'mk': 'शुक्र (Venus) - 17°44\'', 'al': 'कर्क (Cancer)', 'ul': 'वृषभ (Taurus)', 'kl': 'धनु (Sagittarius)'},
    'dasha_info': {
        'running_dasha_full': 'महादशा: शुक्र (Venus) > अन्तर्दशा: गुरु (Jupiter) > प्रत्यन्तर: शनि (Saturn) > सूक्ष्म: बुध (Mercury) > प्राण दशा: केतु (Ketu)',
        'birth_balance': 'जन्म के समय विंशोत्तरी शेष: शनि (Saturn) - 3 वर्ष 0 माह 2 दिन',
        'lifetime_rows': [
            {'lord': 'शनि (Saturn)', 'years': 19, 'start': '1984-11-23', 'end': '1987-11-25', 'summary': 'आरम्भिक बाल्यकाल, संघर्ष उपरान्त सुरक्षा', 'active': False},
            {'lord': 'बुध (Mercury)', 'years': 17, 'start': '1987-11-25', 'end': '2004-11-25', 'summary': 'शिक्षा, विद्या लाभ, वाणी व बुद्धिमत्ता विकास', 'active': False},
            {'lord': 'केतु (Ketu)', 'years': 7, 'start': '2004-11-25', 'end': '2011-11-25', 'summary': 'अध्यात्म, आन्तरिक शोध व जीवन दिशा परिवर्तन', 'active': False},
            {'lord': 'शुक्र (Venus)', 'years': 20, 'start': '2011-11-25', 'end': '2031-11-25', 'summary': 'सर्वश्रेष्ठ काल, धन, यश, प्रतिष्ठा एवं विद्या प्रसार', 'active': True},
            {'lord': 'सूर्य (Sun)', 'years': 6, 'start': '2031-11-25', 'end': '2037-11-25', 'summary': 'प्रशासनिक प्रभाव, मान-सम्मान एवं राजकीय प्रतिष्ठा', 'active': False},
            {'lord': 'चन्द्र (Moon)', 'years': 10, 'start': '2037-11-25', 'end': '2047-11-25', 'summary': 'मानसिक शांति, समाज कल्याण एवं आध्यात्मिक साधना', 'active': False}
        ]
    },
    'verdict_text': '🎯 सीधा शास्त्रीय निर्णय: जातक की कुण्डली में लग्न मेष व लग्नेश मंगल दशम भाव में उच्च का होकर रुचक महापुरुष राजयोग निर्मित कर रहा है।\n🔍 नवम भाव में स्वगृही गुरु एवं भाग्येश का संरेखण जातक को प्रखर बुद्धि, उच्च ज्योतिष ज्ञान एवं न्यायप्रिय प्रशासनिक क्षमता प्रदान करता है।\n⚡ फल क्या और कैसा मिलेगा: आजीविका में स्वतंत्र परामर्श, संस्थागत नेतृत्व एवं बौद्धिक प्रतिष्ठा प्राप्त होगी।\n⏱️ काल-खंड: शुक्र महादशा अंतर्गत गुरु अन्तर्दशा में विशेष उत्कर्ष एवं यश लाभ सुनिश्चित है।',
    'remedy_t1': 'दशम भाव में उच्च के मंगल की ऊर्जा को अनुशासित शोध एवं लोक कल्याण में लगाएं। ईगो से बचें।',
    'remedy_t2': 'नित्य प्रातः सूर्य नमस्कार एवं गायत्री महामंत्र का 24 बार मानसिक जप करें। पक्षियों को जल दें।',
    'remedy_t3': 'वैदिक बीज मंत्र: ॐ क्रां क्रीं क्रौं सः भौमाय नमः। मंगलवार को लाल मसूर व तांबे का दान करें।'
}

with open('artifacts/sample_kundli.json', 'w', encoding='utf-8') as f:
    json.dump(sample_data, f, ensure_ascii=False, indent=2)

pdf_out = build_pdf_dossier(sample_data, 'artifacts/VYAS_Kundli_Mahapatrika_Sample.pdf')
print('TEST PASSED! PDF successfully created at:', pdf_out)

