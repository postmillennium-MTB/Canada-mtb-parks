/* Copy each guide's parks into the other guide, for cross-border road trips.
   The same file lives in the USA and Canada guides.

     node tools/sync-other-parks.js <path to USA-bike-parks> <path to Canada-mtb-parks>
     (needs Playwright; e.g. from either repo root: node tools/sync-other-parks.js ../USA-bike-parks ../Canada-mtb-parks)

   Each guide stays the only place its own parks are edited. This script opens both pages,
   reads the parks the page itself builds (the USA guide parses its .park-row markup and COORDS;
   the Canada guide has the PARKS array), and writes a small snapshot of the OTHER country's
   parks into each page, between the OTHER_PARKS:BEGIN / OTHER_PARKS:END markers. Road trips
   use the snapshot to list, pin and route through parks across the border, each linking to its
   own guide. Run it again after adding, closing or moving a park in either guide, or the other
   guide's road trips will show the old details. Only the fields a trip needs are copied: name,
   town, position, vertical (as published: feet for US parks, metres and feet for Canadian
   parks), whether it is on the Loam Pass (road trips can highlight Loam parks) and
   open / coming / closed.

     node tools/sync-other-parks.js --check <USA-bike-parks> <Canada-mtb-parks>
     reads both pages and reports, for each direction, the last sync date and every park added,
     removed or changed (name, town, position, vertical, status) since then. It writes nothing.
   Without --check, a page is only rewritten when its snapshot is actually out of date, so a
   sync with nothing to do changes no files (and needs no commit). */
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const args = process.argv.slice(2), CHECK = args.includes('--check');
const [usaDir, caDir] = args.filter(a => a !== '--check').map(p => path.resolve(p));
if (!usaDir || !caDir) { console.error('usage: node tools/sync-other-parks.js [--check] <USA-bike-parks> <Canada-mtb-parks>'); process.exit(2); }
const pages = { usa: path.join(usaDir, 'index.html'), ca: path.join(caDir, 'index.html') };
const GUIDE = { usa: 'https://postmillennium-mtb.github.io/USA-bike-parks/', ca: 'https://postmillennium-mtb.github.io/Canada-mtb-parks/' };

(async () => {
  const browser = await chromium.launch();
  const read = async (file, fn, arg) => { const pg = await browser.newPage(); await pg.goto('file://' + file); await pg.waitForTimeout(800); const v = await pg.evaluate(fn, arg); await pg.close(); return v; };
  const usa = await read(pages.usa, () => MAPPED.map(p => ({ id: p.id, name: p.name, city: p.city, coords: p.coords,
    vertFt: p.vertFt, approx: !!p.vertApprox, loam: !!p.isLoam, status: p.status === 'closed' ? 'closed' : p.status === 'coming' ? 'coming' : 'open' })));
  const ca = await read(pages.ca, () => PARKS.map(p => ({ id: p.id, name: p.name, city: p.city, coords: p.coords,
    vertFt: p.vertFt, vertM: p.vertM, loam: p.badges.includes('loam'), status: p.badges.includes('closed') ? 'closed' : p.badges.includes('soon') ? 'coming' : 'open' })));
  /* how far each park sits from the road-trip network (NA_ROADS is the same in both pages) */
  const offRoad = new Map(Object.entries(await read(pages.usa, list => {
    const G = rtBuildGraph(NA_ROADS), out = {};
    list.forEach(([k, c]) => { let best = Infinity; G.edges.forEach(e => { best = Math.min(best, rtNearest(c, e.pts).km); }); out[k] = best; });
    return out;
  }, usa.map(p => ['usa' + p.id, p.coords]).concat(ca.map(p => ['ca' + p.id, p.coords])))));
  await browser.close();
  const today = new Date().toISOString().slice(0, 10);
  /* compare with the snapshot already in the page: what was added, removed or changed */
  const nm = p => (p.name && p.name.en) || p.name;
  const FAR_KM = 15;   // same threshold as tools/fetch-park-access.py
  const diff = (file, country, parks, tag) => {
    const s = fs.readFileSync(file, 'utf8');
    const m = s.match(/const OTHER_PARKS = (\{.*?\});\n/);
    const old = m ? JSON.parse(m[1]) : { synced: 'never', parks: [] };
    const byId = new Map(old.parks.map(p => [p.id, p])), seen = new Set(), lines = [];
    parks.forEach(p => {
      const o = byId.get(p.id); seen.add(p.id);
      const far = () => { const d = offRoad.get(tag + p.id); return d > FAR_KM ?
        `\n    FAR FROM ROADS: ${Math.round(d)} km from the road-trip network; it needs an access road (CLAUDE.md, park sync step 6)` : ''; };
      if (!o) { lines.push(`  added:   ${nm(p)}` + far()); return; }
      const keys = ['name', 'city', 'coords', 'vertFt', 'vertM', 'approx', 'loam', 'status']
        .filter(k => JSON.stringify(o[k]) !== JSON.stringify(p[k]));
      const ch = keys.map(k => k === 'status' ? `status ${o.status} -> ${p.status}` : k);
      if (ch.length) lines.push(`  changed: ${nm(p)} (${ch.join(', ')})` + (keys.includes('coords') ? far() : ''));
    });
    old.parks.forEach(o => { if (!seen.has(o.id)) lines.push(`  removed: ${nm(o)}`); });
    console.log(`${path.basename(path.dirname(file))}: ${country} snapshot last synced ${old.synced}; ` +
      (lines.length ? `${lines.length} difference(s):\n${lines.join('\n')}` : 'up to date'));
    return lines.length > 0;
  };
  const write = (file, guide, country, parks) => {
    if (!diff(file, country, parks, country === 'Canada' ? 'ca' : 'usa') || CHECK) return;
    let s = fs.readFileSync(file, 'utf8');
    const a = s.indexOf('/* OTHER_PARKS:BEGIN'), b = s.indexOf('/* OTHER_PARKS:END */');
    if (a < 0 || b < 0) throw new Error('OTHER_PARKS markers not found in ' + file);
    const block = '/* OTHER_PARKS:BEGIN — generated by tools/sync-other-parks.js; do not edit by hand.\n' +
      `   ${country} parks from the ${country} guide (${guide}), synced ${today}. */\n` +
      'const OTHER_PARKS = ' + JSON.stringify({ guide, country, synced: today, parks }) + ';\n';
    s = s.slice(0, a) + block + s.slice(b);
    fs.writeFileSync(file, s);
    console.log(`${path.basename(path.dirname(file))}: ${parks.length} ${country} parks written`);
  };
  write(pages.usa, GUIDE.ca, 'Canada', ca);
  write(pages.ca, GUIDE.usa, 'USA', usa);
})();
