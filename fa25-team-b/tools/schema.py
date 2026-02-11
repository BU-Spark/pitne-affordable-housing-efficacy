from __future__ import annotations
from pathlib import Path
import yaml


def standardize_columns(df, mapping_file: str | Path = "config/columns.yaml"):
    mapping = yaml.safe_load(Path(mapping_file).read_text())
    rename = {}
    lower_map = {c.lower(): c for c in df.columns}
    for canon, variants in mapping.items():
        for v in variants:
            key = v.lower()
            if key in lower_map:
                rename[lower_map[key]] = canon
                break
    return df.rename(columns=rename)