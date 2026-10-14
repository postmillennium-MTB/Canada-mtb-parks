# Canada Lift-Served MTB Parks — Guide interactif

**29 parks · 7 provinces & territories · Bilingual EN/FR**
Part of [postmillenniumrenaissance.com](https://postmillenniumrenaissance.com)

Last update: October 2026.

[English](#english) · [Français](#français)

---

## English

### About

A single-file interactive HTML guide to every lift-served mountain bike park in Canada: parks reached by chairlift, gondola or similar fixed lift for bike uplift. It covers seven provinces and territories and was built for trail advocacy, tourism research and the Canadian MTB community.

It is fully bilingual (English/French), supports Metric / Imperial / Both unit display, and is self-contained. The only things loaded from the network are the map tiles and the Google Fonts stylesheet.

**Scope.** "Bike park" here means lift-access, downhill-oriented riding. Pump tracks, dirt-jump lines, skills parks and shuttle-only operations are excluded even when the operator calls them a bike park. The test is "is there a lift", never "does the operator call it a bike park". (Nitehawk, Sir Sam's, Mont Sutton and Vélo MSM are included with the *Surface Lift* or *Limited Uplift* badges so the limitation is visible.) See `CLAUDE.md` for the reasoning.

### Features

- Province-by-province accordion with park cards: vertical, trails, season, lift type, badges
- French/English toggle: UI strings, park notes and badge labels all switch
- Metric / Imperial / Both unit toggle (both figures are stored, never converted, so published numbers aren't distorted by rounding)
- Interactive Leaflet map with province-coloured markers and clustering
- **Stats** view: rank all parks by vertical drop or trail distance, or filter by badge
- **Mountain** view: pick parks and see their vertical drop as a skyline of peaks
  - label style adapts to how many peaks are shown (names under each peak, rotated names, or hover/tap only)
  - hover or keyboard focus floats the park name over its peak; on touch, first tap shows the name and a second tap removes the peak
  - a newly added peak shimmers once
- Trail Map and Learn More buttons on every park card
- Badge system with 10 badge types (see Badge Key) and a collapsible bilingual key
- Province filter and search
- Four colour schemes — Boreal, Granite, Maple (dark) and Alpine (light, the default) — with a theme switcher that remembers your choice

### Opening the widget

Open `index.html` in any modern browser. No web server, build step or installation is needed. All JavaScript (Leaflet 1.9.4, Leaflet.MarkerCluster 1.5.3) is embedded in the file.

For GitHub Pages, enable Pages on the repository; the file is already named `index.html`, so it is served at the site root.

### 29 parks by province / territory

28 are open; 1 (Cypress Mountain) is announced.

| Province / Territory | # | Parks |
|---|---|---|
| British Columbia | 12 | Whistler, Revelstoke, Kicking Horse, Fernie, Mount Washington, Sun Peaks, SilverStar, Big White, Panorama, Grouse Mountain, RED Mountain, Cypress Mountain (opening 2027) |
| Québec | 9 | Mont-Sainte-Anne, Bromont, Le Massif de Charlevoix, Camp Fortune, Montcalm, Sommet Saint-Sauveur, MbPark / Mont Blanc, Mont Sutton, Vélo MSM |
| Ontario | 2 | Horseshoe Valley, Sir Sam's (no MTB operation in 2026) |
| Alberta | 2 | WinSport, Nitehawk Adventure Park |
| New Brunswick | 2 | Parc-Vélo Sugarloaf, Poley Mountain |
| Nova Scotia | 1 | Wentworth |
| Yukon | 1 | Mount Sima |

Manitoba, Saskatchewan, Prince Edward Island, Newfoundland & Labrador, the Northwest Territories and Nunavut have no confirmed lift-served mountain bike parks.

### Badge key

| Badge | English | Français |
|---|---|---|
| Opening 2027 | Announced, not yet open — construction underway, targeting a 2027 opening | Annoncé, pas encore ouvert — construction en cours, ouverture ciblée pour 2027 |
| New 2025 | Opened or debuted in 2025 | Ouvert ou inauguré en 2025 |
| UCI World Cup | Has hosted UCI Downhill World Cup rounds | A accueilli des épreuves de Coupe du Monde UCI de descente |
| UCI World Championships | Has hosted the UCI Mountain Bike World Championships | A accueilli les Championnats du Monde UCI de vélo de montagne |
| Gravity Logic | Designed and/or built by Gravity Logic (Whistler, BC) | Conçu et/ou construit par Gravity Logic (Whistler, C.-B.) |
| Kodiak TW | Designed and/or built by Kodiak Trail Works | Conçu et/ou construit par Kodiak Trail Works |
| Community / Non-Profit | Community-owned, publicly-operated, or non-profit | Propriété communautaire, gestion publique ou OBNL |
| Surface Lift | Uses a surface/drag lift — not a chairlift or gondola | Utilise une remontée de surface — pas un télésiège ni une télécabine |
| Limited Uplift | Lift access is limited: specific days, times, or ride counts only | Accès par remontée limité : jours, horaires ou montées spécifiques |
| Loam Pass | Included in the Loam Pass multi-resort pass | Inclus dans le laissez-passer multi-destinations Loam Pass |

The badge list and its order live in one place (`BADGE_ORDER` in `index.html`); the descriptions are in the `badgeDesc` translations (both languages).

### Data sources

- Official park and resort websites
- Trailforks (trail network data and trail counts)
- Gravity Logic official client list (whistlergravitylogic.com/clients)
- Kodiak Trail Works
- UCI MTB World Series historical records
- Mountain Biking BC / Tourism BC
- Bike Magazine, Singletracks and Pinkbike for supplementary park details
- Base list: Two Wheeled Wanderer (Becky Timbers)

### Data notes

- Trail distances (km) are confirmed from official sources for two parks: Whistler (80 km) and Sun Peaks (89 km). Other parks list a trail count only; the guide does not guess a distance.
- Vertical drop is the lift-served vertical from the highest accessible lift terminal to the base, as published by the park. Both metres and feet are stored.
- Season dates, hours and lift availability change annually. Verify with each park before a visit.
- Grouse Mountain and RED Mountain opened in 2025 (Phase 1); counts and distances will grow. RED Mountain is Phase 1 of a four-phase Gravity Logic master plan.
- **Cypress Mountain** is announced but not open; construction is underway toward a summer 2027 target. The vertical shown (279 m / 915 ft) is the trail's published top-to-bottom descent, not the 356 m / 1,168 ft rise of the Raven Ridge chairlift. Trail count and distance haven't been published.
- **Sir Sam's** (ON) has no mountain-bike operation in 2026 while a new quad chairlift is built; 2027 will be assessed afterwards. Its figures reflect the last season it operated. The guide has no `closed` badge yet (see `CLAUDE.md`); the closure is stated in the park's note.
- **Mont Sutton** carries *Limited Uplift*: the resort positions its network as XC/enduro, not downhill, and chairlift access is per ride.
- **Vélo MSM** is a volunteer-run trail network; lift days are run by Mont Ste-Marie resort management, so confirm lift operation before visiting.
- Calabogie Peaks (ON) was a lift-served DH park but discontinued bike uplift in the mid-2000s and is excluded.

### Technical notes

- Single HTML file (about 440 KB including the embedded libraries); no build step, bundler or package manager
- Leaflet 1.9.4 and Leaflet.MarkerCluster 1.5.3 embedded inline
- **Map tiles:** OpenStreetMap's standard tile server (no key needed), with Esri's keyless World Street Map as a fallback if OSM is unreachable. Dark themes darken the tiles with a CSS filter. *(The map previously used CARTO tiles, which now require an API key and return an "API KEY REQUIRED" image with HTTP 200.)* OSM's usage policy discourages embedded production use at scale, so a bundled vector basemap (as the USA guide now has) is the long-term fix — it needs real province boundary geometry. See `CLAUDE.md`.
- Iframe-safe and mobile-first; designed to embed on postmillenniumrenaissance.com and in Pinkbike articles
- No analytics and no data collection; the only external requests are map tiles and Google Fonts

### Appearance

- **Colour schemes** are solved numerically, not by eye, for the "would this survive being printed or saved as a PDF?" standard: main text ≥ 11.5:1, secondary ≥ 9:1, muted ≥ 7:1, accent-as-text ≥ 7:1. Province colours each hold ≥ 3:1 on all four themes.
- **Print / Save as PDF** uses a built-in light palette for every theme, with the page texture hidden. There is deliberately no print button.
- **Page texture** is two faded layers from the PMR texture catalogue: `crowe-1882-12657` (adapted from US Design Patent 12,657, Eugene A. Crowe, 1882; the patent has long expired) and `us-d268339` (US Design Patent 268,339). Alpine uses the pattern as designed in the texture studio; the dark themes ink it in their own accent at lower strength. The credit line in the footer is required.
- `low-pile-carpet.css` is an unused, reusable procedural texture kit for small accents (cards, plates). It is not wired into the page.

### Credits

Developed for Post Millennium Renaissance for trail advocacy and community planning. Trail data and builder attributions were researched from publicly available sources.

Built with Leaflet.js (BSD 2-Clause) and Leaflet.MarkerCluster (MIT). Map imagery © OpenStreetMap contributors (Esri fallback). Background patterns from US Design Patent Nos. 12,657 and 268,339.

### Changelog

- Oct 2026 — Mountain tab rebuilt: legible labels at any park count, hover/tap name, one-time shimmer for new peaks
- Oct 2026 — Colour schemes revised for print/PDF-level contrast; print palette added
- Oct 2026 — Two-layer page texture from the PMR catalogue; footer wording unified with the USA guide
- Oct 2026 — README converted from README.docx to README.md and brought up to date (park count by province, tiles, Cypress and Sir Sam's status)

---

## Français

### À propos

Guide HTML interactif en fichier unique répertoriant les parcs de vélo de montagne desservis par remontée mécanique au Canada : parcs accessibles par télésiège, télécabine ou remontée fixe similaire pour le transport des vélos. Il couvre sept provinces et territoires et a été conçu pour le plaidoyer en faveur des sentiers, la recherche touristique et la communauté canadienne du vélo de montagne.

Il est entièrement bilingue (anglais/français), prend en charge l'affichage des unités métriques / impériales / les deux, et est autonome. Seuls les tuiles de la carte et la feuille de style Google Fonts sont chargées depuis le réseau.

**Portée.** Ici, « parc de vélo » signifie une descente desservie par remontée. Les pumptracks, lignes de dirt jump, parcs d'habiletés et services de navette seulement sont exclus, même si l'exploitant les appelle « parc de vélo ». Le critère : y a-t-il une remontée ? Voir `CLAUDE.md`.

### Fonctionnalités

- Affichage en accordéon par province avec fiches de parc (dénivelé, sentiers, saison, remontée, badges)
- Bascule français/anglais — interface, descriptions et libellés de badges
- Bascule d'unités métrique / impérial / les deux
- Carte Leaflet interactive avec marqueurs colorés par province et regroupement automatique
- Vue **Stats** : classer les parcs par dénivelé ou distance de sentiers, ou filtrer par badge
- Vue **Montagne** : choisir des parcs et comparer leur dénivelé sous forme de sommets (noms au survol ou au toucher, brève animation pour un sommet ajouté)
- Boutons Carte des sentiers et En savoir plus sur chaque fiche
- Système de 10 badges avec légende rétractable bilingue
- Filtre par province et barre de recherche
- Quatre thèmes de couleurs — Boréal, Granit, Érable (sombres) et Alpin (clair, par défaut) — le choix est mémorisé

### Ouverture

Ouvrez `index.html` dans un navigateur moderne. Aucun serveur, processus de construction ou installation n'est requis. Tout le JavaScript (Leaflet 1.9.4, Leaflet.MarkerCluster 1.5.3) est intégré au fichier. Pour GitHub Pages, activez Pages sur le dépôt : le fichier s'appelle déjà `index.html`.

### 29 parcs par province / territoire

Voir le tableau de la section anglaise — 28 parcs sont ouverts et 1 (Cypress Mountain) est annoncé. Les noms de parcs sont identiques en anglais et en français pour la plupart des parcs québécois. Le Manitoba, la Saskatchewan, l'Île-du-Prince-Édouard, Terre-Neuve-et-Labrador, les Territoires du Nord-Ouest et le Nunavut n'ont aucun parc de vélo desservi par remontée mécanique confirmé.

### Légende des badges

Voir le tableau bilingue de la section anglaise.

### Sources de données

Sites officiels des parcs et stations ; Trailforks ; liste officielle des clients de Gravity Logic ; Kodiak Trail Works ; archives de la Série mondiale UCI ; Mountain Biking BC / Tourisme BC ; Bike Magazine, Singletracks et Pinkbike ; liste de base : Two Wheeled Wanderer (Becky Timbers).

### Notes sur les données

- Les distances de sentiers (km) sont confirmées par des sources officielles pour deux parcs seulement : Whistler (80 km) et Sun Peaks (89 km). Les autres parcs n'indiquent que le nombre de sentiers.
- Le dénivelé est celui desservi par remontée, du terminus le plus haut jusqu'au pied, tel que publié par le parc. Mètres et pieds sont tous deux conservés.
- Les dates de saison, heures et disponibilité des remontées changent chaque année. Vérifiez auprès de chaque parc avant de planifier une visite.
- Grouse Mountain et RED Mountain ont ouvert en 2025 (phase 1). RED Mountain est la phase 1 d'un plan directeur en quatre phases de Gravity Logic.
- **Cypress Mountain** est annoncé mais pas encore ouvert ; ouverture ciblée pour l'été 2027. Le dénivelé indiqué (279 m / 915 pi) est la descente totale publiée du sentier, et non le dénivelé de 356 m / 1 168 pi du télésiège Raven Ridge.
- **Sir Sam's** (Ontario) n'exploite pas de vélo de montagne en 2026 pendant la construction d'un nouveau télésiège quadruple ; 2027 sera évalué ensuite.
- **Mont Sutton** porte le badge Remontée limitée : le centre positionne son réseau comme XC/enduro, non descente.
- **Vélo MSM** est un réseau géré par des bénévoles ; les jours de remontée sont assurés par la direction de Mont Ste-Marie — confirmez avant de vous déplacer.
- Calabogie Peaks (Ontario) a cessé le transport de vélos au milieu des années 2000 et est exclu.

### Notes techniques

- Fichier HTML unique (environ 440 Ko avec les bibliothèques intégrées) ; aucun processus de construction
- **Tuiles de la carte :** serveur de tuiles standard d'OpenStreetMap (sans clé), avec Esri en secours ; les thèmes sombres assombrissent les tuiles par un filtre CSS. (CARTO exige désormais une clé d'API.)
- Aucune analytique ni collecte de données ; seules requêtes externes : tuiles de carte et Google Fonts

### Apparence

Les thèmes sont calculés pour rester lisibles à l'impression ou en PDF (texte principal ≥ 11,5:1). Une palette claire intégrée s'applique à l'impression ; il n'y a volontairement aucun bouton d'impression. Le motif de fond combine deux couches du catalogue PMR : `crowe-1882-12657` (adapté du brevet américain de dessin no 12 657, Eugene A. Crowe, 1882 ; brevet expiré depuis longtemps) et `us-d268339` (brevet américain de dessin no 268 339).

### Crédits

Développé pour Post Millennium Renaissance pour le plaidoyer en faveur des sentiers et la planification communautaire. Construit avec Leaflet.js (BSD 2-Clause) et Leaflet.MarkerCluster (MIT). Imagerie cartographique © contributeurs OpenStreetMap (secours Esri).
