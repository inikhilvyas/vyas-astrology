const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf-8');
const desktopStart = html.indexOf('var VyasDesktop = {');
const desktopEnd = html.indexOf("document.addEventListener('DOMContentLoaded'", desktopStart);
const desktopScript = html.substring(desktopStart, desktopEnd);
const lines = desktopScript.split('\n');
console.log('Total lines:', lines.length);
for (let i = 1005; i < 1025; i++) {
    console.log(i + ': ' + lines[i]);
}

