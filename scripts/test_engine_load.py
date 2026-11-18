# -*- coding: utf-8 -*-
import os
import re

def generate_update():
    # 1. Load engine JS from build_comprehensive_vyas_update.py
    with open('scripts/build_comprehensive_vyas_update.py', 'r', encoding='utf-8') as f:
        src = f.read()

    start_m = src.find('computeMathematicalKundli(name, dobStr')
    end_m = src.rfind('},"""')
    engine_js = src[start_m:end_m + 1].strip()

    print(f"Loaded engine JS: {len(engine_js)} chars")
    return engine_js

if __name__ == '__main__':
    generate_update()
