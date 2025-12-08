from fastapi import APIRouter
from pathlib import Path

router = APIRouter()

BASE = Path(__file__).resolve().parents[2] / "data" / "processed"


@router.get("/datasets")
def list_datasets():
    if not BASE.exists():
        return {"datasets": []}
    items = [p.name for p in BASE.iterdir() if p.is_dir()]
    return {"datasets": items}
