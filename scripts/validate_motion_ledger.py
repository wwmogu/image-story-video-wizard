#!/usr/bin/env python3
"""Validate candidate motion-ledger rows without requiring media dependencies."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


REQUIRED_COLUMNS = (
    "experiment_id",
    "output_version",
    "status",
    "base_kind",
    "base_artifact",
    "output_artifact",
    "width",
    "height",
    "internal_scale",
    "fps",
    "frame_count",
    "cover_duration_seconds",
    "total_duration_seconds",
    "motion_profile",
    "transition_profile",
    "transition_frozen",
    "filters",
    "audio_artifact",
    "tts_metadata_artifact",
    "timing_events_artifact",
    "subtitle_timing_source",
    "validation_commands",
    "validation_result",
    "human_verdict",
)
FORBIDDEN_FILTERS = ("zoompan", "pan", "blur", "breathe", "breathing", "shake")
STALE_STATUSES = {"stale", "needs rework", "需要返工"}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                return ["ledger has no header"]
            missing = [column for column in REQUIRED_COLUMNS if column not in reader.fieldnames]
            if missing:
                return [f"missing required columns: {', '.join(missing)}"]
            rows = list(reader)
    except FileNotFoundError:
        return [f"ledger does not exist: {path}"]
    except (OSError, csv.Error) as exc:
        return [f"cannot read ledger: {exc}"]

    if not rows:
        return ["ledger has no experiment rows"]

    for line_number, row in enumerate(rows, start=2):
        status = (row.get("status") or "").strip()
        if not status:
            errors.append(f"line {line_number}: status is required")
        if status.lower() in STALE_STATUSES or status in STALE_STATUSES:
            continue

        for column in (
            "experiment_id",
            "output_version",
            "base_artifact",
            "output_artifact",
            "audio_artifact",
            "tts_metadata_artifact",
            "timing_events_artifact",
            "subtitle_timing_source",
            "validation_commands",
            "human_verdict",
        ):
            if not (row.get(column) or "").strip():
                errors.append(f"line {line_number}: {column} is required")
        if (row.get("base_kind") or "").strip().lower() not in {"clean", "clean-base", "clean base"}:
            errors.append(f"line {line_number}: base_kind must identify a clean base")
        for column in ("width", "height", "frame_count"):
            try:
                if int(row[column]) <= 0:
                    raise ValueError
            except (KeyError, TypeError, ValueError):
                errors.append(f"line {line_number}: {column} must be a positive integer")
        try:
            if float(row["fps"]) <= 0:
                raise ValueError
        except (KeyError, TypeError, ValueError):
            errors.append(f"line {line_number}: fps must be positive")
        for column in ("internal_scale", "cover_duration_seconds", "total_duration_seconds"):
            try:
                if float(row[column]) <= 0:
                    raise ValueError
            except (KeyError, TypeError, ValueError):
                errors.append(f"line {line_number}: {column} must be positive")
        if (row.get("transition_profile") or "").strip().lower() in {"dissolve", "cross-dissolve", "gradient", "pure gradient"}:
            if (row.get("transition_frozen") or "").strip().lower() not in {"true", "yes", "1"}:
                errors.append(f"line {line_number}: pure dissolve requires transition_frozen=true")
        filters = (row.get("filters") or "").lower()
        for forbidden in FORBIDDEN_FILTERS:
            if forbidden in filters:
                errors.append(f"line {line_number}: prohibited filter recorded in candidate: {forbidden}")
        if (row.get("validation_result") or "").strip().lower() not in {"pass", "passed", "valid", "通过"}:
            errors.append(f"line {line_number}: validation_result must be a passing result")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    args = parser.parse_args()
    errors = validate(args.ledger)
    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
