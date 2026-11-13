const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(require('node:path').join(__dirname, '../static/theme.js'), 'utf8');
function run(initial, blocked = false) {
  const values = new Map(Object.entries(initial));
  const context = {document: {documentElement: {dataset: {}}}, matchMedia: () => ({matches: false}), localStorage: {
    getItem(k) {if (blocked) throw Error('Unavailable'); return values.get(k) ?? null;},
    setItem(k,v) {values.set(k,v);}, removeItem(k) {values.delete(k);}
  }};
  vm.runInNewContext(source, context);
  return {values, theme:context.document.documentElement.dataset.theme};
}
const migrated=run({'genjustsu.theme':'dark','genjustsu.language':'en','genjustsu.lastTask':'saved-task'});
assert.equal(migrated.theme,'dark');
assert.equal(migrated.values.get('henge.language'),'en');
assert.equal(migrated.values.get('henge.lastTask'),'saved-task');
assert.equal(migrated.values.has('genjustsu.lastTask'),false);
const current=run({'henge.theme':'light','genjustsu.theme':'dark'});
assert.equal(current.theme,'light');
assert.equal(current.values.has('genjustsu.theme'),false);
assert.equal(run({},true).theme,'light');
console.log('7 browser storage migration assertions passed');
