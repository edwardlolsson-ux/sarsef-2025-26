#!/usr/bin/env python3
"""Convert Overpass JSON response into a GeoJSON FeatureCollection."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def load_overpass_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as src:
        return json.load(src)


def way_to_feature(way: Dict[str, Any]) -> Dict[str, Any]:
    coords = way.get("geometry") or []
    if len(coords) < 2:
        return {}

    line = [[pt["lon"], pt["lat"]] for pt in coords]

    properties = {
        "id": way.get("id"),
        "tags": way.get("tags", {}),
        "version": way.get("version"),
        "timestamp": way.get("timestamp"),
    }

    return {
        "type": "Feature",
        "properties": properties,
        "geometry": {
            "type": "LineString",
            "coordinates": line,
        },
    }


def convert(raw: Path, out_path: Path) -> None:
    data = load_overpass_json(raw)
    elements: List[Dict[str, Any]] = data.get("elements", [])

    features = []
    for way in elements:
        if way.get("type") != "way":
            continue
        feature = way_to_feature(way)
        if feature:
            features.append(feature)

    feature_collection = {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {
            "note": "OSM highways downloaded via Overpass API",
            "source": data.get("generator"),
            "timestamp": data.get("osm3s", {}).get("timestamp_osm_base"),
        },
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as dst:
        json.dump(feature_collection, dst)


def main(argv: List[str]) -> int:
    if len(argv) != 3:
        print("Usage: python scripts/osm_to_geojson.py <raw_overpass.json> <output.geojson>")
        return 1

    raw = Path(argv[1])
    out_path = Path(argv[2])

    convert(raw, out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
