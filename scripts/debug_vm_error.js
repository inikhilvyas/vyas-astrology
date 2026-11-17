
const vm = require('vm');
const fs = require('fs');
const content = fs.readFileSync('index.html', 'utf8');
const scriptRegex = /<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/gi;
let match;
let count = 0;
while ((match = scriptRegex.exec(content)) !== null) {
    count++;
    try {
        new vm.Script(match[1]);
        console.log(`Script ${count}: PASS`);
    } catch(e) {
        console.log(`Script ${count}: FAIL at line ${e.stack}`);
        const lines = match[1].split('\n');
        // print error line
        const m = e.stack.match(/<anonymous>:(\d+)/);
        if (m) {
            const lNum = parseInt(m[1]);
            for (let i = Math.max(0, lNum - 10); i < Math.min(lines.length, lNum + 10); i++) {
                console.log(`${i+1}: ${lines[i]}`);
            }
        }
    }
}
