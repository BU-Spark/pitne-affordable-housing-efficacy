from __future__ import annotations
from pathlib import Path
import argparse


# Stubs for now; call the specific pipelines you want


def main(which: str | None):
    if which in (None, "applications"):
        from scripts import _run_apps as run_apps
        run_apps()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Run cleaning pipeline")
    ap.add_argument("--which", choices=["applications", "resales"], default=None)
    args = ap.parse_args()
    main(args.which)