# Canada MTB Parks Guide

A single-file, bilingual (EN/FR) interactive guide to every lift-served
mountain bike park in Canada. Built as one `index.html` — no build step, no
dependencies beyond Leaflet (inlined) and Google Fonts (CDN) — so it can be
embedded directly in an iframe on postmillenniumrenaissance.com and in
Pinkbike articles. Read `.claude/skills/pmr-build-standard` (if present) or
the equivalent PMR build-standard skill before making structural changes:
one file, zero unnecessary dependencies, one contiguous data block, registry
pattern for anything that repeats, mobile-first, iframe-safe.

## Sibling tool

This is one of two twin PMR bike-park guides by the same author, sharing
the same build standard and the same class of structural bugs but **not**
the same data schema:
- **This repo (Canada):** bilingual (EN/FR), park data is a JS array
  literal (`const PARKS = [...]`).
- **USA — `postmillennium-MTB/USA-bike-parks`:** English only, park data
  is authored directly in the HTML as `.park-row` elements, not an array.

If you're fixing a structural/dependency bug (the CARTO tile-provider
issue below is exactly this kind — it hit both repos identically) or
introducing a new maintenance convention (e.g. how closures are tracked),
check whether the USA repo has the same problem or would benefit from the
same fix. The two repos share no code, so nothing here propagates there
automatically. That repo isn't attached to your session by default — use
`add_repo` (or ask Jon) before assuming its current state.

## Scope: what counts as a "bike park" here

"Bike park" is an overloaded term in the industry. Many facilities that
call themselves a "bike park" are pump tracks, dirt-jump lines, or skills
areas with no real descent — Frisco Bike Park in Frisco, CO (pump track +
jump lines, no lift) is the canonical example. This guide's definition is
narrower:

> A "bike park" here means **lift-access, downhill-oriented mountain bike
> riding** — a chairlift, gondola, or similar fixed lift carries riders
> (and usually bikes) uphill so they can ride trails back down.

Explicitly excluded, even when the operator's own marketing says "bike
park":
- Pump tracks, dirt jump lines, skills parks, BMX-style facilities — no
  lift, no real vertical descent.
- **Shuttle access** — a truck or van with bike racks driving riders to a
  trailhead. No fixed lift, so it doesn't qualify no matter how good the
  descent is. (A park that's mostly lift-served but uses a shuttle for one
  lower section, the way some US parks do, is still in-scope — the test is
  whether the *primary* access is a lift.)

This is already Canada's stated policy — see the footer copy
(`footerNote` in the `T` translations, both `en`/`fr`): "Inclusion requires
chairlift or gondola access for bikes; shuttle-only parks excluded." This
section exists so the *reasoning*, not just the rule, survives: when
vetting a "new park" candidate (see Recurring maintenance below), the test
is always "is there a lift," never "does the operator call it a bike
park."

## Who you're working with

Jon (repo owner) has no coding background and edits through GitHub's web UI,
not git. That means:
- Deliver complete files, not diffs/patches.
- Never invent park data. A gap ("trail count unknown") is honest; a guessed
  number isn't. If you can't verify something, say so and leave it out or
  flag it, don't fill it in.
- Ask before restructuring anything that touches more than the data block —
  a refactor means he has to re-paste and re-verify the whole file.

## Where things live (search for these markers, line numbers shift)

- `const PARKS = [` — the single source of truth. One object per park:
  `id`, `slug`, `province` (must match a `PROVINCES` code), `coords`,
  `vertM`/`vertFt` (both stored, never converted, so published figures
  aren't distorted by rounding), `trailsLabel` (display string, text not
  math) vs `trailCount`/`trailKm` (actual numbers, `trailKmEst` flags an
  estimate), `season`, `lift`, `badges`, `note`, `url`, `mapUrl`. Every
  text field with `{en, fr}` needs both languages filled in — a French
  visitor should never see English fallback text on a Canadian park.
- `const BADGE_ORDER` — the fixed badge vocabulary: `closed, soon, new, wc,
  worlds, gl, kodiak, comm, surf, lim, loam`. Meanings are in `badgeDesc` inside
  the `T` translations object (both `en` and `fr` copies — keep them in sync).
  `closed` is the status badge (see Maintenance below); a closed park's card also
  gets `.is-closed` (dashed outline — never dimmed text).
- `const THEMES` — 4 color schemes, each tagged `basemap: 'light'|'dark'` (descriptive
  only since the vector basemap; nothing reads it). `alpine` is the light one and the default.
- Basemap — search `CA_LAND_GEO` (vector land, lakes and city labels; see Gotchas below).

## Recurring maintenance: park openings & closures

This is a living guide of a fast-moving industry (new lift-served parks get
announced most years; existing ones occasionally go dark for a season or
close for good). When asked to update this tool, or periodically on your
own initiative, check for both directions:

**New parks (opened or announced).**
- Apply the Scope definition above first — a pump track, skills park, or
  shuttle-access operation calling itself a "bike park" doesn't belong
  here even if it's popular or newly opened.
- Sources: the resort's own site/press release, Trailforks region pages,
  Pinkbike/Bike Magazine/Freehub/ https://www.singletracks.com news coverage, local news for the region,
  NSAA (National Ski Areas Association) reporting for US-adjacent context,
  and Jon's own industry contacts (he's written primary-source-sourced
  corrections before — see `git log` for "Correct Bluewood entry..." on the
  sibling USA repo, sourced from a GM's own letter).
- Not yet open but announced/under construction → add it now with the
  `soon` badge, following the precedent of the Cypress Mountain entry
  (`git log --grep=Cypress`): fill in what's confirmed, and say "opening
  20XX" in the `note` rather than guessing specs that haven't been
  published yet.
- **Known trap:** the `soon` badge's tooltip text (`badgeDesc.soon`, both
  `en` and `fr`) is a single hardcoded string — currently "targeting a 2027
  opening." It applies to *every* park tagged `soon`, not just one. If a
  second `soon` park has a different target year, or 2027 arrives, that
  string needs to change (or become per-park) — don't let it silently go
  stale.
- Once a `soon` park actually opens: drop the `soon` badge, add `new`,
  and replace any estimated figures with confirmed ones from a primary
  source (resort site, or direct contact — cite it in the commit message,
  same pattern as the Bluewood correction).

**Temporary closures** (season skipped for financial, lift-mechanical,
wildfire/flood, or ownership-transition reasons — not just normal
off-season, which is already handled by each park's `season` field).
**Permanent closures** (resort shut the bike operation down for good).
- Canada has no `status` field; closures use the `closed` badge (built
  October 2026 for Sir Sam's, mirroring the USA guide's `data-status="closed"`
  rows). To close a park: put `'closed'` in its `badges`, set `season` to say
  "Closed for 20XX · …", and write the `note` (EN and FR) stating why and what
  the operator has said about reopening — say plainly when it is uncertain.
  The `badge--closed` colours are the `--badge-closed-*` tokens; the badge key
  and the Stats badge filter pick it up from `BADGE_ORDER`. Flag any new
  closure to Jon right away.
- Keep closed parks in the list rather than deleting them — this guide has
  historical/reference value (see how README changelog entries treat past
  corrections), and Whistler-era history matters to this audience. A
  closure is a status change, not grounds for removal. Removal is Jon's
  call, not a default.
- Cite the source in the commit message and, when the change is big enough
  to shift the total park count, update the README too (see
  `git log --grep=README` for the established one-line style: "Update
  README for Cypress Mountain and current park count").
- **Then run the park sync** (see "Park sync between the two guides"): any add, close,
  reopen, rename or move changes what the other guide's road trips show. If you can't run it,
  end the handover with the reminder line given there.

## Gotchas (recorded so nobody re-introduces them)

- **CARTO tiles require an API key now.** The map used to use CARTO's free
  raster basemaps (`basemaps.cartocdn.com`). CARTO gated that behind an
  account API key at some point, and the failure is sneaky: an
  unauthenticated request comes back **HTTP 200**, not an error, with
  "API KEY REQUIRED" burned directly into the tile image — so it looks
  like a rendering bug, not a dead tile source, and any error-count-based
  fallback never fires because there's no error to catch. Fixed by
  switching to OpenStreetMap's standard tile server (free, no key, no
  account) for both light and dark themes — dark themes get there via a
  CSS filter (`DARK_MAP_FILTER`) on the Leaflet tile pane instead of a
  second CARTO URL, with Esri's keyless World Street Map tiles as a
  fallback if OSM itself is ever unreachable. If CARTO ever comes back up
  as genuinely free again, that's a reason to *reconsider*, not a reason
  to assume the old code was fine — check the actual tile response before
  reverting.
- An earlier bug used the CARTO path `dark_matter_nolabels`, which isn't a
  real path (the *style* is named Dark Matter, the *path* is
  `dark_nolabels`) — every tile 404'd and the map was permanently blank.
  Not currently relevant (CARTO is gone), but if a raster tile provider
  is ever reintroduced, verify the literal URL path against that
  provider's docs rather than the display name of the style.
- **Resolved November 2026: the map has no tile server any more** (same fix as the USA
  guide). `CA_LAND_GEO` (search it) is Natural Earth 1:50m provinces and territories, the
  neighbouring countries (USA incl. Alaska, Greenland, Mexico) and large lakes, as real WGS84
  polygons baked into the file (~111 KB; Arctic islands simplified harder, since there are no
  parks or roads there). `CA_CITIES` adds ~120 place labels that appear by zoom level, because
  the tiles used to supply place names. Colours come from CSS (`.land-ca`, `.land-other`,
  `.land-lake`, `.map-city`) via `--map-water` / `--map-land` / `--map-other` / `--map-line`,
  which derive from each theme's own tokens, so theme switches need no JS. The map makes no
  outside requests and its max zoom is 10, since 1:50m outlines only get coarser beyond that.
  The OSM/Esri tile version is in git history before this change (main at `cbf0124`) if it
  is ever needed; re-check this file's CARTO notes above before reintroducing any tile host.

## Road-trip mode (Map tab; shared engine with the USA guide)

- Search `MAP DATA — US + Canada highway network` (`NA_ROADS`) and `ROAD TRIP`. The engine
  (`rtBuildGraph`, `rtSnap`, `rtSnapTrip`, `rtParksNear`, ...) is a **twin copy** of the USA
  guide's, byte-for-byte: fix it in one, make the same change in the other. `rtClass` (road costs:
  ferries ×2, US routes ×1.2, other numbered highways ×1.1) is shared too; only the `trip*` UI is
  per-guide.
- Data: Natural Earth 1:10m roads (see the cross-border note below for what `NA_ROADS` holds;
  Canadian ferries matter, Vancouver Island is unreachable without them). The same build script
  lives in both repos. No routing API, same
  reasoning as the tile gotcha above.
- Text is `T.en.trip` / `T.fr.trip`; both must stay complete. Distances follow `units`
  (corridor presets are round numbers in each system, see `TRIP_CORRIDORS`).
  `toggleView` hides the bar on Stats/Mountain (`tripSyncView`); `renderAll` re-labels it
  (`tripRenderText`).
- `rtSnapTrip` returns a route or `{ error: 'short' | 'noroad' | 'disconnected' | 'none' }`;
  a route carries `offStartKm` / `offEndKm`, and the page warns (EN/FR `farStart` / `farEnd` /
  `farBoth` / `farTail`) when a drawn end is over 30 km from a road. Sharp corners are
  must-visit points (`rtCorners`). The highway overlay shows only while drawing, dashed in
  `--gold` so it reads as a guide layer, distinct from the drawn sketch.
  A drawn end that runs past the roads (border, sea) is trimmed back to where the line leaves the
  road network, so a trip stops at the crossing the line used. Trip ends ignore road fragments
  under 300 km (`compKm`). Colour check for trip mode: `node tools/check-trip-colours.js` (needs
  Playwright). It measures the rendered colours in every theme and print, and the same file is
  in both repos.
  "Add to my trip": after a route is drawn every other park stays on the map as a tappable dot
  (`.trip-ghost-live`); ticking "Stop" in the list, or Add / Remove in a pin or dot popup, re-plans
  the trip through that park (`rtSnapTrip(G, sketch, vias)`; vias slot into the sketch in travel
  order and become must-visit points) and makes it a Google Maps stop (max 9). A park you added
  stays listed even if its road is outside the band.
  Whole-line coverage: after planning, the drawn point the route strays farthest from becomes a
  must-visit point when that gap is over 8% of the line (100–250 km) and a road is within 40 km;
  repeats up to 8 times. This is what makes a narrow loop (down the coast, back up the Rockies)
  get driven instead of cut across. Ordinary drawings never reach the threshold.
- **Cross-border trips (November 2026).** Both guides route on one network, `NA_ROADS` (search
  `MAP DATA — US + Canada highway network`): US interstates, US routes and Alaska's highways plus
  every Canadian road class and ferries, built together by `tools/build-road-network.py ... 0.01
  4 250 NA` so the border crossings connect. It is byte-identical in both pages, as are the engine
  and `rtClass` (one set of road costs). Each guide also carries a snapshot of the OTHER guide's
  parks, `OTHER_PARKS` (between the `OTHER_PARKS:BEGIN` / `OTHER_PARKS:END` markers), so trips
  list, pin and route through parks across the border, tagged with their country and linked to
  their own guide. Each guide stays the only place its own parks are edited. **Keeping that
  snapshot current is the park sync: see "Park sync between the two guides" below, and follow
  it exactly.**
  **Park access roads (November 2026).** Natural Earth stops short of many resorts (CO-135 to
  Crested Butte and US-26 over Mt. Hood aren't in it), so `NA_ROADS` also holds ~50 access
  roads from OpenStreetMap: `tools/park-access.geojson`, fetched once from the public OSRM
  router by `tools/fetch-park-access.py` for every park more than 15 km from the network, up to
  three roads per park in different directions, and committed. The page fetches nothing; the
  roads are baked in like the rest. ODbL requires the "(c) OpenStreetMap contributors" credit
  (USA: footer credit line; Canada: map attribution): keep it while these roads are in the data.
  Every park was within 14 km of a routable road after this change; the park sync check flags
  any new or moved park that isn't.
- Open idea, not scheduled: a separate Routes tab (see the USA repo README). Ask first.

## Park sync between the two guides (required; follow this exactly)

The two guides depend on each other. Each page carries a snapshot of the OTHER guide's parks
(`OTHER_PARKS`) so road trips can list, pin and route through parks across the border. The
snapshot is only refreshed by running the sync, so after a park is added, removed, closed or
reopened, renamed, moved or has its vertical changed in either guide, the other guide's road
trips keep showing the old details until someone runs it. Use the steps below. Don't improvise
or explore: the commands do the comparing, and you never need to open either `index.html` to sync.

**Reminder rule.** Whenever a session changes the park list in either guide (any of the edits
above), run the sync as the last step of that same change if both repos are in the session
(steps 1-5). If the other repo isn't attached and can't be added, end the handover to Jon with
this line, word for word:
> A park sync is recommended: the other guide's road trips still show the old details for
> <park(s)>. Ask any Claude session to "run the park sync".

**When Jon asks for a sync ("run the park sync", "sync the guides"):**
1. Both repos must sit side by side (`../USA-bike-parks`, `../Canada-mtb-parks`). If one is
   missing, attach it with `add_repo` (`postmillennium-MTB/USA-bike-parks` or
   `postmillennium-MTB/Canada-mtb-parks`) and clone it next to the other on the same branch.
   Playwright is pre-installed in cloud sessions; don't install it.
2. From either repo root, run the read-only check (it writes nothing):
   `node tools/sync-other-parks.js --check ../USA-bike-parks ../Canada-mtb-parks`
   It prints, for each guide, when its snapshot was last synced and every park added, removed
   or changed since then (with the field that changed), or "up to date".
3. Report to Jon: the last sync date for each direction, and the differences, copied from the
   output.
4. **If both say "up to date": take no action.** No files change and there's no commit. Report
   that and ask Jon whether more review is warranted. A check for real-world park openings and
   closures is the separate "Recurring maintenance" task above, not part of a sync, and costs
   far more (web research), so only do it if he says yes.
5. **If there are differences:** run the same command without `--check`. It rewrites only the
   snapshot(s) that are out of date. Commit in each repo that changed, with a message naming the
   parks (e.g. "Sync OTHER_PARKS snapshot: Telluride, Powder Mountain reopened"), and push to
   the session's branch.
6. **Only if the check printed `FAR FROM ROADS`** for a park (new or moved, more than 15 km from
   the road-trip network): it needs an access road, or trips can't end there. Ask Jon before
   doing this, because it rebuilds the road data in both pages. Run these from the USA repo root
   (the scratch folder can be any temp folder):
   - download and unzip Natural Earth roads: `https://naciscdn.org/naturalearth/10m/cultural/ne_10m_roads.zip`
     (`pip install pyshp shapely` if needed)
   - `python3 tools/build-road-network.py <ne>/ne_10m_roads <tmp>/roads-base.json 0.01 4 250 NA`
   - `python3 tools/fetch-park-access.py <tmp>/roads-base.json index.html ../Canada-mtb-parks/index.html tools/park-access.geojson`
     (keeps every existing access road and only fetches the new far parks)
   - `python3 tools/build-road-network.py <ne>/ne_10m_roads <tmp>/roads.json 0.01 4 250 NA tools/park-access.geojson`
   - `python3 tools/install-road-network.py <tmp>/roads.json index.html ../Canada-mtb-parks/index.html`
     (must print "identical in all pages")
   - copy `tools/park-access.geojson` to the Canada repo, update the km/KB totals in the
     comment above `NA_ROADS` in both pages if they moved, draw one trip to the new park in a
     browser, and commit both repos naming the park and "access road (OpenStreetMap)".
   Without the 7th argument `build-road-network.py` reproduces the base network exactly; with
   it, it reproduces the shipped `NA_ROADS` exactly. If either doesn't match, stop and report;
   don't push a mismatched road network.

## Mountain chart and page texture (shared with the USA guide)

- **Mountain tab = `renderPeakChart`** (search `PEAK CHART`; styles are the
  `.pk-*` rules). It is a **twin copy**: the same block, byte-for-byte, sits in
  the USA repo. Fix or tune it in one, make the same change in the other. Each
  repo only supplies a small "park → item" function (`drawMountainStage` /
  `drawMtnStage`) and a few `--pk-*` theme variables. It draws SVG at 1:1 pixel
  scale (never shrunk to fit) and picks a label style from the pixel width per
  peak: horizontal names (wide) → 90°-rotated names and values (rot) → no printed
  labels, hover/tap only (dense). Hover or keyboard focus floats the name over the
  peak; on touch, first tap shows it and a second tap removes the peak. A peak
  that was not on the previous render plays a one-off shimmer (`pk-fresh`).
- **Page texture = two layers from the PMR texture catalogue**
  (`postmillennium-MTB/pmr-website` → `textures/`), designed in the texture studio:
  layer 1 `crowe-1882-12657` (adapted from US Design Patent 12,657, Eugene A.
  Crowe, 1882) at 140px, strongest at the right edge; layer 2 `us-d268339` (US
  Design Patent 268,339, line art) at 64px, strongest at the left edge. The two
  fades hand off to each other so they never sit at full strength together.
  `.texture` and `.texture-2` are the first children of `<body>`; retint a theme by
  changing only its `--tex-ink` / `--tex-opacity` / `--tex-2-opacity`. Alpine uses
  the studio values exactly (`#624D2B`, .235 / .28); the dark themes ink with their
  own `--gold-dim` at .14 / .18 so muted text stays ≥ 6.8:1 over the inked pixels
  (Alpine's muted text is 4.7–5.0:1 at the most heavily inked pixels — that is the
  studio design, accepted). Catalogue rules apply: `position:absolute` (never fixed
  — Pinkbike embeds clip it). The chart backdrop reuses `--tex-mask` at 520px with a
  scoped, quieter `--tex-opacity` set in the `.pk-stage` hook. Patterns are described
  as "adapted" where the catalogue says so; us-d268339's inventor/date are
  unverified, so it is cited by number only. The credit line (EN/FR
  `textureCredit`) is required — keep it.
- `low-pile-carpet.css` (repo root of the Canada repo) is an unused, reusable
  procedural texture kit for small accents (cards, plates). Not wired into the
  page.

## Color schemes and contrast ("would this survive being printed?")

Standard for every theme, solved numerically against that theme's real surfaces
(not by eye) — keep it when retinting or adding a theme:
- `--text` ≥ 11.5:1, `--text-dim` ≥ 9:1, `--text-muted` ≥ 7:1, accent-as-text
  (`--gold`, `--green`) ≥ 7:1 on every page/card surface. `--border-lit` (control
  outlines) ≥ 3:1, `--border` (card outlines) ≥ 2:1.
- Text never sits directly on a hue-only fill: province chips use `--text` with the
  province hue in the fill and border; pills use a dark fill with near-white text.
- Province colours are data encodings but must each hold ≥ 3:1 on all four themes
  (mid-luminance window), and each province has its own hue. AB and YK used to be
  the same colour; YK is now violet.
- No dimming text with `opacity` or translucent white — use a solid token.
- Map: coast and province lines use `--border-lit` (>= 3:1 on the land in every theme), city
  labels `--text-muted` with a land-coloured halo (>= 7:1).
- `@media print` (search `PRINT / SAVE-AS-PDF PALETTE`) forces the solved Alpine
  palette for every theme, because browsers drop dark backgrounds when printing and
  light text on white vanishes. No print button exists by design; the block only
  acts when someone prints or saves to PDF.
- Audit method: load each theme in a browser, walk every visible text node, composite
  its colour over the effective background, compare to 4.5 (3 for large text) and 7.
  Status at last run: Canada, all 4 themes + print: every item ≥ 7:1.

## License and notice (do not remove)

This repo is licensed under PolyForm Noncommercial 1.0.0 (`LICENSE`). Every edit and rebuild must keep: the `Required Notice:` line at the top of `LICENSE`; the (c) / SPDX comment right after the doctype of each HTML page; and the visible `.pmr-license` footer on each page. Do not remove, reword or hide them. New pages get the same footer. Third-party material keeps its own license: never relicense it, and keep its notices. Jon holds the copyright and decides any license change.
