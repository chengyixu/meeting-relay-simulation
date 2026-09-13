#!/usr/bin/env python3
"""Convert one local meeting note into confirmation-gated JSON actions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from simulation import transform_note


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("note", type=Path, help="UTF-8 local text file to parse")
    args = parser.parse_args()
    try:
        note = args.note.read_text(encoding="utf-8")
        result = transform_note(note)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
