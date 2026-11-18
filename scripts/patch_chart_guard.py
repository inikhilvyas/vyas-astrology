print("Patching renderChart and generateDiamondSVG guards...")

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Guard renderChart
old_render_chart = """            if (this.chartStyle === 'south') {
                wrap.innerHTML = this.generateSouthIndianSVG(cData.houses, 460, cData.title);
            } else {
                wrap.innerHTML = this.generateDiamondSVG(cData.houses, 460, cData.title);
            }"""

new_render_chart = """            var hData = (cData && cData.houses) ? cData.houses : cData;
            var chartTitle = (cData && cData.title) ? cData.title : "D-1 लग्न कुण्डली";
            if (this.chartStyle === 'south') {
                wrap.innerHTML = this.generateSouthIndianSVG(hData, 460, chartTitle);
            } else {
                wrap.innerHTML = this.generateDiamondSVG(hData, 460, chartTitle);
            }"""

if old_render_chart in content:
    content = content.replace(old_render_chart, new_render_chart)
    print("✓ Patched renderChart to safely pass hData")

# 2. Guard generateDiamondSVG at the top
old_diamond_top = """generateDiamondSVG(housesData, size, title) {
            var s = size || 460;"""

new_diamond_top = """generateDiamondSVG(housesData, size, title) {
            var s = size || 460;
            if (!housesData || typeof housesData !== 'object') {
                return this.generateEmptyDiamondSVG(s);
            }"""

if old_diamond_top in content:
    content = content.replace(old_diamond_top, new_diamond_top)
    print("✓ Added null safety guard to generateDiamondSVG")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Guards updated!")

