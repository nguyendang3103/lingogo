// Chạy phần dữ liệu của app tiếng Trung trong vm cô lập, xuất JSON.
const fs = require('fs'), vm = require('vm');
const L = fs.readFileSync(process.argv[2], 'utf8').split('\n');
const pick = (a, b) => L.slice(a - 1, b).join('\n');
const ctx = vm.createContext({ console });
const code = pick(237, 1199).replace(/^const /gm, 'var ').replace(/^let /gm, 'var ');
vm.runInContext(code, ctx, { timeout: 20000 });
for (const ln of [1222, 1460, 1461, 1463, 1464, 1565]) vm.runInContext(L[ln - 1].replace(/^const /, 'var '), ctx);
const out = {};
for (const k of ['W', 'AU', 'HV', 'HVO', 'CH', 'RN', 'GR', 'HSKW', 'HSKT', 'ORDER', 'EN', 'EN_MIX', 'GMAP', 'LV1', 'LV2', 'LV3']) out[k] = ctx[k];
fs.writeFileSync(process.argv[3] + '/zh-data.json', JSON.stringify(out));
fs.writeFileSync(process.argv[3] + '/zh-strokes.json', JSON.stringify(ctx.STROKES));
fs.writeFileSync(process.argv[3] + '/zh-audio.json', JSON.stringify(ctx.BUNDLES));
console.log('W', ctx.W.length, 'strokes', Object.keys(ctx.STROKES).length, 'bundles', Object.keys(ctx.BUNDLES).length, Object.keys(ctx.BUNDLES).map(k => k + ':' + Object.keys(ctx.BUNDLES[k]).length).join(' '));
