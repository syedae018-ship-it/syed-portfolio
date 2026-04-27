const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// Replacements
html = html.replace(/Syed Mustafa — Video Editor & AI Specialist/g, "Syed Mustafa | Video Editor & AI Specialist");
html = html.replace(/AI-Powered Video Editing — Now Available/g, "AI-Powered Video Editing: Now Available");
html = html.replace(/— creating scroll-stopping/g, "Creating scroll-stopping");
html = html.replace(/from concept to delivery — every piece/g, "from concept to delivery. Every piece");
html = html.replace(/Portfolio — Syed Mustafa/g, "Portfolio | Syed Mustafa");

// Remove the rocket from the h2
html = html.replace(/That <em>Actually Performs<\/em> 🚀/g, "That <em>Actually Performs</em>");

fs.writeFileSync('index.html', html);
