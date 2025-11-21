"""Extraction utilities: read CSV files into lists of rows."""
from typing import List, Dict
import csv


def extract_csv(path: str) -> List[Dict[str, str]]:
    """Read a CSV and return a list of dicts (one per row).

    All values are returned as strings; transformation step can coerce types.
    """
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            rows.append(r)
    return rows
