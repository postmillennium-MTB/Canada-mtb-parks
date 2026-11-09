"""Fetch the access roads that link far-off parks to the road-trip network (NA_ROADS).
The same script lives in the USA and Canada guides.

Natural Earth 1:10m, the source of NA_ROADS, has the highways but not the last stretch of road
up to many resorts: CO-135 from Gunnison to Crested Butte is missing entirely. This script finds
every park (both guides) more than FAR_KM in a straight line from the network and asks the
public OSRM router (OpenStreetMap roads) for the real drive from the park to the nearest
highway (plus up to two more roads out, in other directions, when they are nearly as quick). Each route
is cut where it first reaches the network, so only the missing road is kept. The result is a small GeoJSON file, tools/park-access.geojson, committed with the repo;
build-road-network.py adds it to NA_ROADS. Nothing is fetched when the page loads: the roads
are baked into the page like the rest of NA_ROADS.

Road data (c) OpenStreetMap contributors, ODbL 1.0 (https://www.openstreetmap.org/copyright).
The page footers credit it; keep that credit while these roads are in NA_ROADS.

Usage (run once when parks are added, or a park's position changes; ~1 request per second):
    python3 tools/build-road-network.py ne_10m_roads roads-base.json 0.01 4 250 NA
    python3 tools/fetch-park-access.py roads-base.json ../USA-bike-parks/index.html \\
        ../Canada-mtb-parks/index.html tools/park-access.geojson
roads-base.json must be built WITHOUT the access file, so earlier access roads don't count as
network. Parks already in the output file are kept as they are (delete the file to refetch all).
"""
import sys, json, re, math, time, os, ssl, urllib.request, collections

FAR_KM = 15          # parks farther than this (straight line) from the network get an access road
JOIN_KM = 0.8        # a route has reached the network once it is this close to it
ALT_TIME = 1.5       # another access road is kept if it is at most this much slower
MAX_ROADS = 3        # access roads per park at most
OSRM = 'https://router.project-osrm.org'
UA = 'pmr-bike-park-guides/1.0 (road-trip build tool)'

base, usa_html, ca_html, out_path = sys.argv[1:5]

def decode_num(s, i):
    r = sh = 0
    while True:
        b = ord(s[i]) - 63; i += 1
        r |= (b & 0x1f) << sh; sh += 5
        if b < 0x20: break
    return (~(r >> 1) if r & 1 else r >> 1), i

def load_network(path):
    d = json.load(open(path)); q = d['q']; lines = []
    for e in d['edges'].split(' '):
        _, i = decode_num(e, 0); x = y = 0; pts = []
        while i < len(e):
            dy, i = decode_num(e, i); dx, i = decode_num(e, i)
            y += dy; x += dx; pts.append((y / q, x / q))
        lines.append(pts)
    return lines

def km(a, b):
    cl = math.cos(math.radians((a[0] + b[0]) / 2))
    return 111.2 * math.hypot((b[1] - a[1]) * cl, b[0] - a[0])

# grid index of network segments (0.5 deg cells) for fast nearest-point queries
lines = load_network(base)
grid = collections.defaultdict(list)
def index_line(pts):
    for a, b in zip(pts, pts[1:]):
        for gy in range(int(math.floor(min(a[0], b[0]) * 2)), int(math.floor(max(a[0], b[0]) * 2)) + 1):
            for gx in range(int(math.floor(min(a[1], b[1]) * 2)), int(math.floor(max(a[1], b[1]) * 2)) + 1):
                grid[(gy, gx)].append((a, b))
for pts in lines: index_line(pts)

def nearest(p, reach=2):
    """(km, point) of the nearest network point within ~reach*0.5 deg."""
    best = (1e9, None); cl = math.cos(math.radians(p[0]))
    cy, cx = int(math.floor(p[0] * 2)), int(math.floor(p[1] * 2))
    for gy in range(cy - reach, cy + reach + 1):
        for gx in range(cx - reach, cx + reach + 1):
            for a, b in grid.get((gy, gx), ()):
                ax, ay = (a[1] - p[1]) * cl, a[0] - p[0]; bx, by = (b[1] - p[1]) * cl, b[0] - p[0]
                dx, dy = bx - ax, by - ay; L = dx * dx + dy * dy
                t = max(0, min(1, -(ax * dx + ay * dy) / L)) if L else 0
                d = 111.2 * math.hypot(ax + t * dx, ay + t * dy)
                if d < best[0]: best = (d, (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
    return best

def candidates(p):
    """The nearest network point in each of 8 compass sectors, within ~150 km."""
    cl = math.cos(math.radians(p[0])); best = {}
    cy, cx = int(math.floor(p[0] * 2)), int(math.floor(p[1] * 2))
    for gy in range(cy - 3, cy + 4):
        for gx in range(cx - 3, cx + 4):
            for a, b in grid.get((gy, gx), ()):
                for t in (0, .25, .5, .75, 1):
                    q = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])); d = km(p, q)
                    if d > 150: continue
                    sec = int((math.degrees(math.atan2(q[0] - p[0], (q[1] - p[1]) * cl)) + 180) // 45) % 8
                    if sec not in best or d < best[sec][0]: best[sec] = (d, q)
    return [q for _, q in sorted(best.values())]

def snapshot(html):
    s = open(html, encoding='utf-8').read()
    m = re.search(r'const OTHER_PARKS = (\{.*?\});\s*\n', s)
    d = json.loads(m.group(1))
    return [(p['name']['en'] if isinstance(p['name'], dict) else p['name'], p['coords']) for p in d['parks']]

# each guide carries the other's parks; together the two snapshots are every park in both guides
parks = snapshot(ca_html) + snapshot(usa_html)

ctx = ssl.create_default_context()
if os.path.exists('/root/.ccr/ca-bundle.crt'): ctx.load_verify_locations('/root/.ccr/ca-bundle.crt')
def get(url):
    for k in range(4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=60, context=ctx) as r: return json.load(r)
        except Exception as e:
            print('  retry', k + 1, e); time.sleep(2 ** (k + 1))
    raise SystemExit('OSRM did not answer: ' + url)

old = {}
if os.path.exists(out_path):
    for f in json.load(open(out_path))['features']: old.setdefault(f['properties']['park'], []).append(f)
def bearing(p, q):
    return math.degrees(math.atan2(q[0] - p[0], (q[1] - p[1]) * math.cos(math.radians(p[0]))))

def fetch_road(name, lat, lng, q):
    """OSRM route park -> q, kept from where it leaves the roads already known (an earlier access
    road of the same park) to where it first reaches the network. None if nothing new is left."""
    rt = get(f'{OSRM}/route/v1/driving/{lng:.5f},{lat:.5f};{q[1]:.5f},{q[0]:.5f}?overview=full&geometries=geojson&steps=true'); time.sleep(1)
    r = rt['routes'][0]
    line = [(c[1], c[0]) for c in r['geometry']['coordinates']]
    on = [nearest(pt, reach=1)[0] <= JOIN_KM for pt in line]
    s0 = next((i for i in range(len(line)) if not on[i]), None)
    if s0 is None: return None
    s0 = max(0, s0 - 1)
    cut = next((i for i in range(s0 + 1, len(line)) if on[i]), len(line) - 1)
    skipped = sum(km(a, b) for a, b in zip(line[:s0 + 1], line[1:s0 + 1]))
    line = line[s0:cut + 1]
    # start and end exactly on known roads (start only when it branches off an earlier one)
    if s0 > 0: line[0] = nearest(line[0], reach=1)[1] or line[0]
    line[-1] = nearest(line[-1], reach=1)[1] or line[-1]
    length = sum(km(a, b) for a, b in zip(line, line[1:]))
    if length < 2: return None
    # name the road by the route number it mostly follows ("CO 135" -> "CO-135"), counting only
    # the steps inside the part that was kept; a street name if the road has no number
    refs = collections.Counter(); names = collections.Counter(); run = 0
    for st in r['legs'][0]['steps']:
        a, run = run, run + st['distance']
        if run <= skipped * 1000: continue
        if a >= (skipped + length) * 1000: break
        ref = (st.get('ref') or '').split(';')[0].strip()
        if ref: refs[ref.replace(' ', '-')] += st['distance']
        elif st.get('name'): names[st['name']] += st['distance']
    road = (refs or names).most_common(1)[0][0] if (refs or names) else 'Access road'
    index_line(line)
    return {'type': 'Feature', 'properties': {'park': name, 'road': road, 'km': round(length, 1)},
            'geometry': {'type': 'LineString', 'coordinates': [[round(p[1], 5), round(p[0], 5)] for p in line]}}

features = []
# farthest parks first; each access road found counts as network for the parks after it, so two
# resorts up the same valley share one road instead of getting two different ones
far = sorted(((nearest(tuple(c), reach=3)[0], n, c) for n, c in parks), reverse=True)
for d0, name, (lat, lng) in far:
    if d0 <= FAR_KM: continue
    d0, _ = nearest((lat, lng), reach=3)
    if d0 <= FAR_KM: print('reached by an earlier access road:', name); continue
    if name in old:
        for f in old[name]:
            features.append(f); index_line([(c[1], c[0]) for c in f['geometry']['coordinates']])
        print('kept', name); continue
    cands = candidates((lat, lng))
    if not cands: print('no network near', name); continue
    coords = ';'.join(f'{q[1]:.5f},{q[0]:.5f}' for q in cands)
    tab = get(f'{OSRM}/table/v1/driving/{lng:.5f},{lat:.5f};{coords}?sources=0&annotations=duration'); time.sleep(1)
    # fastest, not shortest: the shortest drive is often a forest road, the fastest is the highway
    dur = tab['durations'][0][1:]
    ok = sorted((dur[i], i) for i in range(len(dur)) if dur[i] is not None)
    if not ok: print('no route for', name); continue
    picks = [ok[0][1]]
    # more roads out (up to MAX_ROADS), each leaving in a clearly different direction (>= 90 deg
    # from the others) and at most ALT_TIME x the fastest drive: Mt. Hood gets US-26 east, OR-35
    # north to Hood River and US-26 west to Portland (missing from Natural Earth)
    for t, i in ok[1:]:
        if t > ALT_TIME * ok[0][0] or len(picks) >= MAX_ROADS: break
        b = bearing((lat, lng), cands[i])
        if all(abs((b - bearing((lat, lng), cands[j]) + 180) % 360 - 180) >= 90 for j in picks): picks.append(i)
    for i in picks:
        f = fetch_road(name, lat, lng, cands[i])
        if f:
            features.append(f)
            print(f"{name}: {f['properties']['road']} {f['properties']['km']:.0f} km (straight line to network {d0:.0f} km)")
json.dump({'type': 'FeatureCollection',
           'note': 'Park access roads for NA_ROADS. (c) OpenStreetMap contributors, ODbL 1.0, via OSRM. Built by tools/fetch-park-access.py.',
           'features': features}, open(out_path, 'w'), indent=0)
print(len(features), 'access roads written to', out_path)
