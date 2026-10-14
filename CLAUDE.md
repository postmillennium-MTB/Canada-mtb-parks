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
- `const THEMES` — 4 color schemes, each tagged `basemap: 'light'|'dark'`.
  `boreal` (dark) is the `:root` default; `granite`, `maple` and `alpine` are light
  (the dark ones were lifted/replaced in Oct 2026 because they read too dark and flat).
- Basemap/tile logic — search `OSM_TILES` — see Gotchas below before
  touching this.

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
- **This repo still runs on tiles (OSM + Esri fallback) — the sibling USA
  repo does not anymore.** USA replaced its raster basemap outright with
  real vector state-boundary polygons baked into the file (see its
  CLAUDE.md), which permanently ends this whole class of bug rather than
  swapping to a different tile host that will eventually squeeze its free
  tier too, or get rate-limited (OSM's own usage policy already says its
  tile server isn't meant for embedded production use at real traffic —
  the current fix here is a reprieve, not a permanent one). The reason
  Canada didn't get the same fix in the same session: doing it right needs
  *real* WGS84 province/territory boundary geometry Leaflet can project
  the normal way (matching how it already projects every park marker) —
  not a pre-projected decorative image. The obvious npm candidate,
  `@svg-maps/canada`, is exactly that: a static illustration in an unknown,
  undocumented projection, fine for a flat picture but not safely
  reverse-engineerable into real coordinates without guessing. A search of
  npm and PyPI (the only registries directly reachable from a standard
  sandboxed session, no general internet fetch) turned up nothing
  bundling genuine Canada admin-1 boundary data — `us-atlas` (used for the
  USA fix) has no Canadian counterpart. Two ways to unblock this:
  1. Jon downloads Natural Earth's `ne_50m_admin_1_states_provinces` (or
     Statistics Canada's own boundary files) himself and hands the file
     over — either converts in minutes once the raw geometry exists.
  2. A future session with broader network access fetches it directly.
  Don't reach for `@svg-maps/canada` as a shortcut in the meantime; a
  province boundary that's subtly wrong everywhere is worse than the
  current tile dependency, not better.

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
  the studio ink (`#624D2B`) but eased to .17 / .20 so the paper reads brighter; Granite and
  Maple are light and ink with their own tinted browns/blues at ~.13 / .08; Boreal inks with its
  own tinted ink (see its `body:not([data-theme])` block). Text tokens are solved against the
  flat surfaces; the texture sits under them at low opacity (re-measure over inked pixels
  if you raise it). Catalogue rules apply: `position:absolute` (never fixed
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
- `@media print` (search `PRINT / SAVE-AS-PDF PALETTE`) forces the solved Alpine
  palette for every theme, because browsers drop dark backgrounds when printing and
  light text on white vanishes. No print button exists by design; the block only
  acts when someone prints or saves to PDF.
- Audit method: load each theme in a browser, walk every visible text node, composite
  its colour over the effective background, compare to 4.5 (3 for large text) and 7.
  Status at last run: Canada, all 4 themes + print: every item ≥ 7:1.
