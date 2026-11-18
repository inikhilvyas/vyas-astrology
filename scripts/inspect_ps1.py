for ps in ['scripts/push_to_origin.ps1', 'scripts/push_to_inikhil.ps1']:
    try:
        with open(ps, 'r', encoding='utf-8') as f:
            print(f"=== {ps} ===")
            print(f.read())
    except Exception as e:
        print(f"Error reading {ps}: {e}")

