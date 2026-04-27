const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const emojiRegex = /[\u{1F300}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{1F600}-\u{1F64F}\u{1F680}-\u{1F6FF}]/gu;
const lines = html.split('\n');
lines.forEach((line, i) => {
    if (emojiRegex.test(line)) {
        console.log(`Line ${i+1}: ${line.trim()}`);
    }
});
