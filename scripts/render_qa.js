const { Resvg } = require('C:/Users/lenovo/.workbuddy/binaries/node/workspace/node_modules/@resvg/resvg-js');
const fs = require('fs');
const path = require('path');

const dir = 'C:/Users/lenovo/gh_repos/banners';
const name = process.argv[2];
if (!name) { console.error('usage: node render_qa.js <name>'); process.exit(1); }

let svg = fs.readFileSync(path.join(dir, name + '.svg'), 'utf8');
let s = svg
  .replace(/<animate\b[^>]*\/>/g, '')
  .replace(/<animateTransform\b[^>]*\/>/g, '')
  .replace(/stroke-dashoffset="[^"]*"/g, 'stroke-dashoffset="0"');

const r = new Resvg(s, { background: '#0b0f17', fitTo: { mode: 'width', value: 1280 } });
const png = r.render().asPng();
process.stdout.write(Buffer.from(png));
