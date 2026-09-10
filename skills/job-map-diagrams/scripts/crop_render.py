#!/usr/bin/env python3
"""Trim near-white renderer whitespace while preserving a safety margin."""

from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path

from PIL import Image, ImageChops


def content_bbox(image: Image.Image, threshold: int) -> tuple[int, int, int, int] | None:
    rgba = image.convert("RGBA")
    red, green, blue, alpha = rgba.split()

    def darker_than_threshold(channel: Image.Image) -> Image.Image:
        return channel.point(lambda value: 255 if value < threshold else 0)

    mask = ImageChops.lighter(
        darker_than_threshold(red),
        ImageChops.lighter(darker_than_threshold(green), darker_than_threshold(blue)),
    )
    mask = ImageChops.multiply(mask, alpha)
    return mask.getbbox()


def crop_image(source: Path, destination: Path, padding: int, threshold: int) -> None:
    with Image.open(source) as image:
        bbox = content_bbox(image, threshold)
        if bbox is None:
            raise ValueError("image contains no pixels darker than the background threshold")

        left = max(0, bbox[0] - padding)
        top = max(0, bbox[1] - padding)
        right = min(image.width, bbox[2] + padding)
        bottom = min(image.height, bbox[3] + padding)
        cropped = image.crop((left, top, right, bottom))

        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.resolve() == destination.resolve():
            handle, temporary_name = tempfile.mkstemp(
                prefix=f".{source.stem}-crop-",
                suffix=source.suffix,
                dir=source.parent,
            )
            os.close(handle)
            temporary_path = Path(temporary_name)
            try:
                cropped.save(temporary_path)
                temporary_path.replace(destination)
            finally:
                temporary_path.unlink(missing_ok=True)
        else:
            cropped.save(destination)

        print(
            f"cropped {image.width}x{image.height} to {cropped.width}x{cropped.height} "
            f"(offset {left},{top}; padding {padding}px)"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path, nargs="?")
    parser.add_argument("--padding", type=int, default=24)
    parser.add_argument("--threshold", type=int, default=250)
    args = parser.parse_args()
    if args.padding < 0:
        parser.error("--padding must be non-negative")
    if not 1 <= args.threshold <= 255:
        parser.error("--threshold must be between 1 and 255")
    crop_image(args.source, args.destination or args.source, args.padding, args.threshold)


if __name__ == "__main__":
    main()
