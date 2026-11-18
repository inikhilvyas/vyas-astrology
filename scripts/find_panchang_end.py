with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('renderPanchang: function()')
end_marker = "initPanchangClock: function()"
pos_end = text.find(end_marker, pos)
print(f"renderPanchang ends around {pos_end}")
print(text[pos_end-400:pos_end+100])

