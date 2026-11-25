with open('cpp/src/vedic_engine.hpp', 'r', encoding='utf-8', errors='ignore') as f:
    for i, line in enumerate(f):
        if 'ComputeChart' in line:
            print(str(i+1) + ': ' + line.strip()[:100])
