#!/usr/bin/env python3
"""Plot iNaturalist observations on top of the study area's road network."""

from __future__ import annotations

import argparse
import os
from pathlib import Path


def _prepare_mpl_cache() -> None:
    if "MPLCONFIGDIR" in os.environ:
        cache_dir = Path(os.environ["MPLCONFIGDIR"]).expanduser()
    else:
        cache_dir = Path(".cache/matplotlib").resolve()
        os.environ["MPLCONFIGDIR"] = str(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLBACKEND", "Agg")


_prepare_mpl_cache()

import geopandas as gpd
import matplotlib.pyplot as plt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Layer iNaturalist points over OSM roads and save a PNG preview."
    )
    parser.add_argument(
        "roads",
        type=Path,
        help="Path to the roads GeoJSON (e.g., data/osm_roads.geojson)",
    )
    parser.add_argument(
        "observations",
        type=Path,
        help="Path to the iNaturalist GeoJSON export",
    )
    parser.add_argument(
        "output",
        type=Path,
        help="Where to save the rendered PNG (folders will be created)",
    )
    parser.add_argument(
        "--size",
        type=float,
        default=8.0,
        help="Figure size in inches (default: 8)",
    )
    parser.add_argument(
        "--point-size",
        type=float,
        default=12.0,
        help="Marker size for observations (default: 12)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    roads_gdf = gpd.read_file(args.roads)
    inat_gdf = gpd.read_file(args.observations)

    args.output.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(args.size, args.size))
    roads_gdf.plot(ax=ax, color="#b4b4b4", linewidth=0.2, alpha=0.8, label="Roads")

    if inat_gdf.empty:
        ax.text(
            0.5,
            0.5,
            "No iNaturalist observations",
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=12,
            color="red",
        )
    else:
        inat_gdf.plot(
            ax=ax,
            color="#fb8c00",
            markersize=args.point_size,
            marker="o",
            alpha=0.9,
            label="Observations",
        )

    ax.set_title("iNaturalist observations over OSM roads")
    ax.set_axis_off()
    ax.legend(loc="lower left")
    fig.tight_layout()
    fig.savefig(args.output, dpi=200)
    print(f"Saved map to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
