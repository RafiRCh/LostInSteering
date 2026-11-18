"""Convert a '# %%' percent-format script into a Kaggle-ready .ipynb. Usage: python tools/py2ipynb.py src.py out.ipynb"""
import json, re, sys
src, dst = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf8").read()
cells = []
for chunk in re.split(r"(?m)^# %%", text):
    if not chunk.strip():
        continue
    md = chunk.startswith(" [markdown]")
    body = chunk.split("\n", 1)[1] if "\n" in chunk else ""
    body = body.strip("\n")
    if md:
        body = "\n".join(l[2:] if l.startswith("# ") else l.lstrip("#") for l in body.split("\n"))
    lines = body.split("\n")
    cell = {"cell_type": "markdown" if md else "code", "metadata": {}, "source": [l + "\n" for l in lines[:-1]] + [lines[-1]]}
    if not md:
        cell.update(execution_count=None, outputs=[])
    cells.append(cell)
nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
      "language_info": {"name": "python"}, "kaggle": {"accelerator": "nvidiaTeslaT4", "isInternetEnabled": True}}, "nbformat": 4, "nbformat_minor": 5}
json.dump(nb, open(dst, "w", encoding="utf8"), indent=1, ensure_ascii=False)
print(f"{len(cells)} cells -> {dst}")
