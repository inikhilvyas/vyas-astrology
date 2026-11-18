with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

import re
unsafe_pattern = re.compile(r'this\.activeChartData\.([a-zA-Z0-9_]+)')

for i, l in enumerate(lines):
    if 'this.activeChartData.' in l:
        # check if preceded by this.activeChartData &&
        if 'this.activeChartData &&' not in l and '!this.activeChartData' not in l and 'this.activeChartData ?' not in l and 'if (this.activeChartData)' not in l and 'if (!this.activeChartData)' not in l:
            # print suspicious lines
            print(f'Line {i+1}: {l.strip()[:100]}')

