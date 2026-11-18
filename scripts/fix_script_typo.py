with open('scripts/master_fix_degrees_phalit_and_theme.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("html = html.replace('activeChartData: null,', 'activeChartData: null,\\n' + authenticSwissPlanets_js)", "html = html.replace('activeChartData: null,', 'activeChartData: null,\\n' + authentic_planets_js)")

with open('scripts/master_fix_degrees_phalit_and_theme.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed variable name!")
