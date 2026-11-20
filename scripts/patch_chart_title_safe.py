with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = """            var chartTitle = (cData && cData.title) ? cData.title : (vk.toUpperCase() + " कुण्डली • जन्मपत्रिका");
            if (titleElem) titleElem.innerText = "✦ " + chartTitle;"""

replacement = """            var chartTitle = (cData && typeof cData.title === 'string' && cData.title.trim()) ? cData.title.trim() : ((vk ? vk.toUpperCase() : "D-1") + " कुण्डली • जन्मपत्रिका");
            if (!chartTitle || chartTitle.indexOf('undefined') !== -1) chartTitle = "D-1 लग्न कुण्डली • जन्मपत्रिका";
            if (titleElem) titleElem.innerText = "✦ " + chartTitle;"""

if target in content:
    content = content.replace(target, replacement)
    print("✓ Secured chartTitle against undefined")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
else:
    print("Warning: target not found verbatim")

