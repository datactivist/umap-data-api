#!/usr/bin/env python3
"""
CLI tool for managing uMap Data API preprocessing
"""
import argparse
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.services.dataset_service import DatasetService
from app.processors.preprocessor import preprocessor
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def list_datasets():
    """List all available datasets"""
    print("=== PROCESSED DATASETS ===")
    processed_datasets = DatasetService.list_datasets()
    if processed_datasets:
        print(f"Found {len(processed_datasets)} processed datasets:")
        for dataset in processed_datasets:
            print(f"  - {dataset['name']}: {len(dataset['departements'])} départements")
            print(f"    Features: {dataset.get('feature_count', 'Unknown')}")
            print(f"    Processed: {dataset.get('processed_at', 'Unknown')}")
            print()
    else:
        print("No processed datasets found.")

    print("\n=== RAW DATASETS ===")
    raw_datasets = preprocessor.discover_raw_datasets()
    if raw_datasets:
        print(f"Found {len(raw_datasets)} raw datasets:")
        for name, info in raw_datasets.items():
            print(f"  - {name}: {info['format'].value} ({info['file_path']})")
    else:
        print("No raw datasets found in data/raw/")


def preprocess_dataset(dataset_name: str = None):
    """Preprocess a specific dataset or all datasets"""
    if dataset_name:
        # Find raw dataset
        raw_datasets = preprocessor.discover_raw_datasets()
        if dataset_name not in raw_datasets:
            print(f"Raw dataset '{dataset_name}' not found in data/raw/")
            return

        dataset_info = raw_datasets[dataset_name]
        print(f"Preprocessing dataset: {dataset_name}")

        try:
            result = DatasetService.preprocess_dataset(
                dataset_name, dataset_info["file_path"], dataset_info["format"].value
            )

            print(f"✅ Successfully preprocessed {dataset_name}")
            print(f"   Created files for {len(result['departements'])} départements")
            print(f"   Total features: {result['feature_count']}")
            print(f"   Output directory: {result['processed_dir']}")

        except Exception as e:
            print(f"❌ Error preprocessing {dataset_name}: {e}")
    else:
        print("Preprocessing all datasets...")
        result = DatasetService.preprocess_all_datasets()

        total = result["total_datasets"]
        successes = sum(1 for r in result["results"] if r["success"])
        failures = total - successes

        print(f"Processed {total} datasets: {successes} successes, {failures} failures")

        for res in result["results"]:
            if res["success"]:
                if "departements" in res:
                    print(
                        f"✅ {res['dataset_name']}: {len(res['departements'])} départements"
                    )
                else:
                    print(f"✅ {res['dataset_name']}: {res.get('message', 'Success')}")
            else:
                print(f"❌ {res['dataset_name']}: {res.get('error', 'Unknown error')}")


def cache_status():
    """Show cache status for all datasets"""
    raw_datasets = preprocessor.discover_raw_datasets()
    processed_datasets = preprocessor.list_processed_datasets()

    print("=== PREPROCESSING STATUS ===")
    print("-" * 80)
    print(
        f"{'Dataset Name':<20} | {'Status':<15} | {'Départements':<12} | {'Features':<10}"
    )
    print("-" * 80)

    # Check raw datasets
    for dataset_name, dataset_info in raw_datasets.items():
        needs_processing = preprocessor.needs_preprocessing(
            dataset_name, dataset_info["file_path"]
        )
        info = preprocessor.get_dataset_info(dataset_name)

        if needs_processing:
            status = "❌ Needs processing"
            departements = "0"
            features = "Unknown"
        else:
            status = "✅ Up to date"
            departements = str(len(info.get("departements", []))) if info else "0"
            features = str(info.get("feature_count", "Unknown")) if info else "Unknown"

        print(
            f"{dataset_name:<20} | {status:<15} | {departements:<12} | {features:<10}"
        )

        if info:
            print(f"{'':20} | Last processed: {info.get('processed_at', 'Unknown')}")
            print(f"{'':20} | Source: {dataset_info['format'].value}")

        print()


def cleanup_cache(dataset_name: str = None):
    """Clean up preprocessing cache"""
    if dataset_name:
        info = preprocessor.get_dataset_info(dataset_name)
        if not info:
            print(f"Dataset '{dataset_name}' not found.")
            return

        preprocessor.cleanup_cache(dataset_name)
        print(f"✅ Cleaned cache for {dataset_name}")
    else:
        processed_datasets = preprocessor.list_processed_datasets()
        if not processed_datasets:
            print("No processed datasets to clean.")
            return

        preprocessor.cleanup_cache()
        print(f"✅ Cleaned all cache files ({len(processed_datasets)} datasets)")


def setup_directories():
    """Set up data directories"""
    raw_dir = Path("./data/raw")
    processed_dir = Path("./data/processed")

    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    print("✅ Created data directories:")
    print(f"   Raw datasets: {raw_dir.absolute()}")
    print(f"   Processed datasets: {processed_dir.absolute()}")
    print()
    print(
        "📁 Place your raw dataset files (geopackage, shapefile, geojson, csv) in data/raw/"
    )
    print(
        "🔄 Run 'python manage.py preprocess' to process them into GeoJSON by département"
    )


def main():
    parser = argparse.ArgumentParser(description="uMap Data API Management Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Setup directories
    subparsers.add_parser("setup", help="Set up data directories")

    # List datasets
    subparsers.add_parser("list", help="List all available datasets")

    # Preprocess
    preprocess_parser = subparsers.add_parser("preprocess", help="Preprocess datasets")
    preprocess_parser.add_argument(
        "dataset_name",
        nargs="?",
        help="Dataset name to preprocess (all if not specified)",
    )

    # Cache status
    subparsers.add_parser("status", help="Show preprocessing status")

    # Cleanup
    cleanup_parser = subparsers.add_parser("cleanup", help="Clean up processed files")
    cleanup_parser.add_argument(
        "dataset_name", nargs="?", help="Dataset name to clean (all if not specified)"
    )

    args = parser.parse_args()

    if args.command == "setup":
        setup_directories()
    elif args.command == "list":
        list_datasets()
    elif args.command == "preprocess":
        preprocess_dataset(args.dataset_name)
    elif args.command == "status":
        cache_status()
    elif args.command == "cleanup":
        cleanup_cache(args.dataset_name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
