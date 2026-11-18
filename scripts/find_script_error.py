# -*- coding: utf-8 -*-
with open('scripts/test_modal_and_kundli_creation.js', 'r', encoding='utf-8') as f:
    t_src = f.read()

# See how fullScript is constructed
with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

import re
scripts = re.findall(r'<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>', h, re.IGNORECASE)
print("Total scripts found:", len(scripts))

import subprocess
# Test each script in node vm
test_js = """
const vm = require('vm');
const fs = require('fs');
const content = fs.readFileSync('index.html', 'utf8');
const scriptRegex = /<script(?![^>]*src=)[^>]*>([\\s\\S]*?)<\\/script>/gi;
let match;
let count = 0;
while ((match = scriptRegex.exec(content)) !== null) {
    count++;
    try {
        new vm.Script(match[1]);
        console.log(`Script ${count}: PASS`);
    } catch(e) {
        console.log(`Script ${count}: FAIL at line ${e.stack}`);
        const lines = match[1].split('\\n');
        // print error line
        const m = e.stack.match(/<anonymous>:(\\d+)/);
        if (m) {
            const lNum = parseInt(m[1]);
            for (let i = Math.max(0, lNum - 10); i < Math.min(lines.length, lNum + 10); i++) {
                console.log(`${i+1}: ${lines[i]}`);
            }
        }
    }
}
"""
with open('scripts/debug_vm_error.js', 'w', encoding='utf-8') as f:
    f.write(test_js)

print("Created scripts/debug_vm_error.js")

