with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

bad = "var pindas = (this.activeChartData.ashtakavarga && this.activeChartData.ashtakavarga.pindas) ? this.activeChartData.ashtakavarga.pindas : (window.AUTHENTIC_BUNDLE && window.AUTHENTIC_BUNDLE.ashtakavarga ? window.AUTHENTIC_BUNDLE.ashtakavarga.pindas : null);"
good = "var pindas = (this.activeChartData && this.activeChartData.ashtakavarga && this.activeChartData.ashtakavarga.pindas) ? this.activeChartData.ashtakavarga.pindas : (window.AUTHENTIC_BUNDLE && window.AUTHENTIC_BUNDLE.ashtakavarga ? window.AUTHENTIC_BUNDLE.ashtakavarga.pindas : null);"

if bad in content:
    content = content.replace(bad, good)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("FIXED: Successfully guarded activeChartData in renderPavTable!")
else:
    print("NOT FOUND directly, checking regex...")
    import re
    pat = re.compile(r'var pindas = \(this\.activeChartData\.ashtakavarga')
    if pat.search(content):
        content = pat.sub('var pindas = (this.activeChartData && this.activeChartData.ashtakavarga', content)
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("FIXED via regex!")
    else:
        print("Not found.")

