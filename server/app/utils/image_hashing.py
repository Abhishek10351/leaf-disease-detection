"""Perceptual image hashing helpers for similarity-based cache reuse."""

from __future__ import annotations

from io import BytesIO
from typing import Optional

import imagehash
from PIL import Image


def compute_phash_hex(image_bytes: bytes) -> str:
    """Compute 64-bit perceptual hash as hex string for an image payload."""
    with Image.open(BytesIO(image_bytes)) as image:
        # Normalize mode for stable hash generation across source formats.
        normalized = image.convert("RGB")
        return str(imagehash.phash(normalized, hash_size=8))


def phash_hamming_distance(hash_a: str, hash_b: str) -> Optional[int]:
    """Return Hamming distance between two pHash hex values."""
    if not hash_a or not hash_b:
        return None
    try:
        # imagehash subtraction can return numpy scalar types; normalize to builtin int.
        return int(imagehash.hex_to_hash(hash_a) - imagehash.hex_to_hash(hash_b))
    except Exception:
        return None
