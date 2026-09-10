#!/usr/bin/env python3
"""Validate a structured JTBD job map and emit Eraser Diagrams JSON."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from job_map import build_diagram, validate_spec


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: build_job_map.py INPUT_SPEC.json OUTPUT_DIAGRAM.json", file=sys.stderr)
        return 2

    input_path = Path(argv[1])
    output_path = Path(argv[2])
    try:
        spec = validate_spec(json.loads(input_path.read_text(encoding="utf-8")))
        diagram = build_diagram(spec)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(diagram, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
