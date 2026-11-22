import os, re, json

def audit_all_subsystems():
    results = {}

    # 1. Audit Google Login and Default Kundli loading in index.html
    with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    results['google_login'] = {
        'has_gsi_script': 'accounts.google.com/gsi/client' in html,
        'has_google_client_id': 'googleClientId' in html or 'client_id' in html,
        'has_credential_response_handler': 'handleCredentialResponse' in html or 'onGoogleSignIn' in html,
        'has_auto_load_default_kundli': 'loadDefaultKundli' in html or 'default_kundli' in html or 'vyas_active_profile' in html,
        'auth_methods': re.findall(r'function\s+(?:handleGoogle|onGoogle|initGoogle|login|logout)[a-zA-Z0-9_]*\s*\(', html)
    }

    # 2. Audit Chat Bot and Groq / LLM API
    results['ai_chat'] = {
        'has_groq_api': 'groq.com' in html or 'GROQ_API_KEY' in html or 'gsk_' in html,
        'has_api_chat_php': 'api/chat.php' in html or 'chat.php' in html,
        'has_format_reading_fallback': 'formatReading' in html,
        'has_timeout_handling': 'timeout' in html or 'AbortController' in html,
        'chat_functions': re.findall(r'function\s+(?:sendChatMessage|askDaivagya|callGroq|formatReading)[a-zA-Z0-9_]*\s*\(', html)
    }

    # 3. Audit Payment & Pro Monetization
    results['payments'] = {
        'has_razorpay': 'razorpay' in html.lower(),
        'has_stripe': 'stripe' in html.lower(),
        'has_upi': 'upi://' in html or 'upi' in html.lower(),
        'pro_modal_ids': re.findall(r'id=[\'"][^\'"]*pro[^\'"]*[\'"]', html, re.I),
        'payment_functions': re.findall(r'function\s+[a-zA-Z0-9_]*(?:pay|pro|subscribe|checkout|billing)[a-zA-Z0-9_]*\s*\(', html, re.I)
    }

    # 4. Audit PDF Generation
    results['pdf_generation'] = {
        'has_html2pdf': 'html2pdf' in html.lower(),
        'has_jspdf': 'jspdf' in html.lower(),
        'has_print_css': '@media print' in html,
        'pdf_functions': re.findall(r'function\s+[a-zA-Z0-9_]*(?:pdf|print|dossier|report)[a-zA-Z0-9_]*\s*\(', html, re.I)
    }

    # 5. Audit Astronomical & Divisional Charts (Vargas up to D-150)
    with open('js/vyas_astronomical_engine.js', 'r', encoding='utf-8', errors='ignore') as f:
        ast_code = f.read()

    vargas_found = re.findall(r'D-?[0-9]+|varga|shodashavarga|nadiamsha', ast_code, re.I)
    results['astronomical_vargas'] = {
        'file_size_kb': len(ast_code) // 1024,
        'vargas_mentions': list(set(vargas_found))[:20],
        'has_d60': 'D60' in ast_code or 'D-60' in ast_code or 'shashtiamsha' in ast_code.lower(),
        'has_d150': 'D150' in ast_code or 'D-150' in ast_code or 'nadiamsha' in ast_code.lower(),
        'ayanamsa_types': re.findall(r'ayanamsa|lahiri|raman|kp|true_chitra', ast_code, re.I)
    }

    # 6. Audit Books & Sutras Bank Ingestion
    sutras_path = 'js/vyas_sutras_bank.js'
    has_sutras_bank = os.path.exists(sutras_path)
    sutras_size_kb = os.path.getsize(sutras_path) // 1024 if has_sutras_bank else 0
    books_files = [f for f in os.listdir('books') if f.endswith('.md') or f.endswith('.txt')] if os.path.exists('books') else []

    results['data_bank'] = {
        'has_sutras_bank_js': has_sutras_bank,
        'sutras_bank_kb': sutras_size_kb,
        'books_folder_count': len(books_files),
        'books_sample': books_files[:10]
    }

    # 7. Audit Android Native App
    results['android_app'] = {
        'exists': os.path.exists('android_app'),
        'has_build_gradle': os.path.exists('android_app/app/build.gradle.kts'),
        'has_manifest': os.path.exists('android_app/app/src/main/AndroidManifest.xml'),
        'has_keystore_script': os.path.exists('android_app/generate_keystore.bat'),
        'has_build_aab_script': os.path.exists('android_app/build_release_aab.bat')
    }

    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    audit_all_subsystems()

