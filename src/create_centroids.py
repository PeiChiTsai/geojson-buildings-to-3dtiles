import argparse
import json
from pathlib import Path

import geopandas as gpd


PROJECT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = PROJECT_DIR / "data"

parser = argparse.ArgumentParser(
    description=(
        "Create a centroid JSON file for "
        "sample_cesium_world_terrain.html."
    )
)

parser.add_argument(
    "--input",
    type=Path,
    default=DEFAULT_DATA_DIR / "sample_buildings.geojson",
    help="Input building footprint GeoJSON."
)

parser.add_argument(
    "--output",
    type=Path,
    default=DEFAULT_DATA_DIR / "building_centroids.json",
    help="Output centroid JSON."
)

args = parser.parse_args()

if not args.input.exists():
    raise SystemExit(f"Missing input GeoJSON: {args.input}")

gdf = gpd.read_file(args.input)

if gdf.crs is None:
    raise SystemExit(
        "The input GeoJSON has no CRS information."
    )

if gdf.crs.to_epsg() != 3857:
    raise SystemExit(
        f"Input CRS is {gdf.crs}, but this workflow expects EPSG:3857."
    )

if "id" not in gdf.columns:
    raise SystemExit(
        "The input GeoJSON must contain an 'id' field."
    )

gdf = gdf[
    gdf.geometry.notna() & ~gdf.geometry.is_empty
].copy()

centroids_gdf = gdf.geometry.centroid
lon_lat = gpd.GeoSeries(
    centroids_gdf,
    crs=gdf.crs
).to_crs("EPSG:4326")

points = []

for feature_id, point in zip(
    gdf["id"].astype(str),
    lon_lat
):
    points.append(
        {
            "id": feature_id,
            "lon": float(point.x),
            "lat": float(point.y)
        }
    )

payload = {
    "source": "building footprint centroids",
    "crs": "EPSG:4326",
    "count": len(points),
    "points": points
}

args.output.parent.mkdir(
    parents=True,
    exist_ok=True
)

args.output.write_text(
    json.dumps(
        payload,
        indent=2
    ),
    encoding="utf-8"
)

print(
    f"Created {len(points):,} centroid points: "
    f"{args.output}"
)
