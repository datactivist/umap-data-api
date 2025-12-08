from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pathlib import Path
import json

router = APIRouter()

BASE = Path(__file__).resolve().parents[2] / "data" / "processed"


def list_files(dataset: str) -> List[Path]:
    d = BASE / dataset
    if not d.exists() or not d.is_dir():
        return []
    return [p for p in d.iterdir() if p.suffix.lower() == ".geojson"]


@router.get("/datasets/{dataset_name}/filters")
def dataset_filters(dataset_name: str):
    """List available filters for a dataset by inspecting filenames in data/processed/{dataset_name}"""
    files = list_files(dataset_name)
    print(dataset_name)
    if not files:
        raise HTTPException(status_code=404, detail="Dataset not found")
    filters = set()
    prefix = f"{dataset_name.lower()}_filtres_"
    print(prefix)
    for p in files:
        name = p.stem  # without suffix
        lname = name.lower()
        if lname.startswith(prefix):
            rest = name.split("_filtres_", 1)[1]
            filters.add(rest)

    return {"dataset": dataset_name, "filters": sorted(list(filters))}


@router.get("/datasets/{dataset_name}")
def get_dataset(dataset_name: str, commune: Optional[str] = Query(None), departement: Optional[str] = Query(None)):
    """Retrieve GeoJSON features for a dataset filtered by commune or departement.

    Exactly one of `commune` or `departement` should be provided.
    The router will look for files in data/processed/{dataset_name} and return the merged GeoJSON.
    """
    if not (bool(commune) ^ bool(departement)):
        raise HTTPException(status_code=400, detail="Provide exactly one of 'commune' or 'departement'")

    files = list_files(dataset_name)
    print(files)
    if not files:
        raise HTTPException(status_code=404, detail="Dataset not found")

    value = commune if commune else departement
    value_lower = value.lower()

    matched = []
    prefix = f"{dataset_name.lower()}_filtres_"
    for p in files:
        name = p.stem
        lname = name.lower()
        if lname.startswith(prefix):
            rest = name.split("_filtres_", 1)[1]
            # match if the provided value appears in the filter segment
            if value_lower == rest.lower() or value_lower in rest.lower():
                matched.append(p)

    if not matched:
        raise HTTPException(status_code=404, detail="No matching files for provided parameter")

    # merge features
    features = []
    for p in matched:
        try:
            with p.open("r", encoding="utf-8") as fh:
                doc = json.load(fh)
                if doc.get("type") == "FeatureCollection":
                    features.extend(doc.get("features", []))
        except Exception:
            continue

    return {"type": "FeatureCollection", "features": features}
