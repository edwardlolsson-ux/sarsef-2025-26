# Artifact: OSM Roads Download (2025-11-16 10:23)

## Study Area
- Polygon stored at `data/study_area.geojson`
- Bounding box passed to Overpass: `(31.936315009166563, -111.25749929680498, 32.461266338249004, -110.62070967636338)`

## Steps
1. Saved the Overpass query to `data/osm_roads_query.overpass` so the exact API request is reproducible.
2. Downloaded highway ways from Overpass API with `curl -s -S -X POST -d @data/osm_roads_query.overpass https://overpass-api.de/api/interpreter -o data/osm_roads_raw.json`.
3. Converted the raw Overpass JSON into GeoJSON using `python3 scripts/osm_to_geojson.py data/osm_roads_raw.json data/osm_roads.geojson`.

## Outputs
- `data/osm_roads_raw.json` — raw Overpass response (131 MB)
- `data/osm_roads.geojson` — cleaned LineString features with id, tags, version, timestamp
- `scripts/osm_to_geojson.py` — conversion script for future reruns

## Notes / Next
- All future road analyses should reference `data/osm_roads.geojson`.
- Keep logging additional cleaning/filtering decisions as artifacts.
