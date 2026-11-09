"""Put a rebuilt road network (the JSON from build-road-network.py) into both guides as NA_ROADS.
The same script lives in the USA and Canada guides; both pages must carry the identical string.

Usage:  python3 tools/install-road-network.py roads.json ../USA-bike-parks/index.html ../Canada-mtb-parks/index.html
Only the JSON after "const NA_ROADS = " is replaced; the comment above it (which states the build
arguments and the km / KB totals) is not, so update those numbers by hand if they moved.
"""
import sys, re, json
data = open(sys.argv[1]).read().strip()
json.loads(data)   # refuse anything that isn't valid JSON
pat = re.compile(r'(const NA_ROADS = )(\{.*?\})(;\n)')
for page in sys.argv[2:]:
    s = open(page, encoding='utf-8').read()
    m = pat.search(s)
    if not m: sys.exit('NA_ROADS not found in ' + page)
    old = len(m.group(2))
    s = s[:m.start(2)] + data + s[m.end(2):]
    open(page, 'w', encoding='utf-8').write(s)
    print(f'{page}: NA_ROADS {old} -> {len(data)} bytes')
vals = {pat.search(open(p, encoding='utf-8').read()).group(2) for p in sys.argv[2:]}
print('identical in all pages' if len(vals) == 1 else 'WARNING: pages differ')
