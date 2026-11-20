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
    if (count === 4) {
        // test line by line or binary search to find syntax error
        const lines = jsCode.split('\n');
        console.log(`Script 4 has ${lines.length} lines`);
        let acc = '';
        for (let i = 0; i < lines.length; i++) {
            acc += lines[i] + '\n';
            try {
                // quick test
                new vm.Script(acc);
            } catch (e) {
                if (e.message.includes('Invalid or unexpected token') || e.message.includes('Unexpected token')) {
                    console.log(`Syntax error at line ${i+1}: ${e.message}`);
                    console.log(`Line content: ${lines[i]}`);
                    break;
                }
            }
        }
    }
}

