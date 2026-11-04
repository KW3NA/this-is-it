// Verify every relative import in the app resolves to an existing file,
// and scan JSX for raw string children directly inside non-Text components
// (the cause of "Text strings must be rendered within a <Text> component").
const ts = require('typescript');
const fs = require('fs');
const path = require('path');

const root = process.argv[2] || '.';
const SKIP = new Set(['node_modules', '.git', 'android', 'ios', '.expo', 'dist']);

function walk(dir, out = []) {
  for (const f of fs.readdirSync(dir)) {
    const p = path.join(dir, f);
    const st = fs.statSync(p);
    if (st.isDirectory()) {
      if (!SKIP.has(f)) walk(p, out);
    } else if (/\.(ts|tsx)$/.test(f) && !/\.d\.ts$/.test(f)) {
      out.push(p);
    }
  }
  return out;
}

const files = walk(root);
let missing = 0;
let rawTextIssues = 0;

const TEXTY = new Set(['Text', 'TranslatedText', 'H1', 'H2', 'H3', 'Title', 'Paragraph', 'Label']);

function isTextyTag(name) {
  return TEXTY.has(name) || /text/i.test(name);
}

// Remove block and line comments so example code inside doc blocks isn't scanned.
function stripComments(s) {
  return s.replace(/\/\*[\s\S]*?\*\//g, '').replace(/(^|[^:])\/\/[^\n]*/g, '$1');
}

for (const f of files) {
  const rawSrc = fs.readFileSync(f, 'utf8');

  // Strip comments so example imports inside doc blocks aren't flagged.
  const src = ts.preProcessFile ? stripComments(rawSrc) : rawSrc;

  // 1) Relative import resolution
  const re = /(?:from\s+|require\()['"](\.[^'"]+)['"]/g;
  let m;
  while ((m = re.exec(src))) {
    const rel = m[1];
    const base = path.resolve(path.dirname(f), rel);
    const cands = [
      base + '.ts', base + '.tsx', base + '.js', base + '.jsx',
      base + '/index.ts', base + '/index.tsx', base + '/index.js', base,
    ];
    const ok = cands.some((c) => { try { return fs.statSync(c).isFile(); } catch (e) { return false; } });
    if (!ok) { console.log('MISSING IMPORT in ' + f + ' -> ' + rel); missing++; }
  }

  // 2) Raw string literals as direct JSX children of non-<Text> elements
  if (f.endsWith('.tsx')) {
    const sf = ts.createSourceFile(f, src, ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);
    (function visit(node) {
      if (ts.isJsxElement(node) || ts.isJsxSelfClosingElement(node)) {
        const open = ts.isJsxElement(node) ? node.openingElement : node;
        const tag = open.tagName.getText(sf);
        const kids = ts.isJsxElement(node) ? node.children : [];
        if (!isTextyTag(tag)) {
          for (const k of kids) {
            if (ts.isJsxText(k) && k.getText(sf).trim().length > 0) {
              const pos = sf.getLineAndCharacterOfPosition(k.getStart(sf));
              console.log('RAW TEXT outside <Text> in ' + f + ' L' + (pos.line + 1) + ' inside <' + tag + '> : "' + k.getText(sf).trim().slice(0, 40) + '"');
              rawTextIssues++;
            }
          }
        }
      }
      ts.forEachChild(node, visit);
    })(sf);
  }
}

console.log('---');
console.log('Files checked: ' + files.length);
console.log('Unresolved imports: ' + missing);
console.log('Raw-text-in-non-Text issues: ' + rawTextIssues);
process.exit(missing === 0 && rawTextIssues === 0 ? 0 : 1);
