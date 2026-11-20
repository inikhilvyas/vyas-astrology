with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

fn = text[549753:599768]
script = f"""global.window = {{}};
var Vyas = {{ {fn} }};
const res = Vyas.computeMathematicalKundli("NIKHIL VYAS", "1984-11-23", "16:51", "Falna", "Male");
console.log("PROFILE:", JSON.stringify(res.profile, null, 2));
console.log("PLANETS:", JSON.stringify(res.planet_table, null, 2));
console.log("CHARTS D1:", JSON.stringify(res.charts.d1, null, 2));
"""

with open('temp_eval.js', 'w', encoding='utf-8') as f:
    f.write(script)
print("Written temp_eval.js")
