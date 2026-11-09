"""Build the road-trip highway network baked into index.html: US_ROADS in the
USA guide, CA_ROADS in the Canada guide. The same script lives in both repos.

Source: Natural Earth 1:10m "Roads" (ne_10m_roads, public domain,
https://www.naturalearthdata.com/downloads/10m-cultural-vectors/roads/).
USA: sov_a3 = USA; type "Major Highway" or "Beltway" (interstates and other
expressways) plus "Secondary Highway" at level "Federal" (US routes), plus
Alaska's state highways (Alaska has no US routes; without them Alyeska and
Hilltop are unreachable). Named I-90 / US-2 / AK-1 / SR-9.
CAN: sov_a3 = CAN; every class, because Canada's major-highway layer alone is too
sparse to reach the parks, plus "Ferry Route" (Vancouver Island is otherwise
unreachable). Québec autoroutes (level "Interstate", a known A-number, east of
80°W) are named A-20, ferries "Ferry", everything else by its bare number
("1", "401").
NA: both of the above in one network (each country keeps its own rules and
names), joined where the highways cross the border. This is what both guides
ship as NA_ROADS, so road trips can cross the border.

Steps: join lines where they cross or nearly touch (2 km), collapse interchange
clusters (~1.6 km) into one junction, close gaps in the source (a dead end
joins the same highway within ~50 km, or any road within ~6 km, but only when
the network doesn't already connect them), merge pass-through chains, drop
pieces under 40 km, simplify (~1 km), round to 0.004 deg and polyline-encode.

Output JSON: {"q": 250, "names": [...], "edges": "<edge> <edge> ..."}; each
edge is the encoded name index followed by its encoded lat/lng deltas.

Park access roads: Natural Earth stops short of many resorts (CO-135 to Crested Butte isn't in
it at all). An optional 7th argument adds tools/park-access.geojson, the last stretch of road to
each park more than 15 km from the network, fetched once from OpenStreetMap (via the OSRM
router) by fetch-park-access.py and committed with the repo; (c) OpenStreetMap contributors, ODbL.

Usage:  pip install pyshp shapely
        python3 build-road-network.py ne_10m_roads roads.json [simplify_deg cluster_units q country [access.geojson]]
Shipped data: 0.01 4 250 NA tools/park-access.geojson (both guides). USA / CAN build one
country only. Build without the 7th argument to get the base network fetch-park-access.py needs.
"""
import shapefile, sys, json, collections, math
from shapely.geometry import LineString, Point
from shapely.ops import unary_union, nearest_points
from shapely.strtree import STRtree
SRC, OUT = sys.argv[1], sys.argv[2]
SNAP, SIMP = 0.02, float(sys.argv[3]) if len(sys.argv) > 3 else 0.01
Q = int(sys.argv[5]) if len(sys.argv) > 5 else 250
COUNTRY = sys.argv[6] if len(sys.argv) > 6 else 'USA'
# NA = both countries in one network, noded together so the border crossings connect
WANT = {'USA': {'USA'}, 'CAN': {'CAN'}, 'NA': {'USA', 'CAN'}}[COUNTRY]
# Natural Earth tags Canadian freeways "Interstate" coast to coast; only Québec's are autoroutes
QC_AUTOROUTES = {'5', '10', '13', '15', '19', '20', '25', '30', '31', '35', '40', '50', '55', '70', '73',
                 '85', '410', '440', '520', '540', '573', '610', '640', '720', '730', '740', '930', '955', '973'}
r = shapefile.Reader(SRC)
src = []
for sr in r.iterShapeRecords():
    d = sr.record.as_dict()
    if d['sov_a3'] not in WANT: continue
    ctry = d['sov_a3']
    t, lv = d['type'], d['level']
    n = (d['name'] or '').strip()
    numbered = n.isdigit() or (n[:-1].isdigit() and n)
    if ctry == 'USA':
        # Alaska has no US-numbered routes: its highways (Seward, Glenn, Parks...) are state routes
        alaska = any(x < -129 and y > 51 for x, y in sr.shape.points)
        if not (t in ('Major Highway', 'Beltway') or (t == 'Secondary Highway' and lv == 'Federal')
                or (alaska and t in ('Secondary Highway', 'Major Highway'))): continue
        if numbered: n = ('I-' if lv == 'Interstate' else 'US-' if lv == 'Federal' else 'AK-' if alaska else 'SR-') + n
    else:
        if t not in ('Major Highway', 'Beltway', 'Secondary Highway', 'Road', 'Ferry Route'): continue
        if t == 'Ferry Route': n = 'Ferry'
        elif numbered and lv == 'Interstate' and n in QC_AUTOROUTES and sr.shape.points[0][0] > -80: n = 'A-' + n
    pts = sr.shape.points
    for i, s in enumerate(sr.shape.parts):
        e = sr.shape.parts[i+1] if i+1 < len(sr.shape.parts) else len(pts)
        seg = pts[s:e]
        if len(seg) >= 2: src.append((LineString(seg), n))
# optional park access roads (tools/park-access.geojson, from fetch-park-access.py): the last
# stretch of road to resorts Natural Earth doesn't reach, (c) OpenStreetMap contributors, ODbL
ACCESS = sys.argv[7] if len(sys.argv) > 7 else None
if ACCESS:
    for f in json.load(open(ACCESS))['features']:
        src.append((LineString(f['geometry']['coordinates']), f['properties']['road']))
lines = [l for l, _ in src]
tree = STRtree(lines)
connectors = []
for i, l in enumerate(lines):
    for pt in (Point(l.coords[0]), Point(l.coords[-1])):
        best = None
        for j in tree.query(pt.buffer(SNAP)):
            if j == i: continue
            dd = lines[j].distance(pt)
            if dd < 1e-9: best = None; break
            if dd <= SNAP and (best is None or dd < best[0]): best = (dd, j)
        if best:
            q = nearest_points(pt, lines[best[1]])[1]
            connectors.append(LineString([pt.coords[0], q.coords[0]]))
noded = unary_union(lines + connectors)
segs = list(noded.geoms)
print('noded segments', len(segs), 'connectors', len(connectors))
# name each noded segment from its source line
names = []; nidx = {}
def name_of(seg):
    m = seg.interpolate(0.5, normalized=True)
    best = None
    for j in tree.query(m.buffer(1e-6)):
        dd = lines[j].distance(m)
        if best is None or dd < best[0]: best = (dd, j)
    if best is None or best[0] > 1e-6: return ''
    return src[best[1]][1]
def key(c): return (round(c[0]*Q), round(c[1]*Q))
edges = []
for s in segs:
    nm = name_of(s)
    c = [key(p) for p in s.coords]
    if c[0] == c[-1] and len(set(c)) < 2: continue
    edges.append([nm, c])
# collapse interchange clusters: endpoints within CL quantised units become one node
CL = int(sys.argv[4]) if len(sys.argv) > 4 else 4
endpts = set()
for _, c in edges: endpts.add(c[0]); endpts.add(c[-1])
cpar = {p: p for p in endpts}
def cf(x):
    while cpar[x] != x: cpar[x] = cpar[cpar[x]]; x = cpar[x]
    return x
grid = collections.defaultdict(list)
for p in endpts: grid[(p[0]//CL, p[1]//CL)].append(p)
for p in endpts:
    gx, gy = p[0]//CL, p[1]//CL
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for o in grid.get((gx+dx, gy+dy), ()):
                if o != p and abs(o[0]-p[0]) <= CL and abs(o[1]-p[1]) <= CL: cpar[cf(o)] = cf(p)
members = collections.defaultdict(list)
for p in endpts: members[cf(p)].append(p)
rep = {}
for root, ms in members.items():
    cx = round(sum(m[0] for m in ms)/len(ms)); cy = round(sum(m[1] for m in ms)/len(ms))
    for m in ms: rep[m] = (cx, cy)
ne = []
seen = set()
for nm, c in edges:
    a, b = rep[c[0]], rep[c[-1]]
    if a == b: continue                      # edge internal to one interchange
    c = [a] + c[1:-1] + [b]
    sig = (min(a, b), max(a, b), len(c) < 4)
    if len(c) < 4 and sig in seen: continue  # duplicate short link between same two nodes
    seen.add(sig); ne.append([nm, c])
edges = ne
print('after collapse', len(edges))
# close data gaps: a dead end joins the nearest node of the SAME road within SAME_GAP (the
# highway resumes after a gap in the source), else any road's node within ANY_GAP; skipped
# when the network already links the two within 3x the straight-line distance
SAME_GAP, ANY_GAP = 0.45*Q, 0.06*Q
deg = collections.Counter(); nodename = collections.defaultdict(set)
for nm, c in edges:
    deg[c[0]] += 1; deg[c[-1]] += 1; nodename[c[0]].add(nm); nodename[c[-1]].add(nm)
dead = [p for p, k in deg.items() if k == 1]
allnodes = list(deg)
def dq(a, b):
    return math.hypot((a[0]-b[0])*math.cos(math.radians(a[1]/Q)), a[1]-b[1])
import heapq
adjn = collections.defaultdict(list)
def addadj(nm, c):
    L = sum(dq(p, q) for p, q in zip(c, c[1:]))
    adjn[c[0]].append((c[-1], L)); adjn[c[-1]].append((c[0], L))
for nm, c in edges: addadj(nm, c)
def netdist(a, b, cap):
    best = {a: 0}; h = [(0, a)]
    while h:
        d, n = heapq.heappop(h)
        if n == b: return d
        if d > best.get(n, 1e18) or d > cap: continue
        for o, L in adjn[n]:
            if d + L < best.get(o, 1e18): best[o] = d + L; heapq.heappush(h, (d + L, o))
    return 1e18
added = 0; gaps = []; left = 0
for a in dead:
    nm_a = nodename[a] - {''}
    best = None
    for b in allnodes:
        if b == a: continue
        d = dq(a, b)
        lim = SAME_GAP if (nm_a & nodename[b]) else ANY_GAP
        if d <= lim and (best is None or d < best[0]): best = (d, b)
    if best is None: left += 1; continue
    d, b = best
    if netdist(a, b, 3*d) <= 3*d: left += 1; continue
    nm = sorted(nm_a & nodename[b])[0] if (nm_a & nodename[b]) else ''
    edges.append([nm, [a, b]]); addadj(nm, [a, b]); added += 1; gaps.append(d/Q*111)
print('gap links', added, 'same-road gaps km max', round(max(gaps) if gaps else 0), 'dead ends left', left)
# merge chains through pass-through (degree-2) nodes; adjacency rebuilt from scratch each pass
while True:
    adj = collections.defaultdict(list)
    for k, (nm, c) in enumerate(edges):
        adj[c[0]].append(k); adj[c[-1]].append(k)
    done = set(); merged = 0; alive = [True]*len(edges)
    for node, ks in adj.items():
        if len(ks) != 2: continue
        a, b = ks
        if a == b or a in done or b in done: continue
        ca, cb = edges[a][1], edges[b][1]
        if ca[-1] != node: ca = ca[::-1]
        if cb[0] != node: cb = cb[::-1]
        if ca[0] == cb[-1]: continue
        nm = edges[b][0] if len(cb) > len(ca) else edges[a][0]
        edges[a] = [nm, ca + cb[1:]]; alive[b] = False
        done.add(a); done.add(b); merged += 1
    edges = [e for k, e in enumerate(edges) if alive[k]]
    if not merged: break
# components; drop tiny ones (< 40 km total)
par = {}
def f(x):
    while par.setdefault(x, x) != x: par[x] = par[par[x]]; x = par[x]
    return x
for _, c in edges: par[f(c[0])] = f(c[-1])
def km(c):
    t = 0
    for (x1, y1), (x2, y2) in zip(c, c[1:]):
        dx = (x2-x1)/Q*math.cos(math.radians((y1+y2)/2/Q)); dy = (y2-y1)/Q
        t += 111.32*math.hypot(dx, dy)
    return t
compkm = collections.Counter()
for _, c in edges: compkm[f(c[0])] += km(c)
print('components', len(compkm), 'top km', [round(v) for _, v in compkm.most_common(6)])
edges = [e for e in edges if compkm[f(e[1][0])] >= 40]
# simplify interior (endpoints fixed)
def simplify(c):
    if len(c) < 3: return c
    ls = LineString(c).simplify(SIMP*Q, preserve_topology=False)
    out = [tuple(map(int, map(round, p))) for p in ls.coords]
    out[0], out[-1] = c[0], c[-1]
    return out
def enc_num(v):
    v = ~(v << 1) if v < 0 else (v << 1); s = ''
    while v >= 0x20: s += chr((0x20 | (v & 0x1f)) + 63); v >>= 5
    return s + chr(v + 63)
def encode(c):
    s = ''; px = py = 0
    for x, y in c: s += enc_num(y-py) + enc_num(x-px); px, py = x, y
    return s
out = []
for nm, c in edges:
    c = simplify(c)
    if nm not in nidx: nidx[nm] = len(names); names.append(nm)
    out.append(enc_num(nidx[nm]) + encode(c))
js = json.dumps({'q': Q, 'names': names, 'edges': ' '.join(out)}, separators=(',', ':'))
open(OUT, 'w').write(js)
print('edges', len(out), 'names', len(names), 'bytes', len(js), 'total km', round(sum(compkm[k] for k in compkm if compkm[k]>=40)))
