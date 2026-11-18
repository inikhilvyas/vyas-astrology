with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

bad = "\"                '@media print { .no-print { display:none; } }' +\"\n                '\"\n        '\n\n    </style></head><body>' +\""
# Let's inspect with regex
import re
content = re.sub(r"'@media print \{ \.no-print \{ display:none; \} \}' \+\s*'\s*'\s*</style></head><body>' \+", "'@media print { .no-print { display:none; } }' + '</style></head><body>' +", content)

# Check if there is still a dangling quote
content = content.replace("                '@media print { .no-print { display:none; } }' +\n                '\n        \n\n    </style></head><body>' +", "                '@media print { .no-print { display:none; } }' + '</style></head><body>' +")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Cleaned dangling quote!")
