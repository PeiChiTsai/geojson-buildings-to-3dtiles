# Sample data

This folder contains small example files for testing the repository.

## `sample_buildings.geojson`

Sample building footprints in EPSG:3857.

Required attributes:

- `id`
- `height`
- `var`
- `source`
- `region`

Use this file with:

```bash
python src/buildings_to_3dtiles.py
```

## `sample_building_centroids.json`

The centroids of the sample buildings, converted to EPSG:4326.

This can be selected directly in:

```text
terrain/sample_cesium_world_terrain.html
```

for testing the terrain-sampling workflow.

## Terrain elevations

`terrain_elevations.json` is intentionally not included.

It is generated from Cesium World Terrain for the user's own dataset and requires the user's Cesium ion access token.
