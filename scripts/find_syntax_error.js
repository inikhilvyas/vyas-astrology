const fs = require('fs');
const vm = require('vm');
const html = fs.readFileSync('mobile/index.html', 'utf-8');

const scriptMatches = html.match(/<script[\s\S]*?>([\s\S]*?)<\/script>/gi);
scriptMatches.forEach((s, idx) => {
    const code = s.replace(/<script[\s\S]*?>/i, '').replace(/<\/script>/i, '');
    try {
        new vm.Script(code);
        console.log(`Script ${idx} compiled OK!`);
    } catch (e) {
        console.error(`Script ${idx} failed:`, e.message);
        const match = e.stack.match(/<anonymous>:(\d+)/);
        if (match) {
            const lineNo = parseInt(match[1]);
            const lines = code.split('\n');
            console.log(`Line ${lineNo}:`);
            for (let j = Math.max(0, lineNo-5); j <= Math.min(lines.length-1, lineNo+3); j++) {
                console.log(`${j+1}: ${lines[j]}`);
            }
        }
    }
});
