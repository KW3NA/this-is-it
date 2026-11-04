// Syntax-parse checker for all TS/TSX files in the app (mirrors what Metro/Babel does).
const ts = require('typescript');
const fs = require('fs');
const path = require('path');

const root = process.argv[2] || '.';
const SKIP_DIRS = new Set(['node_modules', '.git', 'android', 'ios', 'dist', '.expo']);

function walk(dir, out = []) {
  for (const f of fs.readdirSync(dir)) {
    const p = path.join(dir, f);
    const st = fs.statSync(p);
    if (st.isDirectory()) {
      if (!SKIP_DIRS.has(f)) walk(p, out);
    } else if (/\.(ts|tsx)$/.test(f) && !/\.d\.ts$/.test(f)) {
      out.push(p);
    }
  }
  return out;
}

const files = walk(root);
let bad = 0;
for (const f of files) {
  const src = fs.readFileSync(f, 'utf8');
  const sf = ts.createSourceFile(
    f,
    src,
    ts.ScriptTarget.Latest,
    true,
    f.endsWith('x') ? ts.ScriptKind.TSX : ts.ScriptKind.TS
  );
  const errs = sf.parseDiagnostics || [];
  if (errs.length) {
    bad++;
    console.log('=== ' + f + ' ===');
    for (const e of errs.slice(0, 8)) {
      const pos = sf.getLineAndCharacterOfPosition(e.start);
      console.log('  L' + (pos.line + 1) + ':' + (pos.character + 1) + ' ' + ts.flattenDiagnosticMessageText(e.messageText, ' '));
    }
  }
}
console.log(bad === 0
  ? 'ALL FILES PARSE OK (' + files.length + ' files checked)'
  : bad + ' file(s) with syntax errors out of ' + files.length);
process.exit(bad === 0 ? 0 : 1);
