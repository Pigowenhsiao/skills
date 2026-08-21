#!/usr/bin/env python3
"""Build a low/base/high markdown table and multiplied totals for Fermi factors."""

from __future__ import annotations

import argparse
from functools import reduce
from operator import mul


def parse_factor(raw: str) -> tuple[str, float, float, float]:
    name, low, base, high = raw.split(":", 3)
    return name, float(low), float(base), float(high)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--factor",
        action="append",
        required=True,
        help="name:low:base:high",
    )
    args = parser.parse_args()

    factors = [parse_factor(item) for item in args.factor]
    low_total = reduce(mul, (f[1] for f in factors), 1.0)
    base_total = reduce(mul, (f[2] for f in factors), 1.0)
    high_total = reduce(mul, (f[3] for f in factors), 1.0)

    print("| Factor | Low | Base | High |")
    print("|---|---:|---:|---:|")
    for name, low, base, high in factors:
        print(f"| {name} | {low:g} | {base:g} | {high:g} |")
    print()
    print(f"Low total: {low_total:g}")
    print(f"Base total: {base_total:g}")
    print(f"High total: {high_total:g}")


if __name__ == "__main__":
    main()
