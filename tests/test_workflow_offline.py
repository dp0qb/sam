"""Offline demo and GeoTIFF export tests, without downloading SAM weights."""
from pathlib import Path
import json
import os
import tempfile
import numpy as np
import rasterio
from rasterio.transform import from_origin
import nbformat

os.environ["MPLBACKEND"] = "Agg"
nb_path = Path(__file__).resolve().parents[1] / "notebooks" / "geological_sam2_colab.ipynb"
nb = nbformat.read(nb_path, as_version=4)
code_cells = [cell.source for cell in nb.cells if cell.cell_type == "code"]
with tempfile.TemporaryDirectory() as tmp:
    scope = {"BASE": Path(tmp)}
    exec(compile(code_cells[1], "image_loader.py", "exec"), scope)
    assert scope["image_rgb"].shape == (650, 900, 3)
    h, w = scope["H"], scope["W"]
    mask = np.zeros((h, w), dtype=bool)
    mask[100:240, 200:380] = True
    scope.update(preview=scope["image_rgb"], MODE="point", mask_records=[{"mask": mask, "score": 0.92, "pixel_area": int(mask.sum())}])
    exec(compile(code_cells[3], "export.py", "exec"), scope)
    output = Path(tmp) / "sam2_geo_results"
    pixel_geojson = json.loads((output / "sam_polygons_pixel_coordinates.geojson").read_text(encoding="utf-8"))
    assert len(pixel_geojson["features"]) == 1
    assert pixel_geojson["metadata"]["coordinate_system"] == "pixel"
    assert (Path(tmp) / "sam_results.zip").is_file()

    tif = Path(tmp) / "sample.tif"
    data = np.full((3, 40, 80), 150, dtype="uint8")
    transform = from_origin(500000, 4800000, 10, 10)
    with rasterio.open(tif, "w", driver="GTiff", height=40, width=80, count=3, dtype="uint8", crs="EPSG:32651", transform=transform) as ds:
        ds.write(data)
    image, reduced_transform, crs, info = scope["load_input"](tif, max_edge=40, rgb_bands=(1,2,3))
    assert image.shape == (20, 40, 3)
    assert reduced_transform.a == 20 and abs(reduced_transform.e) == 20
    h, w = image.shape[:2]
    mask = np.zeros((h, w), dtype=bool)
    mask[5:15, 10:25] = True
    scope.update(image_rgb=image, geo_transform=reduced_transform, geo_crs=crs, input_info=info, H=h, W=w,
                 preview=image, mask_records=[{"mask": mask, "score": 0.95, "pixel_area": int(mask.sum())}])
    exec(compile(code_cells[3], "geo_export.py", "exec"), scope)
    geographic = json.loads((output / "sam_polygons_wgs84.geojson").read_text(encoding="utf-8"))
    assert len(geographic["features"]) == 1
    with rasterio.open(output / "sam_regions_georeferenced.tif") as ds:
        assert ds.crs == crs and ds.transform == reduced_transform
        assert ds.read(1).max() == 1
print("PASS: image polygon extraction and GeoTIFF georeferenced export")
