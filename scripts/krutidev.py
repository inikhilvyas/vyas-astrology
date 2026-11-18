# -*- coding: utf-8 -*-
"""
KrutiDev 010 to Unicode Hindi Converter
"""

def krutidev_to_unicode(text):
    if not text:
        return ""
    
    # Standard replacement pairs
    modified_substring = text
    
    # Basic replacements
    replacements = [
        ("ñ", "ह्न"), ("ò", "ह्र"), ("ó", "ह्ल"), ("ô", "ह्व"),
        ("õ", "हृ"), ("ö", "ह्म"), ("÷", "ह्य"),
        ("à", "अ"), ("á", "आ"), ("â", "इ"), ("ã", "ई"),
        ("ä", "उ"), ("å", "ऊ"), ("æ", "ऋ"),
        ("ç", "ए"), ("è", "ऐ"), ("é", "ओ"), ("ê", "औ"),
        ("ë", "क"), ("ì", "ख"), ("í", "ग"), ("î", "घ"), ("ï", "ङ"),
        ("ð", "च"),
        ("‘", "'"), ("’", "'"), ("“", '"'), ("”", '"'),
        ("=", "ं"), ("v", "अ"), ("vks", "ओ"), ("vkS", "औ"),
        ("vk", "आ"), ("bZ", "ई"), ("b", "इ"), ("m", "उ"),
        ("Å", "ऊ"), (",", "ए"), ("S", "ऐ"), ("_", "ऋ"),
        ("d", "क"), ("[k", "ख"), ("x", "ग"), ("?k", "घ"), ("³", "ङ"),
        ("p", "च"), ("N", "छ"), ("t", "ज"), ("Tk", "झ"), ("¥", "ञ"),
        ("V", "ट"), ("B", "ठ"), ("M", "ड"), ("<", "ढ"), (">", "ढ़"),
        (".k", "ण"),
        ("r", "त"), ("Fk", "थ"), ("n", "द"), ("/k", "ध"), ("u", "न"),
        ("i", "प"), ("Q", "फ"), ("c", "ब"), ("Hk", "भ"), ("e", "म"),
        (";", "य"), ("j", "र"), ("y", "ल"), ("o", "व"), ("k", "ा"),
        ("l", "स"), ("g", "ह"), ("'", "श"), ("\"", "ष"),
        ("K", "ज्ञ"), ("=", "ं"), ("a", "ं"), ("¡", "ँ"),
        ("%", "ः"), ("A", "।"), ("ñ", "्"), ("~", "्"),
        ("q", "ु"), ("w", "ू"), ("`", "ृ"), ("s", "े"), ("S", "ै"),
        ("ks", "ो"), ("kS", "ौ"), ("W", "ॅ"),
        ("Z", "्र"), ("Í", "्र"), ("ç", "प्र"),
        ("R", "्"), ("ीं", "ीं"),
        ("¿", "?"), ("¼", "("), ("½", ")"), ("@", "ध"),
        ("Ø", "क्र"), ("é", "न्न"), ("Í", "्र"),
        ("ä", "क्त"), ("D", "क्"), ("X", "ग्"),
        ("T", "ज्"), ("Y", "ल्"), ("O", "व्"),
        ("L", "स्"), ("J", "श्र"), ("z", "्र")
    ]
    
    # Apply replacements
    for k, v in replacements:
        modified_substring = modified_substring.replace(k, v)
        
    # Re-order 'f' (matra 'i')
    # in KrutiDev, 'f' comes BEFORE the consonant, in Unicode 'ि' comes AFTER
    import re
    # Fix choti 'i' matra
    modified_substring = re.sub(r'f([\u0900-\u097F])', r'\1ि', modified_substring)
    
    return modified_substring

if __name__ == '__main__':
    sample = "1 vkJ; ;ksx - jTtq;ksx\npj jkf'k esa lHkh xzg gksa rks jTtq;ksx gksrk gSA"
    print("Converted:", krutidev_to_unicode(sample))

