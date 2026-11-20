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
    if (attrs.includes('application/ld+json')) continue;
    const linesBefore = html.substring(0, match.index).split('\n').length;
    try {
        new vm.Script(jsCode, { filename: 'index.html', lineOffset: linesBefore - 1 });
    } catch (e) {
        console.error(`Error in script #${count}:`);
        console.error(e.stack);
    }
}

