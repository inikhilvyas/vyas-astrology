# -*- coding: utf-8 -*-
import re

with open('mobile/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract methods of VyasMobile
with open('mobile/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

body = "".join(lines[5575:8819])

methods_to_check = [
    'renderMobileKundliPlanets',
    'updateMobileDynamicUI',
    'renderChart',
    'renderPlanetTable',
    'renderPanchang',
    'renderPredictions',
    'renderAshtakavarga',
    'renderGochar',
    'renderKP',
    'renderJaimini',
    'renderNadi',
    'renderSphutas',
    'renderVarga',
    'renderDashaTree',
    'renderShadbala',
    'renderMatch',
    'renderRemedies',
    'renderPrashna',
    'renderLalKitab',
    'renderTajika'
]

for method in methods_to_check:
    has_method = f"{method}:" in body or f"{method}(" in body
    print(f"Method '{method}': {has_method}")
