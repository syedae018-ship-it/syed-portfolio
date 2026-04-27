const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const textRegex = />([^<]+)</g;
let match;
let i = 0;
while ((match = textRegex.exec(html)) !== null) {
    const text = match[1].trim();
    if (text && (text.includes('-') || text.includes('_') || text.includes('—'))) {
        console.log(`Text: "${text}"`);
        i++;
        if (i > 20) break;
    }
}
