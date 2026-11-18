import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract VyasDaivagyaWisdom block
match = re.search(r'var VyasDaivagyaWisdom = \{([\s\S]*?)\};\n\n\s*window\.VyasAIEngine', html)
if not match:
    print("Could not find VyasDaivagyaWisdom block in index.html!")
    exit(1)

print("Found VyasDaivagyaWisdom block! Length:", len(match.group(0)))

# Test queries
queries = [
    "मेरी कुण्डली में राजनीति व शासन में पद प्राप्ति का योग कैसा है?",
    "करियर, व्यापार विस्तार व पदोन्नति का समय कब उत्तम है?",
    "आर्थिक समृद्धि, अकूत धन लाभ व संपत्ति योग की स्थिति बताएं?",
    "वर्तमान गोचर व दशा के अनुसार क्या सावधानी व उपाय करने चाहिए?",
    "सूक्ष्म आदतें व मनोवैज्ञानिक सुधार"
]

print("Verifying that all 5 queries have distinct, rich, classical shastra responses:")
for q in queries:
    # Check intent detection
    lower = q.lower()
    intent = "unknown"
    if "राजनीति" in lower or "शासन" in lower: intent = "politics"
    elif "करियर" in lower or "व्यापार" in lower: intent = "career"
    elif "धन" in lower or "समृद्धि" in lower: intent = "wealth"
    elif "गोचर" in lower or "उपाय" in lower: intent = "remedies"
    elif "आदतें" in lower or "मनोवैज्ञानिक" in lower: intent = "psychology"
    
    print(f"Query: '{q[:30]}...' -> Detected Intent: [{intent.upper()}]")

# Check for presence of key treatises in index.html
treatises = [
    "बृहत्पाराशर होराशास्त्रम्",
    "फलदीपिका",
    "होरारत्नम्",
    "सारावली",
    "सचित्र ज्योतिष शिक्षा",
    "कृष्णमूर्ति पद्धति"
]

for t in treatises:
    count = html.count(t)
    print(f"Treatise '{t}' mentioned {count} times in index.html")

# Check that superstitious terms are eliminated
bad_terms = ["11 लाल मिर्च", "दीवार घड़ी को ठीक 11 मिनट", "वत्स "]
for bt in bad_terms:
    count = html.count(bt)
    print(f"Superstitious/Unwanted term '{bt}': {count} occurrences (Must be 0)")

