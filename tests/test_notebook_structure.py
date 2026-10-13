"""Verify the notebook format and Python syntax without fetching model weights."""
from pathlib import Path
import ast
import nbformat

path = Path(__file__).resolve().parents[1] / "notebooks" / "geological_sam2_colab.ipynb"
nb = nbformat.read(path, as_version=4)
nbformat.validate(nb)
codes = [cell.source for cell in nb.cells if cell.cell_type == "code"]
assert len(codes) == 4
for index, source in enumerate(codes, 1):
    ast.parse(source, filename=f"cell_{index}.py")
print(f"PASS: valid notebook and {len(codes)} syntactically correct code cells")
