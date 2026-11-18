# -*- coding: utf-8 -*-
"""
Patch Daivagya Wisdom Engine into index.html and mobile/index.html
"""
import re
from generate_daivagya_wisdom_js import generate_daivagya_wisdom_js

wisdom_code = generate_daivagya_wisdom_js()

def patch_file(filepath, is_mobile=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Inject VyasDaivagyaWisdom before VyasDaivagyaVision or VyasAIEngine
    if "var VyasDaivagyaWisdom =" not in content:
        # Find window.VyasAIEngine or global.VyasDaivagyaVision
        marker = "window.VyasAIEngine ="
        if marker in content:
            idx = content.find(marker)
            content = content[:idx] + wisdom_code + "\n\n    " + content[idx:]
            print(f"[{filepath}] Injected VyasDaivagyaWisdom before window.VyasAIEngine")
        else:
            print(f"[{filepath}] Warning: window.VyasAIEngine marker not found!")

    # 2. Update synthesizeHolisticReading inside VyasDaivagyaVision
    # Find synthesizeHolisticReading: function(query, chart) {
    shr_marker = "synthesizeHolisticReading: function(query, chart) {"
    if shr_marker in content:
        # Replace the body of synthesizeHolisticReading
        idx = content.find(shr_marker)
        # Find closing of this function
        # We can simply replace the top of this function:
        replacement = """synthesizeHolisticReading: function(query, chart) {
            if (window.VyasDaivagyaWisdom && window.VyasDaivagyaWisdom.synthesizeReading) {
                return window.VyasDaivagyaWisdom.synthesizeReading(query, chart);
            }"""
        # Let's find end of the old function
        # Old function ends right before `};\n\n    global.VyasDaivagyaVision = VyasDaivagyaVision;`
        end_marker = "global.VyasDaivagyaVision = VyasDaivagyaVision;"
        if end_marker in content:
            end_idx = content.find(end_marker, idx)
            # Find the last `};` before end_marker
            last_brace = content.rfind("};", idx, end_idx)
            if last_brace != -1:
                old_func = content[idx:last_brace]
                new_func = """synthesizeHolisticReading: function(query, chart) {
            if (typeof VyasDaivagyaWisdom !== 'undefined' && VyasDaivagyaWisdom.synthesizeReading) {
                return VyasDaivagyaWisdom.synthesizeReading(query, chart);
            }
            if (window.VyasDaivagyaWisdom && window.VyasDaivagyaWisdom.synthesizeReading) {
                return window.VyasDaivagyaWisdom.synthesizeReading(query, chart);
            }
            return "<b>आचार्य व्यास:</b> कुण्डली का शास्त्रीय वेध जारी है...";
        }"""
                content = content[:idx] + new_func + "\n    " + content[last_brace:]
                print(f"[{filepath}] Replaced synthesizeHolisticReading with VyasDaivagyaWisdom delegation!")

    # 3. In VyasAIEngine.askSage, ensure fallback calls VyasDaivagyaWisdom
    old_fallback = "return this.generateDynamicLocalReply(query, activeChart);"
    new_fallback = """if (typeof VyasDaivagyaWisdom !== 'undefined' && VyasDaivagyaWisdom.synthesizeReading) {
                return VyasDaivagyaWisdom.synthesizeReading(query, activeChart);
            }
            return this.generateDynamicLocalReply(query, activeChart);"""
    if old_fallback in content:
        content = content.replace(old_fallback, new_fallback)
        print(f"[{filepath}] Patched askSage fallback to use VyasDaivagyaWisdom directly!")

    # 4. Remove any remaining superstitious or "वत्स" phrases
    bad_phrases = [
        ("वत्स ", "आदरणीय "),
        ("वत्स!", "जी!"),
        ("घर की मुख्य दीवार घड़ी को ठीक 11 मिनट आगे रखें", "प्रातःकाल सूर्यनारायण को शुद्ध जल से अर्घ्य दें"),
        ("11 लाल मिर्च के बीज", "रक्त चन्दन अथवा कुमकुम"),
        ("दीवार घड़ी का काल-संरेखण", "प्रातः कालीन सूर्य ध्यान")
    ]
    for b, r in bad_phrases:
        if b in content:
            count = content.count(b)
            content = content.replace(b, r)
            print(f"[{filepath}] Replaced bad phrase '{b}' ({count} occurrences)")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[{filepath}] Successfully saved!")

if __name__ == '__main__':
    patch_file('index.html')
    patch_file('mobile/index.html', is_mobile=True)
