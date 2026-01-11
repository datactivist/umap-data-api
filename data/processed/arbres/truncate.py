import json
from pathlib import Path

INPUT_NAME = "arbres_filtres_Paris.geojson"
REMOVE_KEYS = {"genre_francais", "genre_latin", "hauteur", "categorie_hauteur", "long", "lat", "code_dept", "code_insee", "code_iris"}


def main():
    base = Path(__file__).parent
    input_path = base / INPUT_NAME
    if not input_path.exists():
        raise FileNotFoundError(f"{input_path} not found")

    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    features = data.get("features", [])
    removed_counts = {k: 0 for k in REMOVE_KEYS}
    for feat in features:
        props = feat.get("properties", {})
        for k in list(REMOVE_KEYS):
            props.pop(k, None)
            removed_counts[k] += 1

    out_path = base / f"{input_path.stem}_v2{input_path.suffix}"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    total_removed = sum(removed_counts.values())
    print(f"Wrote {out_path} — removed {total_removed} keys: {removed_counts}")


if __name__ == "__main__":
    main()
