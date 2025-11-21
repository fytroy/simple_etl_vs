"""Transformation utilities: simple cleaning and type coercion."""
from typing import List, Dict, Any


def transform_rows(rows: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Apply lightweight transformations: strip strings and coerce numeric-ish values."""
    out = []
    for r in rows:
        new = {}
        for k, v in r.items():
            if v is None:
                new[k] = None
                continue
            s = v.strip()
            # try int
            if s == "":
                new[k] = None
                continue
            try:
                iv = int(s)
                new[k] = iv
                continue
            except Exception:
                pass
            try:
                fv = float(s)
                new[k] = fv
                continue
            except Exception:
                pass
            new[k] = s
        out.append(new)
    return out
