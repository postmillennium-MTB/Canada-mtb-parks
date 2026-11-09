/* Road-trip colour check — run it after changing a theme or any trip-mode colour.
   The same file lives in the USA and Canada guides.

     node tools/check-trip-colours.js            (from the repo root; needs Playwright)

   It opens index.html, plans a real trip, and in every theme plus the print palette reads the
   colours the browser actually renders (not the CSS tokens), so per-theme overrides such as
   theme 142's violet sketch are measured as drawn. Only marks that are on screen together are
   compared: the normal park pins are hidden in trip mode, so they are not paired with the route.
   Standard (CLAUDE.md): lines and marks >= 3:1 against what they sit on, text >= 4.5:1, and two
   colours that must be told apart >= 15 OKLab dE (x100) for normal vision and >= 8 under
   simulated deuteranopia, protanopia and tritanopia. Exits 1 if anything fails. */
const path = require('path');
const { chromium } = require('playwright');

const hexOrRgb = c => {
  const sr = c.match(/color\(srgb ([^)]+)\)/);
  if (sr) return sr[1].trim().split(/\s+/).slice(0, 3).map(Number);
  const m = c.match(/rgba?\(([^)]+)\)/);
  if (m) return m[1].split(',').slice(0, 3).map(v => parseFloat(v) / 255);
  const h = c.replace('#', '');
  return [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16) / 255);
};
const lin = c => c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
const lum = rgb => { const [r, g, b] = rgb.map(lin); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
const over = (fg, bg, a) => fg.map((v, i) => v * a + bg[i] * (1 - a));
const CVD = {   // Machado et al. 2009, severity 1, linear RGB
  deutan: [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
  protan: [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
  tritan: [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]] };
const oklab = ([r, g, b]) => {
  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
  const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
  const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
  return [0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s, 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s, 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s];
};
const sim = (rgb, k) => { const v = rgb.map(lin); return k ? CVD[k].map(r => Math.min(1, Math.max(0, r[0] * v[0] + r[1] * v[1] + r[2] * v[2]))) : v; };
const dE = (a, b, k) => { const x = oklab(sim(a, k)), y = oklab(sim(b, k)); return 100 * Math.hypot(x[0] - y[0], x[1] - y[1], x[2] - y[2]); };

(async () => {
  const file = 'file://' + path.resolve(__dirname, '..', 'index.html');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.goto(file); await page.waitForTimeout(1200);
  const canada = await page.evaluate(() => typeof CA_LAND_GEO !== 'undefined');   // the Canada guide's vector basemap
  const themes = await page.evaluate(() => typeof THEMES !== 'undefined' && typeof setTheme === 'function'
    ? THEMES.map(t => t.id) : [...document.querySelectorAll('.theme-btn[data-theme]')].map(b => b.dataset.theme));
  /* plan a real trip with sketch, route, numbered pins and (for the drawing view) park dots */
  await page.evaluate(canada => {
    tripGraph = rtBuildGraph(typeof NA_ROADS !== 'undefined' ? NA_ROADS : canada ? CA_ROADS : US_ROADS);
    const sk = canada ? [[51.05, -114.07], [51.2, -116.0], [51.0, -118.2], [50.4, -119.3], [49.88, -119.49]]
                      : [[39.74, -104.99], [39.6, -106.0], [39.55, -107.3], [39.06, -108.55], [38.57, -109.55]];
    tripRoute = rtSnapTrip(tripGraph, sk);
    tripSketchLine = L.polyline(sk, { className: 'trip-sketch', interactive: false, weight: 2 }).addTo(mapInstance);
    tripRenderRoute();
    /* "Highlight Loam Pass" on, so its marks are drawn and measured too */
    const lc = document.getElementById(canada ? 'trip-loam' : 'tripLoam');
    if (lc) lc.checked = true;
    tripShowGhosts(true);
    mapInstance.fitBounds(L.polyline(tripRoute.path).getBounds());
  }, canada);

  const read = () => page.evaluate(canada => {
    const cs = sel => { const e = document.querySelector(sel); return e ? getComputedStyle(e) : null; };
    const v = n => getComputedStyle(document.body).getPropertyValue(n).trim();
    return {
      route: cs('.trip-route').stroke, casing: cs('.trip-route-casing').stroke,
      band: cs('.trip-band').stroke, bandA: parseFloat(cs('.trip-band').strokeOpacity),
      sketch: cs('.trip-sketch').stroke, ghost: cs('.trip-ghost:not(.is-loam)').fill, ghostRing: cs('.trip-ghost:not(.is-loam)').stroke,
      pinBg: cs('.trip-pin:not(.is-loam)').backgroundColor, pinFg: cs('.trip-pin:not(.is-loam)').color,
      loam: (cs('.trip-ghost.is-loam') || {}).fill || null,
      loamPinBg: v('--trip-loam'), loamPinFg: v('--trip-loam-fg'),
      land: canada ? cs('.land-ca').fill : cs('.us-state-shape').fill,
      ground: canada ? v('--bg') : cs('.us-state-shape').fill,       // what the route crosses (Canada: OSM tiles; the casing is the guaranteed ground)
      card: getComputedStyle(document.getElementById(canada ? 'trip-results' : 'tripResults')).backgroundColor,
      text: v(canada ? '--text' : '--chalk'), dim: v(canada ? '--text-dim' : '--chalk-dim'), mute: v(canada ? '--text-muted' : '--chalk-mute')
    };
  }, canada);

  let fails = 0;
  const check = (name, value, min) => { const ok = value >= min; if (!ok) fails++; console.log(`  ${ok ? 'ok  ' : 'FAIL'} ${name}: ${value.toFixed(2)} (min ${min})`); };
  const runOne = async label => {
    const c = Object.fromEntries(Object.entries(await read()).map(([k, x]) => [k, typeof x === 'number' ? x : hexOrRgb(x)]));
    console.log(`\n== ${label}`);
    check('route vs casing', ratio(c.route, c.casing), 3);
    check('route vs ground', ratio(c.route, c.ground), 3);
    check('route vs corridor band', ratio(c.route, over(c.band, c.ground, c.bandA)), 3);
    check('sketch vs ground', ratio(c.sketch, c.ground), 3);
    check('park dot vs ground', ratio(c.ghost, c.ground), 3);
    check('pin number vs pin', ratio(c.pinFg, c.pinBg), 4.5);
    check('list text vs card', ratio(c.text, c.card), 4.5);
    check('list dim text vs card', ratio(c.dim, c.card), 4.5);
    check('fine print vs card', ratio(c.mute, c.card), 4.5);
    for (const [k, min] of [[null, 15], ['deutan', 8], ['protan', 8], ['tritan', 8]])
      check(`route vs sketch dE ${k || 'normal'}`, dE(c.route, c.sketch, k), min);
    /* "Highlight Loam Pass": the Loam colour sits on the land with the route, pins, dots and sketch */
    if (c.loam){
      check('Loam dot vs land', ratio(c.loam, c.land), 3);
      check('Loam pin number vs Loam pin', ratio(c.loamPinFg, c.loamPinBg), 4.5);
      for (const [nm, o] of [['route', c.route], ['pin', c.pinBg], ['park dot', c.ghost], ['sketch', c.sketch]])
        for (const [k, min] of [[null, 15], ['deutan', 8], ['protan', 8], ['tritan', 8]])
          check(`Loam vs ${nm} dE ${k || 'normal'}`, dE(c.loam, o, k), min);
    } else { fails++; console.log('  FAIL Loam marks not found'); }
  };
  for (const t of themes) {
    await page.evaluate(t => typeof setTheme === 'function' && typeof THEMES !== 'undefined'
      ? setTheme(t) : document.querySelector(`.theme-btn[data-theme="${t}"]`).click(), t);
    await page.waitForTimeout(150);
    await runOne('theme ' + t);
  }
  await page.emulateMedia({ media: 'print' });
  await runOne('print');
  console.log(`\n${fails ? fails + ' FAILED' : 'all checks passed'}`);
  await browser.close();
  process.exit(fails ? 1 : 0);
})();
