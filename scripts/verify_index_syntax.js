const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('index.html', 'utf8');
const scriptRegex = /<script\b[^>]*>([\s\S]*?)<\/script>/gi;
let match;
let count = 0;
let errors = 0;

while ((match = scriptRegex.exec(html)) !== null) {
    count++;
    const jsCode = match[1];
    // skip empty or external scripts without inline code
    if (!jsCode.trim()) continue;
    try {
        new vm.Script(jsCode);
    } catch (e) {
        errors++;
        console.error(`JS Syntax Error in Script #${count}:`, e.message);
        // find line in file
        const linesBefore = html.substring(0, match.index).split('\n').length;
        console.error(`Approximate line: ${linesBefore}`);
        const codeLines = jsCode.split('\n');
        if (e.lineNumber) {
            console.error(`Error line snippet: ${codeLines[e.lineNumber - 1]}`);
        }
    }
}

if (errors === 0) {
    console.log(`✓ All ${count} inline scripts in index.html passed syntax checks cleanly!`);
} else {
    console.error(`Found ${errors} syntax errors.`);
    process.exit(1);
}

