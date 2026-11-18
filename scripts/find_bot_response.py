# -*- coding: utf-8 -*-
import os

targets = ['अंतिम आश्वासन', 'गुप्त-शत्रु-योग', '31 जनवरी 2025', '31 जनवरी']
found = False
for root, dirs, files in os.walk('.'):
    for skip in ['.git', '.venv311', 'node_modules', 'books']:
        if skip in dirs:
            dirs.remove(skip)
    for f in files:
        if f.endswith(('.js', '.html', '.py', '.json', '.php', '.md')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                    for t in targets:
                        if t in content:
                            print(f'FOUND "{t}" in: {p}')
                            found = True
            except Exception:
                pass

if not found:
    print('No target text found in codebase files.')

