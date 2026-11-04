// Scan for JSX placed directly as an object-literal property value (missing braces),
// which compiles fine under some parsers but breaks Metro/Babel, plus generic AST sanity checks.
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
    } else if (/\.tsx$/.test(f)) {
      out.push(p);
    }
  }
  return out;
}

let issues = 0;
for (const file of walk(root)) {
  const src = fs.readFileSync(file, 'utf8');
  const sf = ts.createSourceFile(file, src, ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);
  (function visit(n) {
    if (ts.isObjectLiteralExpression(n)) {
      for (const p of n.properties) {
        if (
          p.kind === ts.SyntaxKind.JsxElement ||
          p.kind === ts.SyntaxKind.JsxSelfClosingElement ||
          p.kind === ts.SyntaxKind.JsxFragment
        ) {
          const pos = sf.getLineAndCharacterOfPosition(p.getStart(sf));
          console.log('JSX-IN-OBJECT in ' + file + ' L' + (pos.line + 1));
          issues++;
        }
      }
    }
    ts.forEachChild(n, visit);
  })(sf);
}
console.log(issues === 0 ? 'No JSX-in-object-literal problems found' : issues + ' problem(s)');
process.exit(issues === 0 ? 0 : 1);
