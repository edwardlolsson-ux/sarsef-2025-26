#!/usr/bin/env python3
"""Fetch iNaturalist observations and save as GeoJSON."""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List
from urllib.parse import urlencode
from urllib.request import Request, urlopen


INAT_API = "https://api.inaturalist.org/v1/observations"


@dataclass
class BBox:
    min_lon: float
    min_lat: float
    max_lon: float
    max_lat: float


def load_bbox(study_area: Path) -> BBox:
    data = json.loads(study_area.read_text())
    coords = data["features"][0]["geometry"]["coordinates"][0]
    lons = [pt[0] for pt in coords]
    lats = [pt[1] for pt in coords]
    return BBox(min(lons), min(lats), max(lons), max(lats))


def fetch_observations(
    bbox: BBox, taxon_id: int, per_page: int = 200, max_pages: int = 25
) -> Iterable[Dict]:
    for page in range(1, max_pages + 1):
        params = {
            "taxon_id": taxon_id,
            "quality_grade": "research",
            "verifiable": "true",
            "geo": "true",
            "nelat": bbox.max_lat,
            "nelng": bbox.max_lon,
            "swlat": bbox.min_lat,
            "swlng": bbox.min_lon,
            "per_page": per_page,
            "page": page,
            "order": "desc",
            "order_by": "observed_on",
        }
        query = urlencode(params)
        req = Request(f"{INAT_API}?{query}")
        with urlopen(req) as resp:
            payload = json.load(resp)
        results = payload.get("results", [])
        if not results:
            break
        yield from results
        total_results = payload.get("total_results")
        if total_results is not None:
            fetched = page * per_page
            if fetched >= total_results:
                break


def to_feature(obs: Dict) -> Dict:
    geojson = obs.get("geojson")
    if not geojson:
        return {}
    coords = geojson.get("coordinates")
    if not coords:
        return {}
    return {
        "type": "Feature",
        "properties": {
            "id": obs.get("id"),
            "species_guess": obs.get("species_guess"),
            "observed_on": obs.get("observed_on"),
            "quality_grade": obs.get("quality_grade"),
            "user_login": obs.get("user", {}).get("login"),
            "uri": obs.get("uri"),
            "taxon": {
                "id": obs.get("taxon", {}).get("id"),
                "name": obs.get("taxon", {}).get("name"),
                "preferred_common_name": obs.get("taxon", {}).get("preferred_common_name"),
            },
        },
        "geometry": {
            "type": geojson.get("type", "Point"),
            "coordinates": coords,
        },
    }


def save_geojson(features: List[Dict], out_path: Path, metadata: Dict) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as dst:
        json.dump(
            {
                "type": "FeatureCollection",
                "features": features,
                "metadata": metadata,
            },
            dst,
        )


def main(argv: List[str]) -> int:
    if len(argv) not in {4, 5}:
        print(
            "Usage: python scripts/fetch_inaturalist.py <study_area.geojson> <taxon_id> <output.geojson> [max_pages]"
        )
        return 1

    study_area = Path(argv[1])
    taxon_id = int(argv[2])
    out_path = Path(argv[3])
    max_pages = int(argv[4]) if len(argv) == 5 else 25

    bbox = load_bbox(study_area)
    observations = list(fetch_observations(bbox, taxon_id, max_pages=max_pages))
    features = []
    for obs in observations:
        feature = to_feature(obs)
        if feature:
            features.append(feature)

    metadata = {
        "total_features": len(features),
        "taxon_id": taxon_id,
        "source": INAT_API,
        "bounds": bbox.__dict__,
    }
    save_geojson(features, out_path, metadata)
    print(f"Saved {len(features)} observations to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
