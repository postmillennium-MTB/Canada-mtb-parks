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
- `const BADGE_ORDER` — the fixed badge vocabulary: `soon, new, wc, worlds,
  gl, kodiak, comm, surf, lim, loam`. Meanings are in `badgeDesc` inside the
  `T` translations object (both `en` and `fr` copies — keep them in sync).
  There is **no `closed` badge yet** — see Maintenance below.
- `const THEMES` — 4 color schemes, each tagged `basemap: 'light'|'dark'`.
  `alpine` is the light one and the default.
- Basemap/tile logic — search `OSM_TILES` — see Gotchas below before
  touching this.

## Recurring maintenance: park openings & closures

This is a living guide of a fast-moving industry (new lift-served parks get
announced most years; existing ones occasionally go dark for a season or
close for good). When asked to update this tool, or periodically on your
own initiative, check for both directions:

**New parks (opened or announced).**
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
- Canada's data schema has no `status` field or `closed` badge today — the
  sibling USA repo already solved this (search its `CLAUDE.md` / its
  `data-status="closed"` rows for the exact pattern: a dimmed row style, a
  "Closed" tag, and a note explaining why + expected reopening if any).
  The first time a Canadian park needs this, mirror that pattern here:
  add a `closed` entry to `BADGE_ORDER` + `badgeDesc` (both languages), a
  corresponding CSS treatment, and say so in the `note`. That touches
  rendering logic in a few places, not just the data block — **ask Jon
  before building it out**, but do flag the closure to him immediately
  either way rather than sitting on it.
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
