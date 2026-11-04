const en = require('/tmp/localejs/en.js');
const langs = ['af','zu','xh','tn','ve','ts','nso','st','nr','ss'];
function flat(o, p='', out={}) {
  for (const [k,v] of Object.entries(o)) {
    const path = p ? p+'.'+k : k;
    if (typeof v === 'string') out[path] = v;
    else if (v && typeof v === 'object') flat(v, path, out);
  }
  return out;
}
const enf = flat(en);
console.log('EN keys:', Object.keys(enf).length);
for (const l of langs) {
  const f = flat(require('/tmp/localejs/'+l+'.js'));
  const missing = Object.keys(enf).filter(k => !(k in f));
  const extra = Object.keys(f).filter(k => !(k in enf));
  console.log(l, 'keys', Object.keys(f).length, 'missing', missing.length, 'extra', extra.length);
  if (process.argv.includes('--detail')) {
    if (missing.length) console.log('  MISSING:', JSON.stringify(missing));
    if (extra.length) console.log('  EXTRA:', JSON.stringify(extra));
  }
}
