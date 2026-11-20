const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('index.html', 'utf8');
const scriptRegex = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
let match;
let count = 0;

while ((match = scriptRegex.exec(html)) !== null) {
    count++;
    const attrs = match[1];
    const jsCode = match[2];
    if (attrs.includes('application/ld+json')) {
        console.log(`Script #${count} is JSON-LD (valid).`);
        continue;
    }
    try {
        new vm.Script(jsCode);
        console.log(`Script #${count} (length ${jsCode.length}) PASSED.`);
    } catch (e) {
        console.error(`Script #${count} FAILED:`, e.message);
        const linesBefore = html.substring(0, match.index).split('\n').length;
        console.error(`Approximate line in file: ${linesBefore}`);
        const lines = jsCode.split('\n');
        // print error snippet
        console.error("First 15 lines of script:");
        console.error(lines.slice(0, 15).join('\n'));
    }
}

