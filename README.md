# Canada Lift-Served MTB Parks — Guide interactif

**29 parks · 7 provinces & territories · Bilingual EN/FR**
Part of [postmillenniumrenaissance.com](https://postmillenniumrenaissance.com)

Last update: October 2026.

[English](#english) · [Français](#français)

---

## English

### About

A single-file interactive HTML guide to every lift-served mountain bike park in Canada: parks reached by chairlift, gondola or similar fixed lift for bike uplift. It covers seven provinces and territories and was built for trail advocacy, tourism research and the Canadian MTB community.

It is fully bilingual (English/French), supports Metric / Imperial / Both unit display, and is self-contained. The only thing loaded from the network is the Google Fonts stylesheet; the map is built in.

**Scope.** "Bike park" here means lift-access, downhill-oriented riding. Pump tracks, dirt-jump lines, skills parks and shuttle-only operations are excluded even when the operator calls them a bike park. The test is "is there a lift", never "does the operator call it a bike park". (Nitehawk, Sir Sam's, Mont Sutton and Vélo MSM are included with the *Surface Lift* or *Limited Uplift* badges so the limitation is visible.) See `CLAUDE.md` for the reasoning.

### Features

- Province-by-province accordion with park cards: vertical, trails, season, lift type, badges
- French/English toggle: UI strings, park notes and badge labels all switch
- Metric / Imperial / Both unit toggle (both figures are stored, never converted, so published numbers aren't distorted by rounding)
- Interactive Leaflet map with province-coloured markers and clustering
- **Road-trip mode** on the map: press *Plan a road trip*, draw your route with a finger or mouse, and it snaps to real highways (ferries included, so Vancouver Island works). Parks within a chosen distance are numbered in travel order with their km marker and how far off the route they sit; tick up to 9 as stops and open the trip in Google Maps. A loop drawn back to its start is planned as a round trip. Follows the language and units toggles.
- **Stats** view: rank all parks by vertical drop or trail distance, or filter by badge
- **Mountain** view: pick parks and see their vertical drop as a skyline of peaks
  - label style adapts to how many peaks are shown (names under each peak, rotated names, or hover/tap only)
  - hover or keyboard focus floats the park name over its peak; on touch, first tap shows the name and a second tap removes the peak
  - a newly added peak shimmers once
- Trail Map and Learn More buttons on every park card
- Badge system with 11 badge types (see Badge Key) and a collapsible bilingual key
- Province filter and search
- Four colour schemes, each named for a Father of Confederation — Sir John A. Macdonald (light, the default), Sir George-Étienne Cartier (blue), George Brown (brown) and Thomas D'Arcy McGee (green) — with a theme switcher that remembers your choice

### Opening the widget

Open `index.html` in any modern browser. No web server, build step or installation is needed. All JavaScript (Leaflet 1.9.4, Leaflet.MarkerCluster 1.5.3) is embedded in the file.

For GitHub Pages, enable Pages on the repository; the file is already named `index.html`, so it is served at the site root.

### 29 parks by province / territory

27 operated in 2026, Sir Sam's was closed for the season, and 1 (Cypress Mountain) is announced.

| Province / Territory | # | Parks |
|---|---|---|
| British Columbia | 12 | Whistler, Revelstoke, Kicking Horse, Fernie, Mount Washington, Sun Peaks, SilverStar, Big White, Panorama, Grouse Mountain, RED Mountain, Cypress Mountain (opening 2027) |
| Québec | 9 | Mont-Sainte-Anne, Bromont, Le Massif de Charlevoix, Camp Fortune, Montcalm, Sommet Saint-Sauveur, MbPark / Mont Blanc, Mont Sutton, Vélo MSM |
| Ontario | 2 | Horseshoe Valley, Sir Sam's (closed 2026; 2027 uncertain) |
| Alberta | 2 | WinSport, Nitehawk Adventure Park |
| New Brunswick | 2 | Parc-Vélo Sugarloaf, Poley Mountain |
| Nova Scotia | 1 | Wentworth |
| Yukon | 1 | Mount Sima |

Manitoba, Saskatchewan, Prince Edward Island, Newfoundland & Labrador, the Northwest Territories and Nunavut have no confirmed lift-served mountain bike parks.

### Badge key

| Badge | English | Français |
|---|---|---|
| Closed | Not operating this season — closed temporarily or for good; see the park note for the reason and any reopening plan | N'exploite pas cette saison — fermé temporairement ou définitivement ; voir la note du parc pour la raison et tout projet de réouverture |
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
- **Sir Sam's** (ON) carries the *Closed* badge: the 2026 mountain bike season was cancelled (trails closed, camps not held) while a new quad chairlift is built. The resort says only that it will assess resuming operations for 2027, so next season is uncertain. Its figures reflect the last season it operated (2025). Source: sirsams.ca/explore/mountain-biking.
- **Mont Sutton** carries *Limited Uplift*: the resort positions its network as XC/enduro, not downhill, and chairlift access is per ride.
- **Vélo MSM** is a volunteer-run trail network; lift days are run by Mont Ste-Marie resort management, so confirm lift operation before visiting.
- Calabogie Peaks (ON) was a lift-served DH park but discontinued bike uplift in the mid-2000s and is excluded.

### Technical notes

- Single HTML file (about 650 KB including the embedded libraries and highway data); no build step, bundler or package manager
- Leaflet 1.9.4 and Leaflet.MarkerCluster 1.5.3 embedded inline
- **Map:** real province, territory, neighbouring-country and lake outlines from Natural Earth (public domain) baked into the file, with city labels that appear as you zoom. No tile server, no outside requests, re-coloured by each theme. (It used OpenStreetMap tiles until November 2026; CARTO before that, until CARTO required an API key.)
- **Road-trip highways:** `CA_ROADS`, every Canadian road class plus ferries from Natural Earth's public-domain 1:10m roads (~74,000 km in ~28 KB), baked into the file. `tools/build-road-network.py ne_10m_roads out.json 0.01 4 250 CAN` rebuilds it exactly (the USA guide uses the same script). No routing server. Routing never crosses into the US yet; cross-border trips are a known next step.
- Iframe-safe and mobile-first; designed to embed on postmillenniumrenaissance.com and in Pinkbike articles
- No analytics and no data collection; the only external request is Google Fonts

### Appearance

- **Colour schemes** are solved numerically, not by eye, for the "would this survive being printed or saved as a PDF?" standard: main text ≥ 11.5:1, secondary ≥ 9:1, muted ≥ 7:1, accent-as-text ≥ 7:1. Province colours each hold ≥ 3:1 on all four themes.
- **Print / Save as PDF** uses a built-in light palette for every theme, with the page texture hidden. There is deliberately no print button.
- **Page texture** is two faded layers from the PMR texture catalogue, and each scheme has its own pairing: Macdonald uses `crowe-1882-12657` + `us-d268339`; Cartier `us-d268339` + `crowe-1882-12657` (teal inks); Brown `crowe-1884-14685` + `crowe-1882-13102` (amber inks); McGee `us-d268339` + `crowe-1882-13102` (green and purple inks, vertical fades). The Crowe patents (1882–1884) are adapted and long expired; `us-d268339` is US Design Patent 268,339. The dark schemes run their textures at low strength to protect text contrast. The credit line in the footer is required.
- `low-pile-carpet.css` is an unused, reusable procedural texture kit for small accents (cards, plates). It is not wired into the page.

### Colour scheme names

The four colour schemes are named for Fathers of Confederation. The active name shows beside the colour dots in the top bar on wide screens, and as a tooltip everywhere.

- **Sir John A. Macdonald** (light, the default): the primary architect of Confederation and the first Prime Minister of Canada, who led the movement to unite the British North American colonies into a single dominion.
- **Sir George-Étienne Cartier** (blue): a key joint-premier from Canada East (Quebec) who strongly promoted federalism and worked to ensure the protection of French-Canadian rights, language and civil law within the new union.
- **George Brown** (brown): a prominent journalist (founder of *The Globe* newspaper) and politician who built a crucial political coalition to help break a legislative deadlock and advance the framework for a federal system.
- **Thomas D'Arcy McGee** (green): a Father of Confederation, orator and journalist who passionately championed a unified, multi-ethnic Canadian nationality stretching from sea to sea.

### Credits

Developed for Post Millennium Renaissance for trail advocacy and community planning. Trail data and builder attributions were researched from publicly available sources.

Built with Leaflet.js (BSD 2-Clause) and Leaflet.MarkerCluster (MIT). Map outlines, place names and road-trip highways from Natural Earth (public domain). Background patterns from US Design Patent Nos. 12,657 and 268,339.

### Changelog

- Nov 2026 — Cross-border road trips: one shared US + Canada road network, so trips cross the border where highways do; US parks along a route are listed, tagged É.-U./USA and linked to the USA guide (snapshot refreshed by tools/sync-other-parks.js). Drawn loops are followed all the way round.
- Nov 2026 — Add to my trip: after a route is drawn, other parks stay on the map as dots; tapping one (or ticking “Stop”) re-plans the route through that park and adds it to the Google Maps link (EN/FR).
- Nov 2026 — Map tiles replaced by built-in Natural Earth outlines (provinces, neighbouring countries, lakes) and zoom-aware city labels; no tile server or outside requests, re-coloured by every theme.
- Nov 2026 — Road-trip review fixes: sharp corners in a drawing are must-visit points (Tremblant detours no longer get cut); clear EN/FR messages for lines over water, past the US border (with a link to the USA guide) or too short; park dots and dashed highways while drawing; overlapping trip pins merge into a "4–8" badge; Start/Finish labels kept clear of pins; one-row controls on phones; switching language mid-drawing keeps the instructions.
- Nov 2026 — Road-trip mode on the Map tab (draw a route, snap to highways and ferries, parks listed in travel order, Google Maps export); bilingual, follows units. Colours checked in all four schemes and print.
- Oct 2026 — Mountain tab rebuilt: legible labels at any park count, hover/tap name, one-time shimmer for new peaks
- Oct 2026 — Colour schemes revised for print/PDF-level contrast; print palette added
- Oct 2026 — Two-layer page texture from the PMR catalogue; footer wording unified with the USA guide
- Oct 2026 — `closed` badge added (Sir Sam's: 2026 season cancelled for a new quad chairlift, 2027 uncertain)
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
- **Mode virée** sur la carte : appuyez sur *Planifier une virée*, tracez votre trajet au doigt ou à la souris, et il s'aligne sur les routes réelles (traversiers compris, donc l'île de Vancouver fonctionne). Les parcs à la distance choisie sont numérotés dans l'ordre du trajet, avec leur repère kilométrique et leur distance du trajet ; cochez jusqu'à 9 arrêts et ouvrez la virée dans Google Maps. Suit les bascules de langue et d'unités.
- Vue **Stats** : classer les parcs par dénivelé ou distance de sentiers, ou filtrer par badge
- Vue **Montagne** : choisir des parcs et comparer leur dénivelé sous forme de sommets (noms au survol ou au toucher, brève animation pour un sommet ajouté)
- Boutons Carte des sentiers et En savoir plus sur chaque fiche
- Système de 11 badges avec légende rétractable bilingue
- Filtre par province et barre de recherche
- Quatre thèmes de couleurs — Boréal, Granit, Érable (sombres) et Alpin (clair, par défaut) — le choix est mémorisé

### Ouverture

Ouvrez `index.html` dans un navigateur moderne. Aucun serveur, processus de construction ou installation n'est requis. Tout le JavaScript (Leaflet 1.9.4, Leaflet.MarkerCluster 1.5.3) est intégré au fichier. Pour GitHub Pages, activez Pages sur le dépôt : le fichier s'appelle déjà `index.html`.

### 29 parcs par province / territoire

Voir le tableau de la section anglaise — 27 parcs ont été exploités en 2026, Sir Sam's était fermé pour la saison et 1 (Cypress Mountain) est annoncé. Les noms de parcs sont identiques en anglais et en français pour la plupart des parcs québécois. Le Manitoba, la Saskatchewan, l'Île-du-Prince-Édouard, Terre-Neuve-et-Labrador, les Territoires du Nord-Ouest et le Nunavut n'ont aucun parc de vélo desservi par remontée mécanique confirmé.

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
- **Sir Sam's** (Ontario) porte le badge Fermé : la saison de vélo de montagne 2026 a été annulée pendant la construction d'un nouveau télésiège quadruple. Le centre indique seulement qu'il évaluera la reprise pour 2027 ; la saison prochaine est incertaine.
- **Mont Sutton** porte le badge Remontée limitée : le centre positionne son réseau comme XC/enduro, non descente.
- **Vélo MSM** est un réseau géré par des bénévoles ; les jours de remontée sont assurés par la direction de Mont Ste-Marie — confirmez avant de vous déplacer.
- Calabogie Peaks (Ontario) a cessé le transport de vélos au milieu des années 2000 et est exclu.

### Notes techniques

- Fichier HTML unique (environ 650 Ko avec les bibliothèques et les données routières intégrées) ; aucun processus de construction
- **Carte :** contours des provinces, territoires, pays voisins et lacs tirés de Natural Earth (domaine public), intégrés au fichier, avec des noms de villes qui apparaissent au zoom. Aucun serveur de tuiles ni requête externe ; la carte suit chaque thème.
- **Routes des virées :** `CA_ROADS`, routes et traversiers canadiens tirés des routes 1:10m de Natural Earth (domaine public), intégrés au fichier ; aucun serveur d'itinéraires. Les itinéraires ne passent pas encore par les États-Unis.
- Aucune analytique ni collecte de données ; seules requêtes externes : tuiles de carte et Google Fonts

### Apparence

Les thèmes sont calculés pour rester lisibles à l'impression ou en PDF (texte principal ≥ 11,5:1). Une palette claire intégrée s'applique à l'impression ; il n'y a volontairement aucun bouton d'impression. Le motif de fond combine deux couches du catalogue PMR : `crowe-1882-12657` (adapté du brevet américain de dessin no 12 657, Eugene A. Crowe, 1882 ; brevet expiré depuis longtemps) et `us-d268339` (brevet américain de dessin no 268 339).

### Noms des thèmes de couleur

Les quatre thèmes portent le nom de Pères de la Confédération. Le nom actif s'affiche à côté des pastilles de couleur dans la barre du haut sur grand écran, et en info-bulle partout.

- **Sir John A. Macdonald** (clair, par défaut) : principal architecte de la Confédération et premier premier ministre du Canada, qui a mené le mouvement visant à unir les colonies de l'Amérique du Nord britannique en un seul dominion.
- **Sir George-Étienne Cartier** (bleu) : co-premier ministre du Canada-Est (Québec) qui a fermement défendu le fédéralisme et veillé à protéger les droits, la langue et le droit civil des Canadiens français au sein de la nouvelle union.
- **George Brown** (brun) : journaliste et politicien de premier plan (fondateur du journal *The Globe*), qui a bâti une coalition politique décisive pour sortir de l'impasse législative et faire avancer le cadre d'un système fédéral.
- **Thomas D'Arcy McGee** (vert) : Père de la Confédération, orateur et journaliste, ardent défenseur d'une nationalité canadienne unie et multiethnique, d'un océan à l'autre.

### Crédits

Développé pour Post Millennium Renaissance pour le plaidoyer en faveur des sentiers et la planification communautaire. Construit avec Leaflet.js (BSD 2-Clause) et Leaflet.MarkerCluster (MIT). Contours, localités et routes des virées : Natural Earth (domaine public).

## License

Copyright (c) 2026 Post Millennium Renaissance (https://www.postmillenniumrenaissance.com).

Released under the [PolyForm Noncommercial License 1.0.0](LICENSE). In short: free to use, copy, modify and share for any noncommercial purpose, including personal use, research, education, and use by charities, environmental-protection organizations and government institutions. Commercial use needs a separate license; ask through postmillenniumrenaissance.com. Copies must keep the `Required Notice:` line in `LICENSE`. The license text controls over this summary.

Facts, figures and quotations taken from third-party studies and sources remain the property of their authors. This license covers only this project's own code, selection and arrangement of material, and original text. Third-party components keep their own licenses.
