#!/usr/bin/env python3
"""Draw a simple Tucson plan with roads and 100 diamondback points."""

from __future__ import annotations

import argparse
import os
from pathlib import Path


def _prepare_matplotlib_env() -> None:
    cache_dir = Path(".cache/matplotlib").resolve()
    cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(cache_dir))
    os.environ.setdefault("MPLBACKEND", "Agg")


_prepare_matplotlib_env()

import geopandas as gpd  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot 100 Crotalus atrox observations over a simple Tucson road plan."
    )
    parser.add_argument(
        "--roads",
        type=Path,
        default=Path("data/osm_roads.geojson"),
        help="Path to the roads dataset (default: data/osm_roads.geojson)",
    )
    parser.add_argument(
        "--observations",
        type=Path,
        default=Path("data/inaturalist_diamondback.geojson"),
        help="Path to the 100-point diamondback GeoJSON (default: data/inaturalist_diamondback.geojson)",
    )
    parser.add_argument(
        "--study-area",
        type=Path,
        default=Path("data/study_area.geojson"),
        help="Path to the study area polygon (default: data/study_area.geojson)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/plots/diamondback_plan.png"),
        help="Output PNG path (default: artifacts/plots/diamondback_plan.png)",
    )
    parser.add_argument(
        "--figsize",
        type=float,
        default=8.0,
        help="Figure width/height in inches (default: 8)",
    )
    parser.add_argument(
        "--point-size",
        type=float,
        default=18.0,
        help="Marker size for observations (default: 18)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    roads = gpd.read_file(args.roads)
    snakes = gpd.read_file(args.observations)
    study = gpd.read_file(args.study_area)

    args.output.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(args.figsize, args.figsize))
    study.boundary.plot(ax=ax, color="#1f2933", linewidth=1.5, label="Study area")
    roads.plot(ax=ax, color="#d3d3d3", linewidth=0.15, alpha=0.7, label="Roads")

    if snakes.empty:
        ax.text(
            0.5,
            0.5,
            "No diamondback observations",
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=12,
            color="red",
        )
    else:
        snakes.plot(
            ax=ax,
            color="#c2410c",
            markersize=args.point_size,
            marker="o",
            alpha=0.85,
            label="Diamondbacks (100 pts)",
        )

    ax.set_title("Crotalus atrox observations over Tucson road plan")
    ax.set_axis_off()
    ax.legend(loc="lower left")
    fig.tight_layout()
    fig.savefig(args.output, dpi=220)
    print(f"Saved map to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
