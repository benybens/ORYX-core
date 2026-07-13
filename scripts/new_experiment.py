"""Scaffold a new dated experiment record from experiments/template/.

Run with: python scripts/new_experiment.py "short experiment title"
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = REPO_ROOT / "experiments" / "template" / "RECORD.md"
RUNS_DIR = REPO_ROOT / "experiments" / "runs"


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "experiment"


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: python scripts/new_experiment.py "short experiment title"')
        raise SystemExit(1)

    title = " ".join(sys.argv[1:])
    today = date.today().isoformat()
    experiment_dir = RUNS_DIR / f"{today}-{slugify(title)}"
    experiment_dir.mkdir(parents=True, exist_ok=False)

    template_text = TEMPLATE_PATH.read_text()
    record_text = template_text.replace("<TITLE>", title).replace("<DATE>", today)
    (experiment_dir / "RECORD.md").write_text(record_text)

    print(f"Created {experiment_dir / 'RECORD.md'}")


if __name__ == "__main__":
    main()
