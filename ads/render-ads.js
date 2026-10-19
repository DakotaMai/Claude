const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
const ADS = {
  ignite: {
    label: 'FREE SYSTEMS HEALTH CHECK',
    visual: 'ring', score: 50,
    head: 'It works. <em>Because you do.</em>',
    sub: 'Find out where your time is really going, and what to fix first.',
    cta: 'Take the 3-minute check →'
  },
  inferno: {
    label: 'FREE SYSTEMS HEALTH CHECK',
    visual: 'bars',
    head: 'The numbers<br>are good. <em>The picture isn\'t.</em>',
    sub: 'See where your leads, data and processes are leaking, and what it\'s costing you.',
    cta: 'Take the 3-minute check →'
  }
};
const BARS = [['Marketing visibility',33,1],['Connected data',67,0],['Lead quality',67,0],['Process ownership',17,1],['Admin & automation',50,0],['Systems capacity',67,0]];
function page(ad, w, h){
  const story = h > w*1.5;
  const S = w/1080;
  const ring = `<div class="ring"><div class="num">${ad.score}<small>/ 100</small></div></div>`;
  const bars = `<div class="bars">${BARS.map(([n,p,weak])=>`<div class="row${weak?' weak':''}"><div class="top"><span>${n}${weak?'<b>LOOK HERE FIRST</b>':''}</span><span>${p}%</span></div><div class="track"><i style="width:${p}%"></i></div></div>`).join('')}</div>`;
  return `<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Chivo:wght@700;900&family=Livvic:wght@500;600&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:${w}px;height:${h}px;background:#2a140c;color:#f2e1cd;font-family:'Livvic',sans-serif;overflow:hidden}
.wrap{position:absolute;inset:0;padding:${(story?150:90)*S}px ${84*S}px ${(story?170:80)*S}px;display:flex;flex-direction:column;gap:${(story?64:46)*S}px}
.pill{align-self:flex-start;border:${2.5*S}px solid #c75c33;color:#c75c33;border-radius:999px;padding:${10*S}px ${26*S}px;font-weight:600;font-size:${24*S}px;letter-spacing:.18em}
.visual{flex:1;display:flex;align-items:center;justify-content:${ad.visual==='ring'?'flex-start':'stretch'}}
.ring{width:${(story?480:380)*S}px;height:${(story?480:380)*S}px;border-radius:50%;background:conic-gradient(#c75c33 ${ad.score}%,rgba(242,225,205,.12) 0);position:relative;display:grid;place-items:center}
.ring::after{content:"";position:absolute;inset:${30*S}px;border-radius:50%;background:#2a140c}
.num{position:relative;z-index:1;font-family:'Chivo';font-weight:900;font-size:${(story?190:150)*S}px;letter-spacing:-.05em;line-height:1;text-align:center}
.num small{display:block;font-family:'Livvic';font-weight:600;font-size:${28*S}px;letter-spacing:.12em;color:rgba(242,225,205,.55);margin-top:${10*S}px}
.bars{width:100%;display:flex;flex-direction:column;gap:${(story?38:26)*S}px}
.row .top{display:flex;justify-content:space-between;font-size:${30*S}px;font-weight:600;margin-bottom:${12*S}px}
.row .top span:last-child{color:rgba(242,225,205,.55)}
.row b{font-size:${18*S}px;letter-spacing:.14em;color:#c75c33;margin-left:${16*S}px;vertical-align:middle}
.track{height:${14*S}px;border-radius:${7*S}px;background:rgba(242,225,205,.12);overflow:hidden}
.track i{display:block;height:100%;background:rgba(242,225,205,.55);border-radius:inherit}
.weak .track i{background:#c75c33}
h1{font-family:'Chivo';font-weight:900;font-size:${(story?112:(ad.visual==='bars'?86:100))*S}px;line-height:.98;letter-spacing:-.025em}
h1 em{font-style:normal;color:#c75c33;display:block}
p{font-size:${(story?40:36)*S}px;line-height:1.4;color:rgba(242,225,205,.8);max-width:${860*S}px}
.foot{display:flex;justify-content:space-between;align-items:center;gap:${20*S}px}
.cta{background:#c75c33;color:#f2e1cd;border-radius:${14*S}px;padding:${26*S}px ${40*S}px;font-weight:600;font-size:${32*S}px;letter-spacing:.02em}
.brand{font-family:'Chivo';font-size:${22*S}px;letter-spacing:.14em;text-transform:uppercase;text-align:right;line-height:1.3}
.brand span{color:#c75c33;display:block}
</style></head><body><div class="wrap">
<span class="pill">${ad.label}</span>
<div class="visual">${ad.visual==='ring'?ring:bars}</div>
<div style="display:flex;flex-direction:column;gap:${24*S}px"><h1>${ad.head}</h1><p>${ad.sub}</p></div>
<div class="foot"><span class="cta">${ad.cta}</span><span class="brand">Ember<span>by Victoria Lewis</span></span></div>
</div></body></html>`;
}
(async()=>{
  const b = await chromium.launch();
  for (const [key, ad] of Object.entries(ADS)) for (const [fmt,w,h] of [['feed',1080,1350],['story',1080,1920]]) {
    const p = await b.newPage({viewport:{width:w,height:h}});
    await p.setContent(page(ad,w,h), {waitUntil:'networkidle'}).catch(()=>{});
    await p.evaluate(()=>document.fonts.ready);
    const fonts = await p.evaluate(()=>[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family+' '+f.weight).join(', '));
    const file = `/home/user/Claude/ads/health-check-${key}-${fmt}.png`;
    await p.screenshot({path:file});
    console.log(file.split('/').pop(), '| fonts:', fonts || 'FALLBACK');
    await p.close();
  }
  await b.close();
})();
