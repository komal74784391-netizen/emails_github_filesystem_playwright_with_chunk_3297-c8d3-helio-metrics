"""Helio Metrics collector.

Reads raw sensor batches from the Helio deployment API and normalises them
into the metrics schema consumed by the reporting pipeline.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class Sample:
    ts: int
    name: str
    value: float
    labels: dict


def load_batch(path: Path) -> Iterable[Sample]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            yield Sample(
                ts=int(row["timestamp"]),
                name=str(row["metric"]),
                value=float(row["value"]),
                labels=dict(row.get("labels", {})),
            )


def summarise(samples: Iterable[Sample]) -> dict:
    totals = {}
    for sample in samples:
        totals.setdefault(sample.name, []).append(sample.value)
    return {name: sum(values) / len(values) for name, values in totals.items()}
