with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('updateDailyHoroscopeUI() {')
# find next function in VyasDesktop
import re
match = re.search(r'\n\s*([a-zA-Z0-9_]+)\s*\([^)]*\)\s*\{', text[pos+200:])
if match:
    next_fn = match.group(1)
    end = pos + 200 + match.start()
    print(f"updateDailyHoroscopeUI runs from {pos} to {end}, next function is {next_fn}")
    print("--- Tail of updateDailyHoroscopeUI ---")
    print(text[end-400:end])

