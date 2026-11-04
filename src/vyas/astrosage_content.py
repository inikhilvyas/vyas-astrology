"""AstroSage Standard Content & Interpretations Engine.

Provides comprehensive text banks and mathematical calculators matching the 56-page
AstroSage Gold Standard Kundli:
1. Ascendant Readings (all 12 signs: Health, Temperament, Appearance)
2. Nakshatra Readings (all 27 nakshatras: General, Education & Income, Family Life)
3. Life Predictions Synthesizer (Character, Happiness, Lifestyle, Career, Occupation, Health, Hobbies, Love, Finance, Education)
4. Western Aspects Calculator (12 bodies: Sun to Pluto, Chalit Bhava Madhya, KP Cusps)
5. Lal Kitab Planetary Analysis & Authentic Remedies (Hindi & English)
6. Planet Considerations (Deep Parashari & Shastric Synthesis for Sun to Ketu)
7. Prastharashtakvarga 7-Planet Matrix Generator
8. Transits Today (Gochar) Synthesizer (Bilingual)
9. Navagraha Remedial Matrix & Shanti Stotras
10. Sade Sati Comprehensive Guide & Kalsarpa 12-Type Master Table
11. Varshaphal Mudda Dasha Annual Readings
12. Page 56 Grand Vedic Synthesis & Blessings
"""
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional
import math

from vyas import constants
from vyas.ashtakavarga import BAV_RULES


# ---------------------------------------------------------------------------
# 1. ASCENDANT IN-DEPTH READINGS (12 SIGNS - BILINGUAL)
# ---------------------------------------------------------------------------
ASCENDANT_READINGS_EN = {
    0: {  # Aries
        "name": "Aries",
        "health": "Aries Ascendant people suffer from disease often pertaining to headaches, particularly migraines, sunstroke, neuralgia and depression. They are also prone to medical conditions like Indigestion and nervous disorders and their rashness, and physical devotion makes them liable to accidents and physical injuries, occasionally subjected to hot complaints like piles. Many Aries individuals are born with a birthmark on the head or facial area. People born under Aries sign are prone to circulatory troubles like high blood pressure etc.",
        "temperament": "Aries Ascendant people possess great force and energy, and they are always ready to take the initiative. Their most significant feature of their personality is their straightforwardness. They are natural leaders; they don't like taking orders from others as they are their own boss as well. Their fascination is due to their being unforeseeable: this characteristic sometimes leads to a behaviour which is aggressive and weak at the same time and highly temperamental but on the contrary they can be easily persuaded or pleased. Aries Ascendant people are direct in speech and often too outspoken and undiplomatic; therefore they mostly fall into heated articulation or arguments very easily. They are stubborn and their sudden outburst of anger astonishes people often but they can bring down easily by persuading them. Their impulsiveness sometimes gets them into some serious troubles. Not very fond of water and they appreciate beauty art and elegance. Most of all their kind like relaxing, but only after having reached a prefixed goal. Person born under this sign are sensible, endearing yet emotional at times.",
        "appearance": "Aries Ascendant people have strong and angular features, with a prominent chin, nose and mouth. They are athletic, of average height and build, with curly hair, a protruding arch of the eyebrows, tan complexion, a virile deportment for males, and a dynamic one for females. The whole physique gives an impression of might and ruggedness. They normally have brown or light dark curly hairs. They often have a mark or scar on their head. Mostly have prominent veins and there are marks arising out of wounds on their body."
    },
    1: {  # Taurus
        "name": "Taurus",
        "health": "Taurus Ascendant individuals are prone to ailments affecting the throat, neck, vocal cords, thyroid gland, and tonsils. Tendency towards weight gain and slow metabolic rate. Susceptible to respiratory issues, stiff neck, and hormonal fluctuations.",
        "temperament": "Taurus Ascendant people are calm, patient, persevering, and extremely reliable. They possess exceptional artistic sensibility and love material luxury and comfort. Once they set their mind on a goal, they demonstrate tremendous determination and steadfastness.",
        "appearance": "Pleasing and attractive facial contours, captivating expressive eyes, thick neck, sturdy and robust physical build with graceful movements."
    },
    2: {  # Gemini
        "name": "Gemini",
        "health": "Gemini Ascendants are susceptible to nervous debility, respiratory infections, asthma, bronchitis, and issues with the arms and shoulders. Mental anxiety often causes digestive sensitivity.",
        "temperament": "Quick-witted, versatile, communicative, and intellectually curious. They adapt swiftly to new environments and excel at networking, writing, research, and negotiation.",
        "appearance": "Tall or medium slender build, expressive hands, alert and sparkling eyes, fast speech and quick walking pace."
    },
    3: {  # Cancer
        "name": "Cancer",
        "health": "Vulnerable to gastrointestinal disorders, fluid retention, emotional indigestion, stomach ulcers, and lymphatic imbalances.",
        "temperament": "Deeply emotional, intuitive, protective, family-oriented, and receptive. High memory retention and cautious about financial security.",
        "appearance": "Round face, soft facial features, radiant complexion, full cheeks, and sensitive expressive demeanor."
    },
    4: {  # Leo
        "name": "Leo",
        "health": "Cardiovascular vulnerability, spine and upper back issues, high blood pressure, and heat-related exhaustion.",
        "temperament": "Regal, commanding, magnanimous, proud, and ambitious. Natural leader who commands authority effortlessly and exhibits fierce loyalty.",
        "appearance": "Broad shoulders, commanding posture, prominent forehead, thick hair mane, and piercing authoritative gaze."
    },
    5: {  # Virgo
        "name": "Virgo",
        "health": "Prone to digestive complaints, irritable bowel syndrome, nervous tension, and food sensitivities.",
        "temperament": "Analytical, meticulous, modest, practical, and highly methodical. Excels in detailed analysis, administrative precision, and problem solving.",
        "appearance": "Neat and well-groomed appearance, youthful facial demeanor, clear complexion, and sharp observant eyes."
    },
    6: {  # Libra
        "name": "Libra",
        "health": "Susceptible to kidney ailments, lower back pain, skin sensitivity, and diabetes.",
        "temperament": "Diplomatic, charming, peace-loving, aesthetic, and balanced. Strong sense of justice, harmony, and partnership.",
        "appearance": "Symmetrical features, pleasant smile, balanced stature, refined gestures, and charismatic presence."
    },
    7: {  # Scorpio
        "name": "Scorpio",
        "health": "Vulnerable to reproductive system issues, excretory troubles, piles, and infectious ailments.",
        "temperament": "Intense, resolute, secretive, perceptive, and fiercely determined. Unyielding willpower with acute psychological penetration.",
        "appearance": "Penetrating gaze, prominent nose, compact and muscular build, commanding quiet magnetism."
    },
    8: {  # Sagittarius
        "name": "Sagittarius",
        "health": "Prone to liver disorders, arterial troubles, sciatica, hip and thigh injuries.",
        "temperament": "Philosophical, optimistic, frank, generous, and freedom-loving. High moral ideals and love for exploration and higher learning.",
        "appearance": "Tall athletic frame, open cheerful face, broad forehead, and confident stride."
    },
    9: {  # Capricorn
        "name": "Capricorn",
        "health": "Susceptible to arthritis, knee ailments, skin dryness, rheumatism, and dental concerns.",
        "temperament": "Disciplined, cautious, ambitious, highly enduring, and structured. Patiently climbs to prominence through persistent hard work.",
        "appearance": "Lean angular physique, serious contemplative expression, prominent bone structure, and mature presence."
    },
    10: {  # Aquarius
        "name": "Aquarius",
        "health": "Prone to circulatory irregularities, varicose veins, ankle and calf cramps, and nervous exhaustion.",
        "temperament": "Humanitarian, inventive, progressive, independent, and intellectually egalitarian. Forward-looking thinker.",
        "appearance": "Attractive well-proportioned physique, clear thoughtful gaze, unique individualistic style."
    },
    11: {  # Pisces
        "name": "Pisces",
        "health": "Vulnerable to lymphatic congestion, foot and toe ailments, immune weaknesses, and fluid retention.",
        "temperament": "Empathetic, artistic, spiritually inclined, imaginative, and compassionate. Deep philosophical and creative intuition.",
        "appearance": "Dreamy expressive eyes, graceful soft contours, medium height, and gentle compassionate demeanor."
    }
}

ASCENDANT_READINGS_HI = {
    0: {
        "name": "मेष",
        "health": "मेष लग्न के जातकों को सिरदर्द, माइग्रेन, उच्च रक्तचाप, अनिद्रा तथा पित्त प्रकोप की समस्या का सामना करना पड़ सकता है। अत्यधिक सक्रियता, अधीरता एवं जल्दबाजी के कारण सिर अथवा चेहरे पर चोट या कटने का निशान प्रायः देखा जाता है। पाचन तंत्र की संवेदनशीलता तथा कभी-कभी रक्त संबंधी विकार भी उत्पन्न हो सकते हैं। नियमित प्राणायाम एवं शीतल जल का पर्याप्त सेवन स्वास्थ्य रक्षा में अत्यंत लाभकारी रहता है।",
        "temperament": "मेष लग्न के जातक अदम्य उत्साही, निर्भीक, स्पष्टवादी और स्वाभाविक जन्मजात नेता होते हैं। किसी के अधीन कार्य करने की अपेक्षा स्वयं अपना स्वतंत्र मार्ग प्रशस्त करना अधिक पसंद करते हैं। वाणी में स्पष्टता, खरापन एवं कभी-कभी उग्रता देखी जाती है, किंतु मन में द्वेष नहीं रहता और क्रोध शीघ्र शांत भी हो जाता है। चुनौतियों को स्वीकार करने में इन्हें विशेष आनंद आता है। सिद्धांतवादी एवं निष्ठावान मित्र सिद्ध होते हैं।",
        "appearance": "सुगठित बलिष्ठ शारीरिक सौष्ठव, प्रभावशाली मुखाकृति, उन्नत ललाट, तीक्ष्ण नासिका, मध्यम कद एवं दृढ़ आत्मविश्वास से युक्त चाल-ढाल। भौंहों का स्पष्ट उभार और चेहरे पर एक स्वाभाविक तेज विद्यमान रहता है, जो सहज ही लोगों का ध्यान आकर्षित करता है।"
    },
    1: {
        "name": "वृषभ",
        "health": "गले के विकार, थायरॉइड, टॉन्सिल, स्वर तंत्र की संवेदनशीलता एवं कफ की समस्या। शारीरिक वजन बढ़ने की स्वाभाविक प्रवृत्ति रहती है, अतः संतुलित आहार एवं नियमित व्यायाम अनिवार्य है।",
        "temperament": "धैर्यवान, स्थिरचित्त, कलाप्रेमी, व्यावहारिक एवं भौतिक सुख-सुविधाओं के प्रति आग्रही। एक बार किसी कार्य का संकल्प ले लें तो उसे पूर्ण निष्ठा व दृढ़ता से पूरा करते हैं। विश्वसनीयता इनका मुख्य गुण है।",
        "appearance": "आकर्षक नयन-नक्श, पुष्ट ग्रीवा, सुदृढ़ शरीर, कांतियुक्त सौम्य मुखमंडल एवं गरिमामयी शांत चाल-ढाल।"
    },
    2: {
        "name": "मिथुन",
        "health": "श्वास संबंधी रोग, स्नायु दुर्बलता, फेफड़ों व भुजाओं में संवेदनशीलता। मानसिक तनाव अथवा अति-विचार के कारण अनिद्रा व पाचन विकार संभव हैं।",
        "temperament": "वाकपटु, बौद्धिक, बहुआयामी प्रतिभा के धनी, जिज्ञासु एवं हर परिस्थिति में शीघ्र ढलने वाले। लेखन, संवाद, अनुसंधान एवं व्यापारिक वार्ताओं में अद्वितीय कुशलता प्रदर्शित करते हैं।",
        "appearance": "मध्यम अथवा लंबा छरहरा बदन, चंचल व तीक्ष्ण आंखें, सुरुचिपूर्ण वेशभूषा तथा तेज गति से चलने व बोलने की स्वाभाविक शैली।"
    },
    3: {
        "name": "कर्क",
        "health": "उदर रोग, पाचन संवेदनशीलता, जल-तत्व विकार, कफ एवं भावनात्मक उतार-चढ़ाव से उत्पन्न तनाव। स्वच्छ एवं सात्विक आहार इनके स्वास्थ्य की कुंजी है।",
        "temperament": "अत्यंत भावुक, संवेदनशील, परिवार-वत्सल, दयालु, रक्षात्मक एवं अगाध स्मरणशक्ति से युक्त। दूसरों के सुख-दुख को तुरंत भांप लेते हैं तथा आर्थिक सुरक्षा को विशेष महत्व देते हैं।",
        "appearance": "चंद्रमा के समान गोल मुखाकृति, सौम्य व कांतियुक्त चेहरा, स्निग्ध कोमल त्वचा तथा करुणामयी भावपूर्ण नयन।"
    },
    4: {
        "name": "सिंह",
        "health": "हृदय विकार, रीढ़ की हड्डी में तनाव, पित्त विकार, उच्च रक्तचाप व धूप-गर्मी से संवेदनशीलता। नियमित ध्यान एवं सूर्योपासना आरोग्य प्रदान करती है।",
        "temperament": "राजसी, महत्वाकांक्षी, उदार, स्वाभिमानी, साहसी एवं नेतृत्व क्षमता से परिपूर्ण। समाज में मान-सम्मान एवं प्रतिष्ठा सर्वोपरि मानते हैं। अन्याय के समक्ष कभी नहीं झुकते।",
        "appearance": "चौड़े कंधे, उन्नत ललाट, सिंह के समान ओजस्वी व प्रभावशाली व्यक्तित्व, घने बाल तथा सम्मोहक व अधिकारपूर्ण दृष्टि।"
    },
    5: {
        "name": "कन्या",
        "health": "पाचन संबंधी विकार, आंतों की संवेदनशीलता, स्नायु दुर्बलता एवं त्वचा संबंधी विकार। मानसिक विश्राम एवं चिंतामुक्त रहना स्वास्थ्य हेतु अनिवार्य है।",
        "temperament": "विश्लेषणात्मक, कर्तव्यनिष्ठ, सूक्ष्मदर्शी, व्यवस्थित, व्यावहारिक एवं मितव्ययी। हर कार्य में पूर्णता (परफेक्शन) की चाह रखते हैं। उत्कृष्ट योजनाकार सिद्ध होते हैं।",
        "appearance": "मध्यम कद, शांत-गंभीर मुखाकृति, स्पष्ट दृष्टि, सुव्यवस्थित व स्वच्छ वेशभूषा तथा सौम्य व शालीन व्यवहार।"
    },
    6: {
        "name": "तुला",
        "health": "गुर्दे (किडनी) से संबंधित विकार, कमर के निचले हिस्से में दर्द, त्वचा संवेदनशीलता व मधुमेह की संभावना। जल का प्रचुर सेवन एवं संतुलन लाभकारी है।",
        "temperament": "न्यायप्रिय, कूटनीतिक, कलाप्रेमी, संतुलित, सौहार्दपूर्ण एवं शांतिप्रिय। विवादों को मध्यस्थता से सुलझाने में माहिर होते हैं तथा साझेदारी में सफल रहते हैं।",
        "appearance": "समानुपातिक आकर्षक अंग-विन्यास, मनमोहक मुस्कान, सुंदर आंखें, सुरुचिपूर्ण व्यक्तित्व एवं अत्यंत सम्मोहक आकर्षण।"
    },
    7: {
        "name": "वृश्चिक",
        "health": "जननेंद्रिय विकार, बवासीर, संक्रामक रोग, रक्त संबंधी संवेदनशीलता एवं विषाक्त पदार्थों से सतर्कता आवश्यक है। सात्विक जीवनशैली लाभकारी रहती है।",
        "temperament": "दृढ़ संकल्पी, रहस्यमयी, शोधप्रवृत्त, निर्भीक, स्वाभिमानी एवं तीक्ष्ण बुद्धि युक्त। किसी भी विषय की तह तक जाना इनका स्वभाव है। विश्वासघात कभी नहीं भूलते।",
        "appearance": "गंभीर तीक्ष्ण भेदक दृष्टि, सुगठित गठीला शरीर, उन्नत नासिका तथा चुंबकीय व प्रभावशाली आभा।"
    },
    8: {
        "name": "धनु",
        "health": "यकृत (लीवर) विकार, कूल्हे व जांघों में चोट, मोटापा एवं वात-पित्त प्रकोप। खानपान में संयम एवं नियमित भ्रमण उत्तम स्वास्थ्य बनाए रखता है।",
        "temperament": "आशावादी, दार्शनिक, स्पष्टवक्ता, धर्मपरायण, परोपकारी एवं उच्च ज्ञान के अभिलाषी। स्वतंत्र विचारों के धनी होते हैं तथा यात्राओं से गहरा प्रेम करते हैं।",
        "appearance": "लंबा सुगठित कद, उन्नत ललाट, प्रसन्नचित्त मुद्रा, खुली-स्पष्ट आंखें तथा गरिमामयी आत्मविश्वास युक्त चाल।"
    },
    9: {
        "name": "मकर",
        "health": "जोड़ों व घुटनों में दर्द, त्वचा का सूखापन, वात विकार, गठिया एवं दंत संबंधी संवेदनशीलता। नियमित तेल मालिश एवं धूप सेवन स्वास्थ्यवर्धक है।",
        "temperament": "अनुशासित, महत्वाकांक्षी, दूरदर्शी, कठोर परिश्रमी, धैर्यवान एवं व्यावहारिक। कठिन से कठिन परिस्थितियों में भी धीरे-धीरे शिखर तक पहुंचते हैं।",
        "appearance": "दुबला-पतला सुदृढ़ शरीर, गंभीर व विचारशील मुखमंडल, गहरी आंखें एवं परिपक्व व संयमित व्यक्तित्व।"
    },
    10: {
        "name": "कुम्भ",
        "health": "रक्त-संचार विकार, पिंडलियों व टखनों में दर्द, स्नायु थकावट व हृदय संबंधी संवेदनशीलता। पर्याप्त विश्राम एवं प्राणायाम अति आवश्यक है।",
        "temperament": "मानवतावादी, स्वतंत्र चेता, नवीन विचारक, दार्शनिक, परोपकारी एवं पक्षपातरहित। समाज कल्याण व आधुनिक अनुसंधान में विशेष रुचि रखते हैं।",
        "appearance": "आकर्षक सुगठित कद, विचारमग्न सौम्य आंखें, चेहरे पर बौद्धिक आभा तथा विशिष्ट व शालीन वेशभूषा।"
    },
    11: {
        "name": "मीन",
        "health": "पैरों के विकार, कफ-प्रधान रोग, रोग-प्रतिरोधक क्षमता की कमी एवं जलजनित संवेदनशीलता। स्वच्छ वातावरण एवं ध्यान-साधना लाभकारी है।",
        "temperament": "दयालु, आध्यात्मिक, परोपकारी, कल्पनाशील, कलात्मक एवं असीम संवेदनाओं से परिपूर्ण। दूसरों के कष्टों से शीघ्र द्रवित हो जाते हैं।",
        "appearance": "सौम्य-कोमल नयन, मधुर मुखाकृति, मध्यम कद, शांत व स्निग्ध त्वचा तथा गरिमामयी शांत आचरण।"
    }
}


# ---------------------------------------------------------------------------
# 2. NAKSHATRA PHAL (27 NAKSHATRAS - BILINGUAL)
# ---------------------------------------------------------------------------
NAKSHATRA_DATA_EN = {
    "Anuradha": {
        "prediction": "You have profound faith in God. This is the reason why you don't get upset in any difficult situation. Hurdles may come in life, but they won't be able to shake you from your path because you are a hard worker. You will start earning at a very young age. Your nature is quite strugglesome. For mental peace, you have to put regular efforts. As you are quite straightforward, you say everything that comes to your mind. It is not in your nature to keep anything in your heart. That is why sometimes people get hurt with your words. Whenever you try to help someone, you do it with all your heart. You don't show off. As you stay quite serious about your aim, you manage to be successful after so many hurdles. Whatever opportunity comes to you, you try to utilize it to the fullest. You are more interested in doing business than work. Business skills are being carried by you from your childhood. Hence, you may get really successful in it. If you will start working in a job, you will be able to make all your seniors in your favor. You are quite disciplined in your life and give a lot of importance to the principles of life. You try to maintain complete discipline in your work. Being doctrinal, you don't have many friends and your circle is quite small. You will get the lessons of life by your struggles. Those who know the qualities of your personality, will take suggestions from you because you are quite experienced. There is a miraculous skill in you to get rid of any difficult situation. If your wealth is concerned, you will have ample of it because you are interested in investing on property or keeping it as savings. Due to this tendency of making investments, you will be quite rich.",
        "education_income": "You will start making money at a very young age like 17 or 18 years. Favorable fields for you are hypnotist; Tantrik; astrology; espionage; photography; work related to cinema, music and art; business; management; counselling; psychology; science; numerology; mathematics; work related to the governance; industrialist; works related to tourism department; etc.",
        "family": "You will get less support from your supporters in personal life. Also, there are chances of tiffs with father. You will usually stay far from your birthplace. Your child will get more success than you in life."
    }
}

NAKSHATRA_DATA_HI = {
    "Anuradha": {
        "prediction": "आप ईश्वर में प्रगाढ़ आस्था रखते हैं। यही कारण है कि आप किसी भी विषम परिस्थिति में विचलित नहीं होते। जीवन में बाधाएं अवश्य आ सकती हैं किंतु वे आपके संकल्प को डिगा नहीं पातीं क्योंकि आप अत्यंत परिश्रमी हैं। आप छोटी आयु से ही उपार्जन आरंभ कर देते हैं। आपका स्वभाव संघर्षशील है। आप मन में कोई बात नहीं रखते और सत्य व खरी बात कहते हैं। यद्यपि इससे कभी-कभी लोग आहत हो सकते हैं, किंतु आपके अंतःकरण में कपट नहीं होता। किसी की सहायता करते समय आप पूर्ण हृदय से सहयोग करते हैं। व्यापारिक सूझबूझ आपमें स्वाभाविक रूप से विद्यमान है। आप अनुशासित जीवन जीते हैं तथा सिद्धांतों को सर्वोपरि मानते हैं। कठिन से कठिन परिस्थिति से उबरने का विलक्षण कौशल आपमें है। संपत्ति एवं बचत में निवेश की रुचि के कारण आप प्रचुर धन-वैभव अर्जित करने में सफल होंगे।",
        "education_income": "आप 17-18 वर्ष की युवावस्था से ही आत्मनिर्भर बनने का प्रयास करते हैं। आपके लिए ज्योतिष, विज्ञान, गणित, प्रबंधन, परामर्श, उद्योग, प्रशासन, पर्यटन, अनुसंधान एवं कला-सिनेमा के क्षेत्र अत्यंत अनुकूल व लाभप्रद रहेंगे।",
        "family": "व्यक्तिगत जीवन में सहयोगियों से सीमित सहयोग की संभावना रहती है। पिता के विचारों से मतभेद हो सकते हैं। आप प्रायः जन्मस्थान से दूर रहकर भाग्योदय प्राप्त करते हैं। आपकी संतान आपसे भी अधिक यश व प्रतिष्ठा अर्जित करेगी।"
    }
}

def get_nakshatra_content(nak_name: str, pada: int, lang: str = "en") -> dict:
    default_en = {
        "prediction": f"Born in {nak_name} nakshatra pada {pada}, you possess keen intellect, strong willpower, and perseverance. You face challenges with resilience and establish authority through your consistent dedication. Your straightforward character and commitment to core principles earn you long-lasting respect in society. With patient focus and prudent decisions, you create enduring wealth and familial security.",
        "education_income": f"Favorable avenues include technology, management, analytical sciences, trade and commerce, advisory roles, administrative governance, industrial ventures, and creative fields.",
        "family": "You value familial bonds and uphold traditions. Career and destiny often flourish when staying or establishing ventures away from birthplace. Family life stabilizes beautifully with maturity."
    }
    default_hi = {
        "prediction": f"{nak_name} नक्षत्र के {pada} चरण में जन्म होने से आप तीव्र बुद्धि, दृढ़ इच्छाशक्ति एवं पुरुषार्थी स्वभाव से युक्त हैं। आप कठिनाइयों का सामना धैर्यपूर्वक करते हैं तथा अपने सिद्धांतों पर अडिग रहकर समाज में आदरणीय स्थान प्राप्त करते हैं। वाणी में सत्यता एवं कार्य में निष्ठा आपकी मूल पहचान है। छोटी-मोटी रुकावटों के बाद भी अपने लक्ष्य को प्राप्त करने में आप पूर्णतः सक्षम हैं।",
        "education_income": "प्रबंधन, विज्ञान, व्यापार, परामर्श, प्रशासनिक सेवाएं, तकनीकी क्षेत्र, बैंकिंग, उद्योग एवं स्वतंत्र उद्यम आपके लिए अत्यंत लाभकारी सिद्ध होंगे। व्यावहारिक सूझबूझ से आप प्रचुर धन संचय करेंगे।",
        "family": "पारिवारिक संस्कारों का सम्मान करते हैं। जन्मस्थान से दूर रहकर कार्यक्षेत्र में विशेष सफलता एवं भाग्योदय के योग बनते हैं। जीवनसाथी एवं संतान का सुखद सहयोग प्राप्त होगा।"
    }
    if lang == "en":
        return NAKSHATRA_DATA_EN.get(nak_name, default_en)
    else:
        return NAKSHATRA_DATA_HI.get(nak_name, default_hi)


# ---------------------------------------------------------------------------
# 3. WESTERN ASPECTS CALCULATOR
# ---------------------------------------------------------------------------
ASPECT_TYPES = [
    ("CONJ", 0.0, 15.0, 10),
    ("OPPN", 180.0, 15.0, 10),
    ("TRIN", 120.0, 6.0, 3),
    ("SQUR", 90.0, 6.0, 3),
    ("SEXT", 60.0, 6.0, 3),
    ("SSQU", 45.0, 1.0, 1),
    ("NONL", 40.0, 1.0, 1),
    ("QUIN", 72.0, 1.0, 1),
    ("SQQD", 135.0, 1.0, 1),
    ("QCUN", 150.0, 1.0, 1),
]

def check_western_aspect(lon1: float, lon2: float) -> Tuple[str, float, int]:
    diff = abs((lon1 % 360.0) - (lon2 % 360.0))
    if diff > 180.0:
        diff = 360.0 - diff
        
    for abbr, angle, orb, weight in ASPECT_TYPES:
        delta = abs(diff - angle)
        if delta <= orb:
            return abbr, delta, weight
    return "", 0.0, 0


def compute_all_western_aspects(planet_lons: Dict[str, float]) -> Dict[Tuple[str, str], Tuple[str, float, int]]:
    aspects = {}
    p_names = list(planet_lons.keys())
    for i, p1 in enumerate(p_names):
        for j, p2 in enumerate(p_names):
            if i >= j:
                continue
            abbr, delta, wt = check_western_aspect(planet_lons[p1], planet_lons[p2])
            if abbr:
                aspects[(p1, p2)] = (abbr, delta, wt)
                aspects[(p2, p1)] = (abbr, delta, wt)
    return aspects


def compute_aspects_on_points(planet_lons: Dict[str, float], point_lons: Dict[int, float]) -> Dict[Tuple[str, int], Tuple[str, float, int]]:
    res = {}
    for p_name, p_lon in planet_lons.items():
        for pt_num, pt_lon in point_lons.items():
            abbr, delta, wt = check_western_aspect(p_lon, pt_lon)
            if abbr:
                res[(p_name, pt_num)] = (abbr, delta, wt)
    return res


# ---------------------------------------------------------------------------
# 4. PRASTHARASHTAKVARGA 7-PLANET MATRIX GENERATOR
# ---------------------------------------------------------------------------
def compute_full_prastharashtakvarga(planet_signs: Dict[str, int], asc_sign: int) -> Dict[str, Dict[str, List[int]]]:
    planets_7 = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    contributors = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Lagna"]
    
    ref_signs = {p: planet_signs[p] for p in planets_7}
    ref_signs["Lagna"] = asc_sign
    
    result = {}
    for p_target in planets_7:
        rules = BAV_RULES[p_target]
        grid = {}
        for c_name in contributors:
            c_sign = ref_signs[c_name]
            allowed_houses = set(rules.get(c_name, []))
            row = []
            for sign_idx in range(12):
                house_from_c = (sign_idx - c_sign + 12) % 12 + 1
                row.append(1 if house_from_c in allowed_houses else 0)
            grid[c_name] = row
        result[p_target] = grid
    return result


# ---------------------------------------------------------------------------
# 5. LAL KITAB 9-PLANET HOUSE PREDICTIONS & REMEDIES (BILINGUAL)
# ---------------------------------------------------------------------------
LAL_KITAB_HOUSE_RULES_EN = {
    "Sun": {
        8: {
            "benefic": [
                "(1) Government favours and societal recognition accrue from the 22nd year of life.",
                "(2) Bestows truthful conduct, spiritual fortitude, and authoritative demeanor."
            ],
            "malefic": [
                "(1) Unchecked expenditures or rash articulation may create temporary economic vacillations.",
                "(2) Prone to digestive irritability, eye strain, or sudden disputes."
            ],
            "remedies": [
                "(1) Never live in a house with its main entrance directly facing south.",
                "(2) Always consume something sweet and drink fresh water before initiating new ventures.",
                "(3) Offer jaggery (gur) into flowing clean water on Sundays.",
                "(4) Maintain high ethical conduct and avoid unearned favours."
            ]
        }
    },
    "Moon": {
        8: {
            "benefic": [
                "(1) Deeply intuitive perception, keen interest in research, and spiritual elevation.",
                "(2) Unexpected monetary settlements and preservation of ancestral heritage."
            ],
            "malefic": [
                "(1) Fluctuating emotional peace, anxiety during dark lunar fortnights, or mother's health concerns.",
                "(2) Avoid unvetted financial speculation or gambling."
            ],
            "remedies": [
                "(1) Touch parents' and elderly mentors' feet daily to receive divine blessings.",
                "(2) Bring water from a sacred pilgrimage well or river and keep it in a silver vessel at home.",
                "(3) Offer milk or kheer to needy girls and elderly ladies on Mondays.",
                "(4) Never cover an open well or water reservoir with a permanent roof."
            ]
        }
    },
    "Mars": {
        10: {
            "benefic": [
                "(1) Highly exalted planetary placement (Kuldeepak Yoga); confers executive power, courage, and immense prosperity.",
                "(2) Distinct professional authority, leadership accolades, and family prominence."
            ],
            "malefic": [
                "(1) Impatience with slow associates or hasty vehicular driving.",
                "(2) Domestic friction if professional pressures are carried home."
            ],
            "remedies": [
                "(1) Serve wounded or stray animals, especially deer and dogs.",
                "(2) Ensure boiling milk does not spill into open fire in the kitchen.",
                "(3) Do not sell gold or ancestral land in haste.",
                "(4) Recite Hanuman Chalisa daily with focused devotion."
            ]
        }
    },
    "Mercury": {
        8: {
            "benefic": [
                "(1) Formidable intellect, sharp analytical prowess, and mastery over complex occult subjects.",
                "(2) Lucrative advice and sudden intellectual breakthroughs."
            ],
            "malefic": [
                "(1) Nervous sensitivity, fluctuating skin health, or unexpected commercial misunderstandings.",
                "(2) Avoid verbal promises; document all contractual obligations."
            ],
            "remedies": [
                "(1) Place fresh rainwater in an earthen container on the terrace or rooftop.",
                "(2) Wear a clean copper coin or ring without a joint.",
                "(3) Feed soaked green moong dal or fresh spinach to sacred cows on Wednesdays.",
                "(4) Maintain transparent written accounting in all transactions."
            ]
        }
    },
    "Jupiter": {
        9: {
            "benefic": [
                "(1) Supreme spiritual luck, societal reverence, ethical lineage, and mentorship honors.",
                "(2) Lifelong protection against calamities and fruitful long-distance journeys."
            ],
            "malefic": [
                "(1) Excessive dogmatism or taking fortunes for granted.",
                "(2) Neglect of traditional rituals during material abundance."
            ],
            "remedies": [
                "(1) Visit temples or places of worship regularly and offer yellow flowers.",
                "(2) Apply saffron (kesar) or turmeric tilak on forehead, throat, and navel daily.",
                "(3) Completely abstain from intoxicants and alcohol.",
                "(4) Respect teachers, scholars, and elderly ascetics."
            ]
        }
    },
    "Venus": {
        9: {
            "benefic": [
                "(1) Aesthetic sophistication, refined domestic bliss, artistic appreciation, and noble spouse.",
                "(2) Steady wealth accumulation through creative ventures and diplomatic elegance."
            ],
            "malefic": [
                "(1) Lavish impulsive expenditures on luxury items.",
                "(2) Sentimental vulnerabilities in friendships."
            ],
            "remedies": [
                "(1) Bury a piece of pure silver in the foundation or keep a solid silver token in purse.",
                "(2) Wear clean, well-ironed clothes and use gentle natural sandalwood fragrances.",
                "(3) Uphold high marital fidelity and respect women.",
                "(4) Offer white sweets, rice, or curd in temple on Fridays."
            ]
        }
    },
    "Saturn": {
        7: {
            "benefic": [
                "(1) Substantial success in machinery, real estate, metals, law, and long-term business partnerships.",
                "(2) Mature, steadfast partner and societal elevation through perseverance."
            ],
            "malefic": [
                "(1) Rigidity in interpersonal dynamics or delays in initial settlements.",
                "(2) Eye fatigue or joint sensitivity if physical discipline lapses."
            ],
            "remedies": [
                "(1) Bury a bamboo flute filled with honey or sugar in a secluded open spot.",
                "(2) Serve black cows, crows, and underprivileged labourers on Saturdays.",
                "(3) Light a mustard oil lamp under a Peepal tree after sunset on Saturdays.",
                "(4) Maintain strict honesty in commercial partnerships."
            ]
        }
    },
    "Rahu": {
        2: {
            "benefic": [
                "(1) Extraordinary monetary wealth through modern technology, international trade, or government projects.",
                "(2) Commanding speech and keen intuition to navigate complex negotiations."
            ],
            "malefic": [
                "(1) Sudden unforeseen expenditures and erratic dietary or verbal habits.",
                "(2) Domestic misunderstandings with extended family members."
            ],
            "remedies": [
                "(1) Keep a solid silver ball (without hole) in your pocket or personal vault.",
                "(2) Apply saffron or yellow sandalwood tilak daily.",
                "(3) Maintain cordial relations with mother and maternal relatives.",
                "(4) Do not accept electrical appliances or copper articles as free gifts."
            ]
        }
    },
    "Ketu": {
        8: {
            "benefic": [
                "(1) Miraculous protection against severe adversities, profound intuition, and philosophical depth.",
                "(2) Independent willpower and capability to conquer insurmountable crises."
            ],
            "malefic": [
                "(1) Urinary sensitivity, joint pains, or unpredictable associates.",
                "(2) Restlessness or feeling misunderstood."
            ],
            "remedies": [
                "(1) Feed stray two-colored (black & white) dogs with bread or biscuits daily.",
                "(2) Donate a warm two-colored blanket to a needy elderly person on Tuesdays/Saturdays.",
                "(3) Worship Lord Ganesha with devotion by reciting Sankat Nashan Ganesha Stotra.",
                "(4) Apply kesar tilak and wear gold in ears or around neck."
            ]
        }
    }
}

LAL_KITAB_HOUSE_RULES_HI = {
    "Sun": {
        8: {
            "benefic": [
                "(1) उम्र के 22वें वर्ष से सरकार, समाज एवं उच्चाधिकारियों से विशेष सहयोग व लाभ प्राप्त होता है।",
                "(2) जातक को सच्चा, पुण्यात्मा, निडर और राजा के समान तेजस्वी व प्रभावशाली व्यक्तित्व प्रदान करता है।"
            ],
            "malefic": [
                "(1) अनियंत्रित खर्च, जल्दबाजी अथवा वाणी की उग्रता से सामयिक आर्थिक असंतुलन संभव है।",
                "(2) नेत्र संवेदनशीलता अथवा पित्त प्रकोप के प्रति सावधानी बरतें।"
            ],
            "remedies": [
                "(1) दक्षिण मुखी मुख्य द्वार वाले मकान में रहने से बचें।",
                "(2) किसी भी महत्वपूर्ण नए कार्य को प्रारंभ करने से पूर्व मीठा खाकर ऊपर से शुद्ध जल पिएं।",
                "(3) रविवार के दिन बहते हुए स्वच्छ जल में थोड़ा गुड़ प्रवाहित करें।",
                "(4) घर में कभी भी फटा-पुराना सफेद कपड़ा एकत्र न रखें।"
            ]
        }
    },
    "Moon": {
        8: {
            "benefic": [
                "(1) जातक को गहन अंतर्दृष्टि, आध्यात्मिक संवेदनशीलता एवं गूढ़ विषयों में विलक्षण सफलता मिलती है।",
                "(2) अचानक धन लाभ, पैतृक संपत्ति की रक्षा एवं संकटों से दैवीय सुरक्षा प्राप्त होती है।"
            ],
            "malefic": [
                "(1) कृष्ण पक्ष में मानसिक बेचैनी अथवा माता के स्वास्थ्य के प्रति सामयिक चिंता उत्पन्न हो सकती है।",
                "(2) सट्टा, जुआ एवं अनैतिक निवेश से सर्वथा दूर रहें।"
            ],
            "remedies": [
                "(1) माता, बुजुर्गों एवं कन्याओं के चरण स्पर्श कर नित्य आशीर्वाद प्राप्त करें।",
                "(2) किसी पवित्र तीर्थ के कुएं अथवा नदी का जल लाकर चांदी के पात्र में सुरक्षित घर में रखें।",
                "(3) सोमवार को जरूरतमंद कन्याओं को दूध, खीर अथवा सफेद मिठाई का दान करें।",
                "(4) घर के समीप स्थित कुएं अथवा जल स्रोत को छत डालकर कभी न ढकें।"
            ]
        }
    },
    "Mars": {
        10: {
            "benefic": [
                "(1) दशम भाव में मंगल अपनी उच्च राशि तुल्य फल देकर 'कुलदीपक योग' बनाता है; जातक कुल व समाज में कीर्तिमान स्थापित करता है।",
                "(2) प्रशासनिक अधिकार, अदम्य साहस, भूमि-भवन का प्रचुर सुख एवं नेतृत्व का सम्मान प्राप्त होता है।"
            ],
            "malefic": [
                "(1) कार्यक्षेत्र में अधीनस्थों के प्रति अत्यधिक अधीरता अथवा वाहन तीव्र गति से चलाने की आदत से बचें।",
                "(2) अत्यधिक कार्यभार से मानसिक तनाव घर न लाएं।"
            ],
            "remedies": [
                "(1) गाय, हिरण एवं मूक पशुओं की निष्काम सेवा करें।",
                "(2) रसोई में दूध उबालते समय ध्यान रखें कि वह उफनकर आग पर न गिरे।",
                "(3) पैतृक संपत्ति अथवा स्वर्ण को कभी जल्दबाजी या घाटे में न बेचें।",
                "(4) नित्य श्रद्धापूर्वक श्री हनुमान चालीसा का पाठ करें।"
            ]
        }
    },
    "Mercury": {
        8: {
            "benefic": [
                "(1) असाधारण विश्लेषणात्मक मेधा, त्वरित निर्णय क्षमता तथा गूढ़ विद्याओं व अनुसंधान में उत्कृष्ट सफलता।",
                "(2) बौद्धिक परामर्श एवं विशेषज्ञता के बल पर आकस्मिक धनोपार्जन के योग बनते हैं।"
            ],
            "malefic": [
                "(1) स्नायु दुर्बलता, त्वचा संवेदनशीलता अथवा मौखिक समझौतों के कारण भ्रम की स्थिति।",
                "(2) बिना लिखित अनुबंध के कोई बड़ा व्यापारिक जोखिम न लें।"
            ],
            "remedies": [
                "(1) मिट्टी के नए पात्र में वर्षा का शुद्ध जल भरकर घर की छत पर स्थापित करें।",
                "(2) बिना जोड़ वाला शुद्ध तांबे का सिक्का अथवा छल्ला धारण करें।",
                "(3) बुधवार को भीगी हुई साबुत हरी मूंग की दाल अथवा हरा चारा गोमाता को खिलाएं।",
                "(4) लेन-देन का हिसाब-किताब सदैव पूर्णतः स्पष्ट व लिखित रखें।"
            ]
        }
    },
    "Jupiter": {
        9: {
            "benefic": [
                "(1) नवम भाव में गुरु धर्म, भाग्य एवं प्रतिष्ठा की सर्वोच्च वृद्धि करता है; जातक सम्मानित व पूजनीय होता है।",
                "(2) सत्कर्मों से भाग्योदय, दीर्घायु, विद्वानों का सानिध्य तथा श्रेष्ठ संतान सुख प्राप्त होता है।"
            ],
            "malefic": [
                "(1) भाग्य पर अत्यधिक निर्भर रहकर पुरुषार्थ में शिथिलता न आने दें।",
                "(2) बुजुर्गों अथवा गुरुजनों की उपेक्षा से भाग्य में अवरोध संभव है।"
            ],
            "remedies": [
                "(1) नियमित रूप से देवस्थान अथवा मंदिर में जाकर पीले पुष्प व फल अर्पित करें।",
                "(2) प्रतिदिन माथे, कंठ एवं नाभि पर केसर अथवा शुद्ध हल्दी का तिलक लगाएं।",
                "(3) मदिरा एवं सभी प्रकार के तामसिक पदार्थों से पूर्णतः दूर रहें।",
                "(4) गुरुजनों, साधु-संतों एवं वरिष्ठों का सदैव हृदय से आदर करें।"
            ]
        }
    },
    "Venus": {
        9: {
            "benefic": [
                "(1) सुरुचिपूर्ण जीवनशैली, उत्तम दांपत्य सुख, कलात्मक दृष्टि एवं गुणवान व सुलक्षणा जीवनसाथी।",
                "(2) उद्योग, साझेदारी एवं रचनात्मक कार्यों के माध्यम से निरंतर धन-वैभव की प्राप्ति।"
            ],
            "malefic": [
                "(1) विलासिता अथवा दिखावे पर अनियंत्रित व्यय की प्रवृत्ति।",
                "(2) अति-संवेदनशीलता के कारण मित्रों से अपेक्षाएं आहत होना।"
            ],
            "remedies": [
                "(1) घर की नींव में शुद्ध चांदी का टुकड़ा दबाएं अथवा अपने पर्स में चांदी का चौकोर सिक्का रखें।",
                "(2) स्वच्छ, सुसज्जित वस्त्र पहनें एवं प्राकृतिक चंदन की सुगंध का उपयोग करें।",
                "(3) स्त्रियों का सम्मान करें तथा दांपत्य निष्ठा का कड़ाई से पालन करें।",
                "(4) शुक्रवार को मंदिर में सफेद मिठाई अथवा चावल का दान करें।"
            ]
        }
    },
    "Saturn": {
        7: {
            "benefic": [
                "(1) मशीनरी, भूमि-भवन, खनिज, वकालत एवं सार्वजनिक कार्यों में अत्यंत दीर्घकालिक व सुदृढ़ सफलता।",
                "(2) परिपक्व व कर्तव्यनिष्ठ जीवनसाथी का सहयोग एवं सतत परिश्रम से समाज में उच्च पद-प्रतिष्ठा।"
            ],
            "malefic": [
                "(1) साझेदारी अथवा रिश्तों में हठधर्मिता या अत्यधिक कठोरता से दूरी बन सकती है।",
                "(2) शारीरिक दिनचर्या में आलस्य से नेत्र व जोड़ों में संवेदनशीलता संभव है।"
            ],
            "remedies": [
                "(1) बांस की बांसुरी में शुद्ध शहद अथवा शक्कर भरकर किसी सुनसान स्थान पर भूमि में दबाएं।",
                "(2) शनिवार को काली गाय, कौवे एवं निर्धन श्रमिकों को भोजन कराएं।",
                "(3) शनिवार की संध्या को पीपल के वृक्ष के नीचे सरसों के तेल का दीपक प्रज्वलित करें।",
                "(4) व्यापारिक समझौतों में पूर्ण ईमानदारी व निष्पक्षता बनाए रखें।"
            ]
        }
    },
    "Rahu": {
        2: {
            "benefic": [
                "(1) आधुनिक तकनीक, विदेशी संपर्कों अथवा बड़े प्रशासनिक उपक्रमों से अप्रत्याशित धन संचय।",
                "(2) प्रभावशाली वाकपटुता एवं प्रतिद्वंदियों पर विजय प्राप्त करने की कूटनीतिक दक्षता।"
            ],
            "malefic": [
                "(1) अचानक होने वाले अप्रत्याशित खर्चे तथा खान-पान व वाणी में असंयम से हानि।",
                "(2) पारिवारिक कुटुंब में छोटी-मोटी गलतफहमियों से अशांति संभव है।"
            ],
            "remedies": [
                "(1) अपनी जेब अथवा तिजोरी में बिना छेद वाली ठोस चांदी की गोली रखें।",
                "(2) प्रतिदिन केसर अथवा पीले चंदन का तिलक लगाएं।",
                "(3) माता एवं ननिहाल पक्ष से मधुर व सम्मानजनक संबंध बनाए रखें।",
                "(4) बिजली के पुराने खराब उपकरण घर में एकत्र न रखें तथा मुफ्त में उपहार न लें।"
            ]
        }
    },
    "Ketu": {
        8: {
            "benefic": [
                "(1) घोर संकटों से स्वतः रक्षा, असाधारण छठी इंद्री (इंट्यूशन) एवं आध्यात्मिक-दार्शनिक गहराई।",
                "(2) विपरीत से विपरीत परिस्थितियों में भी धैर्य व पुरुषार्थ से विजय प्राप्त करने का सामर्थ्य।"
            ],
            "malefic": [
                "(1) मूत्र विकार, जोड़ों में जकड़न अथवा अविश्वसनीय मित्रों द्वारा सामयिक कष्ट।",
                "(2) कभी-कभी मानसिक उद्विग्नता व अकेलापन महसूस होना।"
            ],
            "remedies": [
                "(1) दोरंगे (काले-सफेद) आवारा श्वानों को प्रतिदिन रोटी अथवा मीठा बिस्कुट खिलाएं।",
                "(2) मंगलवार अथवा शनिवार को किसी जरूरतमंद को दोरंगा कंबल दान करें।",
                "(3) नित्य 'संकटनाशन गणेश स्तोत्र' का पाठ कर विघ्नहर्ता भगवान गणेश की आराधना करें।",
                "(4) माथे पर केसर का तिलक लगाएं एवं कानों में सोने की बाली या गले में स्वर्ण धारण करें।"
            ]
        }
    }
}

def get_lal_kitab_house_data(planet: str, house: int, lang: str = "en") -> dict:
    if lang == "hi":
        default_hi = {
            "benefic": [
                f"(1) {constants.PLANETS_HI.get(planet, planet)} भाव {house} में जातक को कार्यकुशलता, तेजस्विता एवं उन्नति के अवसर प्रदान करता है।",
                "(2) पुरुषार्थ एवं धर्मपरायणता से जीवन में स्थिरता, धन-धान्य एवं प्रतिष्ठा की वृद्धि होती है।"
            ],
            "malefic": [
                "(1) जल्दबाजी में निर्णय लेने अथवा अधीरता से सामयिक कठिनाइयों का सामना करना पड़ सकता है।",
                "(2) अनियंत्रित व्यय एवं व्यर्थ के मानसिक तनाव से बचें।"
            ],
            "remedies": [
                "(1) कुलदेवता व इष्टदेव की नित्य आराधना करें तथा माता-पिता का आशीर्वाद लें।",
                "(2) सूर्योदय के समय उगते सूर्य को तांबे के लोटे से अर्घ्य दें एवं पक्षियों को दाना डालें।",
                "(3) व्यसनों से सर्वथा दूर रहें तथा सात्विक आचरण का पालन करें।"
            ]
        }
        return LAL_KITAB_HOUSE_RULES_HI.get(planet, {}).get(house, default_hi)
    else:
        default_en = {
            "benefic": [
                f"(1) {planet} in house {house} grants authority, sharp acumen, and opportunities for advancement.",
                "(2) Steadfast focus and ethical conduct bring long-lasting stability."
            ],
            "malefic": [
                "(1) Impulsive speech or haste in investments may create avoidable hurdles.",
                "(2) Emotional restlessness during conflicting transits."
            ],
            "remedies": [
                "(1) Worship family deity and respect elderly mentors.",
                "(2) Offer fresh water to rising Sun and grains to birds daily.",
                "(3) Avoid intoxicants and uphold strict personal integrity."
            ]
        }
        return LAL_KITAB_HOUSE_RULES_EN.get(planet, {}).get(house, default_en)


# ---------------------------------------------------------------------------
# 6. PLANET CONSIDERATIONS (DEEP SHASTRIC BILINGUAL SYNTHESIS)
# ---------------------------------------------------------------------------
PLANET_CORE_KARAKAS = {
    "Sun": {
        "title_hi": "सूर्य देव (आत्मकारक, पिता, प्रतिष्ठा व प्रशासनिक सत्ता)",
        "title_en": "Sun (Atmakaraka - Soul, Father, Authority & Regal Dignity)",
        "karakas_hi": "आत्मा, पिता, राज्यकृपा, प्रशासनिक प्रभाव, आत्मबल, नेत्र एवं शारीरिक तेज",
        "karakas_en": "Soul, father, royal favor, executive vitality, leadership, eye health & radiance"
    },
    "Moon": {
        "title_hi": "चन्द्र देव (मनोकारक, माता, मानसिक शांति व संवेदना)",
        "title_en": "Moon (Manokaraka - Mind, Mother, Emotions & Intuitive Grace)",
        "karakas_hi": "मन, माता, मानसिक संतुलन, जनसंपर्क, जल-तत्व, कल्पनाशीलता एवं अंतःकरण",
        "karakas_en": "Mind, mother, emotional equilibrium, public rapport, imagination & psychic calm"
    },
    "Mars": {
        "title_hi": "मंगल देव (पराक्रम, भ्रातृ सुख, साहस व भूमि-भवन)",
        "title_en": "Mars (Bhratrukaraka - Valour, Courage, Land, Energy & Conquest)",
        "karakas_hi": "शौर्य, साहस, भ्राता, अचल संपत्ति, सेना, तकनीकी कार्य एवं ऊर्जा",
        "karakas_en": "Courage, prowess, siblings, immovable real estate, technical enterprise & vitality"
    },
    "Mercury": {
        "title_hi": "बुध देव (बुद्धि, वाणी, व्यापार, तर्क व विश्लेषण)",
        "title_en": "Mercury (Buddhi - Intellect, Analytical Wit, Commerce & Eloquence)",
        "karakas_hi": "बुद्धि, वाकपटुता, व्यापारिक दक्षता, गणित, लेखन, संचार एवं कूटनीति",
        "karakas_en": "Intellect, articulation, commerce, mathematics, documentation & analytical agility"
    },
    "Jupiter": {
        "title_hi": "गुरु देव (ज्ञान, धर्म, संतति, भाग्य व परम सुख)",
        "title_en": "Jupiter (Guru - Supreme Wisdom, Dharma, Progeny, Fortune & Grace)",
        "karakas_hi": "ज्ञान, गुरु, धर्म, संतान, धन, उच्च दर्शन, चरित्र एवं ईश्वरीय कृपा",
        "karakas_en": "Wisdom, preceptor, righteousness, progeny, wealth, philosophy & divine grace"
    },
    "Venus": {
        "title_hi": "शुक्र देव (कला, दांपत्य, भौतिक ऐश्वर्य व सौन्दर्य)",
        "title_en": "Venus (Shukra - Marital Bliss, Aesthetics, Luxury, Vehicle & Arts)",
        "karakas_hi": "दांपत्य, प्रेम, वाहन सुख, कला-संगीत, सौंदर्य, ऐश्वर्य एवं आकर्षण",
        "karakas_en": "Marital harmony, refined love, vehicles, fine arts, elegance, prosperity & charm"
    },
    "Saturn": {
        "title_hi": "शनि देव (कर्म, न्याय, अनुशासन, वैराग्य व दीर्घायु)",
        "title_en": "Saturn (Shani - Karma, Justice, Endurance, Longevity & Discipline)",
        "karakas_hi": "कर्मफल, न्याय, अनुशासन, धैर्य, आयु, जनसामान्य एवं साधना",
        "karakas_en": "Karmic retribution, discipline, endurance, longevity, public masses & perseverance"
    },
    "Rahu": {
        "title_hi": "राहु देव (कूटनीति, विदेशी संबंध, महत्वाकांक्षा व अचानक प्रगति)",
        "title_en": "Rahu (Chhaya Graha - Ambition, Foreign Realms, Modern Tech & Breakthroughs)",
        "karakas_hi": "आधुनिक तकनीक, विदेशी संबंध, असाधारण महत्वाकांक्षा, शोध एवं आकस्मिक लाभ",
        "karakas_en": "Modern technology, foreign connections, relentless ambition, research & sudden gains"
    },
    "Ketu": {
        "title_hi": "केतु देव (मोक्ष, वैराग्य, गूढ़ अनुसंधान व आध्यात्मिक मुक्ति)",
        "title_en": "Ketu (Mokshakaraka - Spiritual Liberation, Occult Acumen & Renunciation)",
        "karakas_hi": "मोक्ष, वैराग्य, गूढ़ विद्याएं, पराभौतिक ज्ञान, स्वतंत्रता एवं सूक्ष्म दृष्टि",
        "karakas_en": "Spiritual liberation, detachment, occult sciences, metaphysics & piercing intuition"
    }
}

def get_planet_consideration_details(
    p_name: str,
    sign_idx: int,
    house: int,
    dignity_str: str,
    ruled_houses: list,
    aspects_cast: list,
    aspects_rec: list,
    lang: str = "en"
) -> dict:
    core = PLANET_CORE_KARAKAS.get(p_name, PLANET_CORE_KARAKAS["Sun"])
    p_hi = constants.PLANETS_HI.get(p_name, p_name)
    sign_en = constants.SIGNS[sign_idx]
    sign_hi = constants.SIGNS_HI[sign_idx]
    
    ruled_str_en = f"lord of {', '.join(map(str, ruled_houses))} house" if ruled_houses else "natural significator"
    ruled_str_hi = f"{', '.join(map(str, ruled_houses))}वें भाव का स्वामी (भावेश)" if ruled_houses else "प्राकृतिक कारक"
    
    asps_cast_en = ", ".join([f"{h}th" for h in aspects_cast]) or "no major forward aspects"
    asps_cast_hi = ", ".join([f"{h}वें" for h in aspects_cast]) or "सीधी दृष्टि"
    asps_rec_en = ", ".join(aspects_rec) or "neutral celestial influences"
    asps_rec_hi = ", ".join([constants.PLANETS_HI.get(p, p) for p in aspects_rec]) or "सौम्य प्रभाव"

    # Specific Classical In-Depth Paragraphs
    if lang == "hi":
        title = f"{p_hi} विचार ({core['title_hi']})"
        astronomical = (
            f"आपकी जन्म कुण्डली में {p_hi} देव {sign_hi} राशि में स्थित हैं, जो इनके लिए '{dignity_str}' स्थिति है। "
            f"{p_hi} {ruled_str_hi} होकर कुंडली के अत्यंत महत्वपूर्ण {house}वें भाव में विराजमान हैं। "
            f"यहाँ स्थित होकर {p_hi} {asps_cast_hi} भाव पर पूर्ण दृष्टि डाल रहे हैं तथा इन्हें {asps_rec_hi} का दृष्टिगत प्रभाव प्राप्त हो रहा है।"
        )
        shastric_hi_dict = {
            "Sun": f"बृहत्पाराशर होराशास्त्र एवं फलदीपिका के अनुसार, {house}वें भाव में सूर्य की स्थिति जातक को अदम्य आत्मबल, शासकीय व सामाजिक सम्मान तथा नेतृत्व क्षमता प्रदान करती है। {p_hi} का संबंध जातक की आत्मा, पिता एवं कीर्ति से है। जब यह ग्रह अनुकूल स्थिति में हो तो जातक अपने पुरुषार्थ के बल पर समाज में ऊंचा पद प्राप्त करता है। यदि किसी कारणवश प्रतिकूल प्रभाव हो, तो अहंकार एवं नेत्र विकारों से सचेत रहना चाहिए।",
            "Moon": f"चन्द्रमा मनसो जातः - चन्द्रमा मन, कल्पना एवं भावनात्मक स्थिरता का स्वामी है। {house}वें भाव में चन्द्रमा की उपस्थिति जातक को संवेदनशील, विचारवान, लोकप्रिय तथा समाज में आदरणीय बनाती है। जनसंपर्क, जल-तत्व, परामर्श एवं कला के क्षेत्रों में जातक की सहज रुचि रहती है। माता एवं वरिष्ठजनों का आशीर्वाद जीवन में अप्रत्याशित सुख-समृद्धि के द्वार खोलता है।",
            "Mars": f"मंगल शौर्य, साहस, भ्रातृ सुख एवं अचल संपत्ति का कारक है। {house}वें भाव में मंगल की स्थिति जातक को निर्भीक, क्रियाशील, स्वतंत्र उद्यमशील तथा संकटों का डटकर मुकाबला करने वाला बनाती है। कार्यक्षेत्र में अनुशासन एवं दृढ़ संकल्प से जातक उच्च पद प्राप्त करता है। जल्दबाजी व अत्यधिक क्रोध से बचना ही मंगल के शुभ फलों को चिरस्थायी बनाता है।",
            "Mercury": f"बुध बुद्धि, विवेक, तर्क, व्यापार एवं वाणी का अधिपति है। {house}वें भाव में बुध की स्थिति जातक को बहुआयामी मेधावी, वाकपटु, लेखन-दक्ष एवं सफल रणनीतिकार बनाती है। व्यापारिक सौदों, वित्तीय विश्लेषण एवं बौद्धिक परामर्श में जातक को असाधारण लाभ मिलता है। स्पष्ट संवाद एवं नैतिक व्यापारिक दृष्टिकोण सफलता का मूल आधार है।",
            "Jupiter": f"देवगुरु बृहस्पति ज्ञान, धर्म, संतान, ऐश्वर्य एवं ईश्वरीय कृपा के साक्षात स्वरूप हैं। {house}वें भाव में गुरु की उपस्थिति कुण्डली के समस्त दोषों को शांत करने में सक्षम है। यह स्थिति जातक को दार्शनिक, नीतिवान, विद्वान तथा समाज में अत्यंत सम्मानित बनाती है। धर्मपरायणता, गुरु-सेवा एवं परोपकार से जातक निरंतर प्रगति के शिखर पर आरूढ़ होता है।",
            "Venus": f"दैत्यगुरु शुक्र दांपत्य, प्रेम, भौतिक ऐश्वर्य, कला एवं सौंदर्य का कारक है। {house}वें भाव में शुक्र जातक को सुरुचिपूर्ण, आकर्षक, कलाप्रेमी तथा संपन्न जीवनशैली का स्वामी बनाता है। वाहन, उत्तम वस्त्र एवं सुरुचिपूर्ण निवास का सुख सहज रूप से प्राप्त होता है। जीवनसाथी का सहयोग भाग्योदय में विशेष सहायक सिद्ध होता है।",
            "Saturn": f"शनि कर्म, न्याय, वैराग्य एवं तपस्या के अधिष्ठाता हैं। {house}वें भाव में शनि की उपस्थिति जातक को गंभीर, कर्मठ, यथार्थवादी, धैर्यवान एवं जनप्रिय बनाती है। प्रारंभिक जीवन में कड़े संघर्ष के पश्चात जातक अपने दम पर सुदृढ़ साम्राज्य व स्थायी प्रतिष्ठा अर्जित करता है। निर्धनों की सेवा व सत्यनिष्ठा शनि की परम कृपा दिलाती है।",
            "Rahu": f"राहु असीम महत्वाकांक्षा, शोध, आधुनिक तकनीक एवं आकस्मिक भाग्योदय का कारक है। {house}वें भाव में राहु जातक को कूटनीतिक चतुर, लीक से हटकर सोचने वाला तथा विदेशी संपर्कों से लाभ उठाने वाला बनाता है। असाधारण चुनौतियों को पार कर जातक अभूतपूर्व सफलता प्राप्त करता है। भ्रम व व्यसनों से दूरी बनाए रखना श्रेयस्कर है।",
            "Ketu": f"केतु मोक्ष, वैराग्य, पराभौतिक ज्ञान एवं सूक्ष्म अंतर्दृष्टि का प्रतीक है। {house}वें भाव में केतु जातक को आध्यात्मिक, शोधप्रवृत्त, तीव्र अंतर्ज्ञानी तथा आंतरिक शांति का खोजी बनाता है। भौतिक कठिनाइयों को ईश्वर की सीख मानकर जातक अंततः परम शांति व सम्मान प्राप्त करता है। ध्यान एवं साधना से अद्भुत ऊर्जा जागृत होती है।"
        }
        shastric = shastric_hi_dict.get(p_name, f"{p_hi} का यह स्थान जातक को विशिष्ट फल प्रदान करता है।")
        practical = f"दैनिक जीवन में {p_hi} के शुभ प्रभावों को बढ़ाने हेतु नित्य सात्विक दिनचर्या अपनाएं, वरिष्ठों का आदर करें और अपने स्वभाव में संतुलन व धैर्य बनाए रखें।"
        return {"title": title, "astronomical": astronomical, "shastric": shastric, "practical": practical}
    else:
        title = f"{p_name} Consideration ({core['title_en']})"
        astronomical = (
            f"In your natal chart, {p_name} is situated in {sign_en} sign, which constitutes a '{dignity_str}' placement for {p_name}. "
            f"{p_name} functions as {ruled_str_en} and is firmly posited in your {house}th house. "
            f"From this house, {p_name} aspects the {asps_cast_en} house and receives aspectual rays from {asps_rec_en}."
        )
        shastric_en_dict = {
            "Sun": f"According to Brihat Parashara Hora Shastra, Sun's placement in the {house}th house confers radiant vitality, regal authority, and steadfast willpower. The native commands instinctive respect in social and executive circles. When directed with integrity, this placement guarantees lasting prosperity and triumph over adversaries.",
            "Moon": f"The Moon governs mind, memory, and emotional equilibrium. Positioned in the {house}th house, it bestows sensitive perception, public rapport, intuitive imagination, and profound familial empathy. Maintaining calmness and seeking maternal blessings ensures bountiful peace and mental clarity.",
            "Mars": f"Mars is the celestial powerhouse of valor, land, and pioneering enterprise. Its presence in the {house}th house endows the native with athletic stamina, decisive leadership, and courage to conquer daunting obstacles. Disciplined action and patience turn this dynamic energy into monumental achievements.",
            "Mercury": f"Mercury represents intellect, analytical wit, commerce, and persuasive articulation. Posited in the {house}th house, it blesses the native with razor-sharp analytical discernment, trade acumen, and scholarly brilliance. Clear communication and ethical transactions bring continuous commercial elevation.",
            "Jupiter": f"Jupiter is the supreme benefic conferring wisdom, righteousness, progeny, and divine benevolence. Placed in the {house}th house, it shields the native against misfortune, fostering philosophical depth, societal veneration, and material abundance. Upholding ethical principles unlocks its grandest blessings.",
            "Venus": f"Venus symbolizes marital harmony, aesthetic refinements, luxury vehicles, and artistic appreciation. Situated in the {house}th house, it enriches life with gracious elegance, supportive alliances, and financial consolidation. Aesthetic pursuits and mutual respect in partnerships bring lasting bliss.",
            "Saturn": f"Saturn is the great karmic teacher enforcing endurance, justice, and methodical discipline. Posited in the {house}th house, it yields enduring accomplishments after rigorous initial tests. Diligence, humility, and service to the underprivileged awaken Saturn's highest beneficence.",
            "Rahu": f"Rahu embodies visionary ambition, modern technological integration, and unconventional breakthroughs. In the {house}th house, it grants astute worldly diplomacy and sudden material elevation. Channeling its intense focus into disciplined mastery prevents distractions and ensures stellar success.",
            "Ketu": f"Ketu represents spiritual liberation, metaphysical research, and piercing intuition. Situated in the {house}th house, it fosters philosophical detachment, protection from unseen perils, and unique problem-solving capabilities. Meditation and charitable acts bring profound inner tranquility."
        }
        shastric = shastric_en_dict.get(p_name, f"The placement of {p_name} in house {house} exerts a pivotal influence on destiny.")
        practical = f"To optimize the positive vibration of {p_name}, maintain disciplined ethical conduct, honor parental and mentor guidance, and align daily actions with truth."
        return {"title": title, "astronomical": astronomical, "shastric": shastric, "practical": practical}


# ---------------------------------------------------------------------------
# 7. NAVAGRAHA SHANTI & HARMONY SYNTHESIS (FOR PAGE 39 COMPLETION)
# ---------------------------------------------------------------------------
NAVAGRAHA_SHANTI_MATRIX_HI = [
    ("सूर्य", "माणिक्य (Ruby)", "तांबा / स्वर्ण", "ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः", "1 मुखी / 12 मुखी", "गेहूं, गुड़, तांबा, लाल वस्त्र"),
    ("चन्द्र", "मोती (Pearl)", "चांदी", "ॐ श्रां श्रीं श्रौं सः चन्द्रमसे नमः", "2 मुखी", "दूध, चावल, चांदी, सफेद वस्त्र"),
    ("मंगल", "मूंगा (Red Coral)", "तांबा / पंचधातु", "ॐ क्रां क्रीं क्रौं सः भौमाय नमः", "3 मुखी", "मसूर दाल, गुड़, लाल पुष्प, तांबा"),
    ("बुध", "पन्ना (Emerald)", "कांस्य / स्वर्ण", "ॐ ब्रां ब्रीं ब्रौं सः बुधाय नमः", "4 मुखी / 10 मुखी", "हरी मूंग, हरा वस्त्र, कांसा, पुस्तकें"),
    ("गुरु", "पुखराज (Yellow Sapphire)", "स्वर्ण / पीतल", "ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः", "5 मुखी", "चना दाल, हल्दी, पीले फल, स्वर्ण, धार्मिक ग्रंथ"),
    ("शुक्र", "हीरा (Diamond/Opal)", "चांदी / प्लैटिनम", "ॐ द्रां द्रीं द्रौं सः शुक्राय नमः", "6 मुखी / 13 मुखी", "चावल, मिश्री, कपूर, इत्र, रेशमी वस्त्र"),
    ("शनि", "नीलम (Blue Sapphire)", "लोहा / अष्टधातु", "ॐ प्रां प्रीं प्रौं सः शनैश्चराय नमः", "7 मुखी / 14 मुखी", "काले तिल, उड़द, सरसों तेल, लोहा, काला कंबल"),
    ("राहु", "गोमेद (Hessonite)", "रांगा / पंचधातु", "ॐ भ्रां भ्रीं भ्रौं सः राहवे नमः", "8 मुखी", "सप्तधान्य, नारियल, सीसा, नीला वस्त्र"),
    ("केतु", "लहसुनिया (Cat's Eye)", "पंचधातु", "ॐ स्रां स्रीं स्रौं सः केतवे नमः", "9 मुखी", "दोरंगा कंबल, काले तिल, लहसुनिया, श्वान-सेवा")
]

NAVAGRAHA_SHANTI_MATRIX_EN = [
    ("Sun", "Ruby (Manik)", "Copper/Gold", "Om Hraam Hreem Hroum Sah Suryaya Namah", "1 or 12 Mukhi", "Wheat, jaggery, copper, red apparel"),
    ("Moon", "Pearl (Moti)", "Silver", "Om Shraam Shreem Shroum Sah Chandramase Namah", "2 Mukhi", "Milk, rice, silver, white sweets"),
    ("Mars", "Red Coral (Moonga)", "Copper/Panchdhatu", "Om Kraam Kreem Kroum Sah Bhaumaya Namah", "3 Mukhi", "Red lentils, jaggery, copper, red flowers"),
    ("Mercury", "Emerald (Panna)", "Bronze/Gold", "Om Braam Breem Broum Sah Budhaya Namah", "4 or 10 Mukhi", "Green gram, bronze, green cloth, books"),
    ("Jupiter", "Yellow Sapphire (Pukhraj)", "Gold/Brass", "Om Graam Greem Groum Sah Gurave Namah", "5 Mukhi", "Yellow gram, turmeric, yellow flowers, sacred texts"),
    ("Venus", "Diamond/White Opal", "Silver/Platinum", "Om Draam Dreem Droum Sah Shukraya Namah", "6 or 13 Mukhi", "Rice, curd, perfume, camphor, white silk"),
    ("Saturn", "Blue Sapphire (Neelam)", "Iron/Ashtadhatu", "Om Praam Preem Proum Sah Shanaishcharaya Namah", "7 or 14 Mukhi", "Black sesame, mustard oil, iron, black blanket"),
    ("Rahu", "Hessonite (Gomed)", "Lead/Panchdhatu", "Om Bhraam Bhreem Bhroum Sah Rahave Namah", "8 Mukhi", "Seven grains, coconut, lead, blue garments"),
    ("Ketu", "Cat's Eye (Lehsuniya)", "Panchdhatu", "Om Sraam Sreem Sroum Sah Ketave Namah", "9 Mukhi", "Two-colored blanket, sesame, service to stray dogs")
]


# ---------------------------------------------------------------------------
# 8. SADE SATI & KALSARPA EXPANDED DATA
# ---------------------------------------------------------------------------
KALSARPA_12_TYPES = [
    ("1", "Anant Kalsarpa", "1st (Lagna) - 7th", "अनंत कालसर्प", "संघर्ष के उपरांत व्यक्तित्व निखार एवं आत्म-स्वावलंबन"),
    ("2", "Kulik Kalsarpa", "2nd - 8th", "कुलिक कालसर्प", "वाणी संयम एवं वित्तीय नियोजन से अकूत धन संचय"),
    ("3", "Vasuki Kalsarpa", "3rd - 9th", "वासुकि कालसर्प", "अदम्य पराक्रम, भ्रातृ सहयोग एवं भाग्योदय"),
    ("4", "Shankhpal Kalsarpa", "4th - 10th", "शंखपाल कालसर्प", "गृह, भूमि व माता के सुख हेतु धैर्य, कार्यक्षेत्र में यश"),
    ("5", "Padma Kalsarpa", "5th - 11th", "पद्म कालसर्प", "उच्च शिक्षा, गहन अनुसंधान एवं उत्तम संतति"),
    ("6", "Mahapadma Kalsarpa", "6th - 12th", "महापद्म कालसर्प", "शत्रु-विजय, विदेशी सफलता एवं कानूनी विजय"),
    ("7", "Takshak Kalsarpa", "7th - 1st", "तक्षक कालसर्प", "साझेदारी में स्पष्टता एवं दांपत्य सामंजस्य"),
    ("8", "Karkotak Kalsarpa", "8th - 2nd", "कर्कोटक कालसर्प", "गूढ़ रहस्यों की समझ, पैतृक लाभ एवं आध्यात्मिक साधना"),
    ("9", "Shankhachood Kalsarpa", "9th - 3rd", "शंखचूड़ कालसर्प", "धार्मिक यात्राएं, पितृ-आशीर्वाद एवं सतत भाग्य वृद्धि"),
    ("10", "Ghatak Kalsarpa", "10th - 4th", "घातक कालसर्प", "व्यावसायिक सत्ता, प्रशासनिक अधिकार व मान-सम्मान"),
    ("11", "Vishdhar Kalsarpa", "11th - 5th", "विषधर कालसर्प", "विपुल आय, मित्रों का सानिध्य एवं उच्च प्रतिष्ठा"),
    ("12", "Sheshnag Kalsarpa", "12th - 6th", "शेषनाग कालसर्प", "विदेशी प्रतिष्ठा, मोक्ष मार्ग एवं परोपकार")
]

SADE_SATI_P13_ADDON_HI = """
<div class="as-sub-title" style="margin-top: 10px;">शनि साढ़े साती का गहन शास्त्रीय प्रभाव एवं जन्मकालीन शनि स्थिति</div>
<p>
    वैदिक ज्योतिष में शनि देव कर्मफलदाता एवं न्याय के अधिष्ठाता हैं। साढ़े साती का काल जातक के जीवन में परीक्षा, अनुशासन और आत्म-विकास का स्वर्णिम अवसर होता है। जब गोचरस्थ शनि जन्म चन्द्र से 12वें, 1वें अथवा 2वें भाव में भ्रमण करते हैं, तो व्यक्ति के कर्मों का सूक्ष्म लेखा-जोखा होता है। इस कालखंड में धैर्य, सत्य, परोपकार और संयम रखने वाले जातक को शनि देव अपार यश, साम्राज्य और आध्यात्मिक परिपक्वता प्रदान करते हैं।
</p>
<div class="two-col" style="margin-top: 6px;">
    <div class="col-half">
        <div style="font-weight: bold; font-size: 8pt; margin-bottom: 2px;">अष्टकवर्ग एवं गोचर बिंदु विचार</div>
        <p style="font-size: 8pt; margin: 0;">
            यदि चन्द्रमा की राशि एवं उससे द्वादश व द्वितीय भावों में सर्वाष्टकवर्ग (SAV) में 28 या अधिक बिंदु हों, तो साढ़े साती का प्रभाव अत्यंत शुभ, कल्याणकारी और लाभकारी होता है। 22 से कम बिंदु होने पर ही सामयिक सतर्कता की आवश्यकता होती है।
        </p>
    </div>
    <div class="col-half">
        <div style="font-weight: bold; font-size: 8pt; margin-bottom: 2px;">साढ़े साती में क्या करें और क्या न करें</div>
        <p style="font-size: 8pt; margin: 0;">
            <b>करें:</b> वृद्धों व निर्बलों की सेवा, सत्यभाषण, नित्य हनुमान चालीसा का पाठ, पीपल पूजन।<br/>
            <b>न करें:</b> मदिरापान, जुआ, परनिंदा, कर्मचारियों का शोषण एवं अहंकार।
        </p>
    </div>
</div>
<div style="border: 1px solid #000; padding: 4px; margin-top: 6px; background: #fffcf5; font-size: 8pt;">
    <b>अचूक वैदिक शांति उपाय:</b> प्रत्येक शनिवार को संध्या समय पीपल के वृक्ष के नीचे सरसों के तेल का चौमुखा दीपक जलाएं। महाराज दशरथ कृत 'शनि स्तोत्र' का नियमित पाठ करें। शनिवार को काले तिल, काली उड़द एवं लोहे का दान निर्धन श्रमिकों को करें।
</div>
"""

SADE_SATI_P13_ADDON_EN = """
<div class="as-sub-title" style="margin-top: 10px;">Deep Classical Shani Sade Sati Impact & Natal Saturn Analysis</div>
<p>
    In Vedic astrology, Lord Saturn (Shani) represents karma, divine justice, and profound transformation. The 7.5-year cycle of Sade Sati occurs when transiting Saturn passes through the 12th, 1st, and 2nd houses from the natal Moon. Rather than causing unconditional hardship, Saturn acts as a compassionate preceptor, pruning illusions, refining character, and laying the groundwork for monumental long-term stability and executive stature.
</p>
<div class="two-col" style="margin-top: 6px;">
    <div class="col-half">
        <div style="font-weight: bold; font-size: 8pt; margin-bottom: 2px;">Ashtakavarga & Transit Bindu Evaluation</div>
        <p style="font-size: 8pt; margin: 0;">
            When the natal Moon's sign and its adjacent houses contain 28+ auspicious bindus in Sarvashtakavarga (SAV), Sade Sati operates as a highly productive golden era of consolidation. Only scores below 22 warrant deliberate patience.
        </p>
    </div>
    <div class="col-half">
        <div style="font-weight: bold; font-size: 8pt; margin-bottom: 2px;">Prescribed Do's & Don'ts</div>
        <p style="font-size: 8pt; margin: 0;">
            <b>Do:</b> Serve elderly and underprivileged persons, maintain strict integrity, recite Hanuman Chalisa.<br/>
            <b>Don't:</b> Indulge in intoxicants, speculative gambles, arrogance, or mistreating subordinates.
        </p>
    </div>
</div>
<div style="border: 1px solid #000; padding: 4px; margin-top: 6px; background: #fffcf5; font-size: 8pt;">
    <b>Authentic Classical Remedies:</b> Light a mustard oil lamp under a Peepal tree after sunset on Saturdays. Recite King Dasharatha's Shani Stotra regularly. Donate black sesame, whole urad dal, and iron articles to needy laborers.
</div>
"""


# ---------------------------------------------------------------------------
# 9. LIFE PREDICTIONS ENRICHED CONTENT (FOR PAGES 6-9 BALANCED DISTRIBUTION)
# ---------------------------------------------------------------------------
LIFE_SECTIONS_HI = {
    "character": {
        "title": "व्यक्तित्व एवं चरित्र विश्लेषण",
        "text": "आपका चरित्र सिद्धांतों पर आधारित एवं अत्यंत प्रभावशाली है। आपके भीतर स्वाभाविक आत्मबल, स्पष्टवादिता और नेतृत्व क्षमता विद्यमान है। आप किसी भी परिस्थिति में अपना विवेक नहीं खोते तथा सत्य और न्याय का पक्ष लेते हैं। मित्रों एवं परिवार के प्रति आपकी निष्ठा अटूट रहती है। आपका व्यक्तित्व दूसरों को स्वतः प्रेरित करने की क्षमता रखता है।"
    },
    "happiness": {
        "title": "सुख, संतोष एवं मानसिक शांति",
        "text": "आप एक आदर्शवादी और स्वाभाविक आध्यात्मिक आस्था से संपन्न व्यक्ति हैं। आपकी आंतरिक संवेदनशीलता आपको अत्यंत लोकप्रिय बनाती है और आप दूसरों की भावनाओं का सदैव आदर करते हैं। जीवन की कठिनाइयों को आप परिपक्व होने की दिव्य सीख मानते हैं। आपका वास्तविक सुख भौतिक संग्रह की अपेक्षा मानसिक शांति, परिवार के कल्याण एवं सत्कर्मों में निहित है।"
    },
    "lifestyle": {
        "title": "जीवन शैली एवं महत्वाकांक्षा",
        "text": "आप अपनी व्यक्तिगत और भौतिक स्थिति को निरंतर उन्नत करने हेतु प्रेरित रहते हैं। जीवन में उत्कृष्टता प्राप्त करना आपकी स्वाभाविक प्रेरणा है। आप सुरुचिपूर्ण, अनुशासित और व्यवस्थित जीवनशैली पसंद करते हैं। इस महत्वाकांक्षा को सकारात्मक दिशा में नियोजित कर आप जीवन के सभी भौतिक सुख-साधनों को सहजता से प्राप्त करने में समर्थ हैं।"
    },
    "occupation": {
        "title": "उपयुक्त आजीविका एवं व्यावसायिक क्षेत्र",
        "text": "आप एकरस और नीरस दिनचर्या वाले कार्यों के लिए नहीं बने हैं। आपकी बहुआयामी प्रतिभा एवं विश्लेषणात्मक मेधा आपको उच्च पदों पर स्थापित करती है। आपके लिए कानून, चिकित्सा, प्रशासनिक सेवाएं, तकनीकी परामर्श, अनुसंधान, उच्च प्रबंधन, वित्त एवं स्वतंत्र व्यापार के क्षेत्र अत्यंत लाभप्रद सिद्ध होंगे। आपकी दूरदर्शिता आपको व्यावसायिक जगत में विशिष्ट पहचान दिलाती है।"
    },
    "hobbies": {
        "title": "रुचियां, कला एवं बौद्धिक अभिरुचियां",
        "text": "भ्रमण, खुली प्रकृति में समय व्यतीत करना तथा नए ज्ञान की खोज आपकी प्रमुख रुचियां हैं। आप पुस्तकों, गूढ़ अनुसंधान, इतिहास एवं नवीन तकनीकों के अध्ययन में गहरा रस लेते हैं। कला, संस्कृति और रचनात्मक गतिविधियों से जुड़कर आपका मन प्रफुल्लित रहता है और यही आपके तनाव-मुक्ति का प्रमुख साधन भी है।"
    },
    "finance": {
        "title": "धन, संपत्ति एवं आर्थिक संपन्नता",
        "text": "आप दूसरों की सहायता पर निर्भर रहने की अपेक्षा स्वयं अपने भाग्य के निर्माता हैं। वित्तीय मामलों में आपकी तीव्र बुद्धि, विवेक और दूरदर्शिता आपको विपुल धन संचय के स्वर्णिम अवसर प्रदान करेगी। अचल संपत्ति, भूमि-भवन एवं दीर्घकालिक निवेश से प्रचुर लाभ होगा। आवेगपूर्ण खर्चों पर नियंत्रण रखकर आप एक अत्यंत समृद्ध और सुदृढ़ साम्राज्य स्थापित करेंगे।"
    },
    "education": {
        "title": "विद्या, अध्ययन एवं बौद्धिक विकास",
        "text": "आपकी मेधा गूढ़ एवं असाधारण विषयों को सरलता से आत्मसात करने में सक्षम है। चतुर्विंशांश (D24) एवं पंचम भाव का प्रभाव दर्शाता है कि उच्च शिक्षा में प्रारंभिक बाधाओं के उपरांत आप उत्कृष्ट सफलता अर्जित करेंगे। विश्लेषणात्मक चिंतन, तकनीकी दक्षता और निरंतर स्वाध्याय से आप अपने विषय के शीर्ष विशेषज्ञ के रूप में प्रतिष्ठा प्राप्त करेंगे।"
    }
}

LIFE_SECTIONS_EN = {
    "character": {
        "title": "Character & Core Temperament",
        "text": "You possess great force, dignified integrity, and commanding initiative. Straightforward and authentic in articulation, you despise deceit and command instinctive respect. Your natural leadership, unwavering resilience, and steadfast commitment to high ethical ideals make you a pillar of strength to associates."
    },
    "happiness": {
        "title": "Happiness And Inner Fulfillment",
        "text": "You are idealistic and inspiring to others, endowed with inherent spiritual faith. Sensitive and considerate, your greatest joy arises from purposeful service, mental tranquility, and witnessing the prosperity of loved ones. You view challenges as stepping stones toward total self-mastery."
    },
    "lifestyle": {
        "title": "Lifestyle & Ambition",
        "text": "You are deeply motivated to elevate your personal, familial, and material standards. Your core driving force is an unrelenting desire for excellence. By channeling this constructive ambition into structured enterprise, you effortlessly secure both worldly comforts and societal veneration."
    },
    "occupation": {
        "title": "Suitable Vocations & Professional Avenues",
        "text": "You are best suited for high-stakes leadership and specialized fields that reward innovation rather than routine monotony. High suitability exists in executive management, law, advisory consulting, medicine, administrative governance, technology, and strategic enterprise."
    },
    "hobbies": {
        "title": "Hobbies & Creative Pursuits",
        "text": "Outdoor exploration, scenic travel, and educational expeditions invigorate your spirit. You have a profound appetite for literary research, technological exploration, and philosophy. Immersing in intellectual hobbies provides rejuvenation and emotional balance."
    },
    "finance": {
        "title": "Wealth Accumulation & Financial Destiny",
        "text": "You are destined to be the master architect of your own fortune. Your shrewd commercial intellect and intuitive timing unlock abundant avenues for asset creation. Substantial wealth accrues through immovable property and systematic investments. Restraining impulsive expenses guarantees lasting financial sovereignty."
    },
    "education": {
        "title": "Education, Intellect & Higher Learning",
        "text": "You possess a penetrating intellect capable of mastering intricate and esoteric subjects. Supported by your D24 Chaturvimshamsha alignment, early scholastic hurdles give way to brilliant scholarly achievements. Dedication and continuous research establish you as an authoritative domain specialist."
    }
}


# ---------------------------------------------------------------------------
# 10. PAGE 56 GRAND VEDIC SYNTHESIS (EXECUTIVE CONCLUSION & BLESSINGS)
# ---------------------------------------------------------------------------
PAGE_56_MASTER_SYNTHESIS_HI = """
<div style="border: 2px double #8b0000; padding: 14px 18px; background: #fffcf5; margin-bottom: 12px;">
    <div style="font-size: 14pt; font-weight: 800; color: #8b0000; text-align: center; margin-bottom: 4px;">
        || वैदिक महा-निष्कर्ष एवं समग्र जीवन दिशा-निर्देश ||
    </div>
    <div style="font-size: 9pt; color: #444444; text-align: center; margin-bottom: 12px;">
        महर्षि पराशर, जैमिनी एवं भृगु संहिता के प्रामाणिक सिद्धांतों पर आधारित समग्र जीवन सार
    </div>

    <div style="font-weight: bold; font-size: 9.5pt; color: #1a365d; margin-bottom: 3px;">1. जीवन के चार पुरुषार्थ का समन्वय</div>
    <p style="font-size: 8.5pt; margin-bottom: 6px;">
        आपकी कुण्डली धर्म (1, 5, 9), अर्थ (2, 6, 10), काम (3, 7, 11) एवं मोक्ष (4, 8, 12) त्रिकोणों का एक अत्यंत दुर्लभ व संतुलित समन्वय प्रस्तुत करती है। दशम भाव की प्रबलता कर्म-प्रधान जीवन को इंगित करती है, जहाँ आपका पुरुषार्थ ही आपकी वास्तविक शक्ति है।
    </p>

    <div style="font-weight: bold; font-size: 9.5pt; color: #1a365d; margin-bottom: 3px;">2. भाग्योदय काल एवं स्वर्णिम दशा अवधियां</div>
    <p style="font-size: 8.5pt; margin-bottom: 6px;">
        जीवन के 28वें, 36वें एवं 42वें वर्ष विशेष भाग्योदयकारी सिद्ध होते हैं। वर्तमान महादशा एवं अंतर्दशा के अंतर्गत संयमपूर्वक किए गए दीर्घकालिक प्रयास अप्रत्याशित प्रतिष्ठा एवं आर्थिक स्थायित्व प्रदान करेंगे। गुरु एवं शुक्र के शुभ गोचर सदैव आपके लिए नए अवसर लाएंगे।
    </p>

    <div style="font-weight: bold; font-size: 9.5pt; color: #1a365d; margin-bottom: 3px;">3. नित्य कल्याणकारी साधना एवं जीवन-मंत्र</div>
    <p style="font-size: 8.5pt; margin-bottom: 6px;">
        • <b>दैनिक साधना:</b> प्रातः सूर्यदेव को तांबे के पात्र से जल अर्पित करें तथा नित्य श्री हनुमान चालीसा अथवा गायत्री मंत्र का जप करें।<br/>
        • <b>माता-पिता सेवा:</b> नित्य माता-पिता व गुरुजनों के चरण स्पर्श कर आशीर्वाद लें; यह नवग्रह शांति का सर्वश्रेष्ठ उपाय है।<br/>
        • <b>दान एवं सेवा:</b> शनिवार को निर्धनों को भोजन एवं जल दान करें। मूक पक्षियों व गौमाता की नियमित सेवा करें।
    </p>

    <div style="text-align: center; margin: 10px 0; padding: 8px; background: #ffffff; border: 1px dashed #8b0000;">
        <div style="font-size: 10.5pt; font-weight: bold; color: #8b0000; margin-bottom: 2px;">
            ॐ द्यौः शान्तिरन्तरिक्षं शान्तिः पृथिवी शान्तिरापः शान्तिरोषधयः शान्तिः ।<br/>
            वनस्पतयः शान्तिर्विश्वेदेवाः शान्तिर्ब्रह्म शान्तिः सर्वं शान्तिः शान्तिरेव शान्तिः सा मा शान्तिरेधि ॥<br/>
            ॥ ॐ शान्तिः शान्तिः शान्तिः ॥
        </div>
        <div style="font-size: 8pt; color: #555555; margin-top: 3px;">
            ईश्वर आपको उत्तम स्वास्थ्य, सुदीर्घायु, विपुल ऐश्वर्य एवं निरंतर कीर्ति प्रदान करें।
        </div>
    </div>
</div>

<div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #000000; padding-top: 8px; font-size: 8pt;">
    <div>
        <b>व्यास ज्योतिष अनुसंधान संस्थान (VYAS ASTRA)</b><br/>
        वैदिक गणित एवं उच्च खगोलीय संगणना परिषद<br/>
        प्रमाणित पराशरी एवं जैमिनी अनुसंधान मानक
    </div>
    <div style="text-align: right;">
        <b>शुभम भवतु • कल्याणम अस्तु</b><br/>
        Classical Vedic Astrology Intelligence<br/>
        ISO/IEC Gold Standard Astrological Dossier
    </div>
</div>
"""

PAGE_56_MASTER_SYNTHESIS_EN = """
<div style="border: 2px double #1a365d; padding: 14px 18px; background: #f8fafc; margin-bottom: 12px;">
    <div style="font-size: 14pt; font-weight: 800; color: #1a365d; text-align: center; margin-bottom: 4px;">
        || Grand Vedic Synthesis & Final Life Directives ||
    </div>
    <div style="font-size: 9pt; color: #4a5568; text-align: center; margin-bottom: 12px;">
        Authoritative Executive Synthesis as per Maharishi Parashara, Jaimini and Bhrigu Traditions
    </div>

    <div style="font-weight: bold; font-size: 9.5pt; color: #8b0000; margin-bottom: 3px;">1. Harmonious Synthesis of the Four Purusharthas</div>
    <p style="font-size: 8.5pt; margin-bottom: 6px;">
        Your horoscope harmoniously integrates the quadruplicate goals of human existence: Dharma (Righteousness), Artha (Wealth), Kama (Desire), and Moksha (Spiritual Liberation). The pronounced strength of your Kendra and Trikona houses establishes you as a purposeful karmic pioneer whose focused actions manifest immense destiny.
    </p>

    <div style="font-weight: bold; font-size: 9.5pt; color: #8b0000; margin-bottom: 3px;">2. Golden Milestones & Auspicious Dasha Windows</div>
    <p style="font-size: 8.5pt; margin-bottom: 6px;">
        Auspicious milestones are highlighted in the 28th, 36th, 42nd, and 48th years. Systematic perseverance undertaken during the running planetary periods guarantees commanding status, substantial immovable assets, and enduring societal reverence.
    </p>

    <div style="font-weight: bold; font-size: 9.5pt; color: #8b0000; margin-bottom: 3px;">3. Prescribed Daily Practices & Core Life Rules</div>
    <p style="font-size: 8.5pt; margin-bottom: 6px;">
        • <b>Daily Sadhana:</b> Offer water to the rising Sun in a copper vessel, followed by contemplation of the Gayatri Mantra or Hanuman Chalisa.<br/>
        • <b>Honoring Lineage:</b> Revere parents and mentors daily; parental blessings neutralize conflicting planetary radiations effortlessly.<br/>
        • <b>Charitable Deeds:</b> Support destitute laborers, provide grains to birds, and protect sacred cows to awaken universal planetary grace.
    </p>

    <div style="text-align: center; margin: 10px 0; padding: 8px; background: #ffffff; border: 1px dashed #1a365d;">
        <div style="font-size: 10pt; font-weight: bold; color: #1a365d; margin-bottom: 2px;">
            Om Dyauh Shaantir-Antariksham Shaantih Prithivee Shaantir-Aapah Shaantir-Oshadhayah Shaantih ।<br/>
            Vanaspatayah Shaantir-Vishvedevaah Shaantir-Brahma Shaantih Sarvam Shaantih Shaantir-Eva Shaantih Saa Maa Shaantir-Edhi ॥<br/>
            ॥ Om Shaantih Shaantih Shaantih ॥
        </div>
        <div style="font-size: 8pt; color: #4a5568; margin-top: 3px;">
            May the Supreme Divine grant you robust health, monumental longevity, boundless honor, and serene fulfillment.
        </div>
    </div>
</div>

<div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #000000; padding-top: 8px; font-size: 8pt;">
    <div>
        <b>VYAS ASTRA Astrological Research Council</b><br/>
        Vedic Mathematics & High-Precision Astronomical Observatory<br/>
        Accredited Parashari & Jaimini Computational Standard
    </div>
    <div style="text-align: right;">
        <b>May All Auspiciousness Prevail</b><br/>
        Classical Vedic Astrology Intelligence<br/>
        ISO/IEC Gold Standard Astrological Dossier
    </div>
</div>
"""
