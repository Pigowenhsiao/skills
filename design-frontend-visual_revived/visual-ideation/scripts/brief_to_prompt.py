#!/usr/bin/env python3
"""Convert structured visual inputs into a compact image prompt scaffold."""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", required=True)
    parser.add_argument("--use", required=True)
    parser.add_argument("--style", required=True)
    parser.add_argument("--lighting", default="")
    parser.add_argument("--composition", default="")
    parser.add_argument("--ratio", default="16:9")
    parser.add_argument("--avoid-text", action="store_true")
    parser.add_argument("--negative", default="")
    args = parser.parse_args()

    parts = [
        args.subject,
        f"for {args.use}",
        args.style,
        args.lighting,
        args.composition,
        f"aspect ratio {args.ratio}",
    ]
    if args.avoid_text:
        parts.append("no text, no letters, no watermark")
    if args.negative:
        parts.append(f"avoid {args.negative}")

    prompt = ", ".join(part for part in parts if part)
    print(prompt)


if __name__ == "__main__":
    main()
