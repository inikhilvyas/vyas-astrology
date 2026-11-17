with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
unsafe_lines = []
for idx, line in enumerate(lines):
    if 'this.activeChartData.' in line:
        # Check if line or preceding 3 lines have a guard
        context = '\n'.join(lines[max(0, idx-4):idx+1])
        has_guard = ('!this.activeChartData' in context or 
                     'this.activeChartData &&' in context or 
                     'if (this.activeChartData' in context or
                     '? this.activeChartData.' in context)
        if not has_guard:
            unsafe_lines.append((idx + 1, line.strip()))

print(f"Found {len(unsafe_lines)} potentially unguarded accesses to this.activeChartData:")
for lnum, ltext in unsafe_lines:
    print(f"L{lnum}: {ltext}")

