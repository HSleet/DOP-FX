#!/usr/bin/env python3
"""
DOP-FX: Foreign Exchange Rate Tracking for Dominican Peso

Main entry point for the application.
"""

import argparse
import sys
from pathlib import Path

# Add source to path
sys.path.insert(0, str(Path(__file__).parent / "source"))

from config import config


def main():
    parser = argparse.ArgumentParser(description="DOP-FX: FX Rate Tracking")
    parser.add_argument(
        "--mode",
        choices=["ingest", "normalize", "store", "full"],
        default="full",
        help="Operation mode (default: full pipeline)"
    )
    parser.add_argument(
        "--source",
        default="central_bank",
        help="Data source to process (default: central_bank)"
    )
    parser.add_argument(
        "--date",
        help="Specific date to process (YYYY-MM-DD)"
    )

    args = parser.parse_args()

    print(f"DOP-FX starting in {args.mode} mode...")
    print(f"Database: {config.database_path}")
    print(f"Source: {args.source}")

    # TODO: Implement pipeline execution
    if args.mode == "full":
        print("Running full pipeline...")
        # run_ingestion(args.source)
        # run_normalization(args.source)
        # run_storage()
    elif args.mode == "ingest":
        print(f"Running ingestion for {args.source}...")
        # run_ingestion(args.source)
    # etc.

    print("Pipeline completed successfully!")


if __name__ == "__main__":
    main()