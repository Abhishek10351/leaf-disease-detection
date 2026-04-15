"""OpenCV preprocessing pipeline for noisy mobile leaf images."""

from __future__ import annotations

from typing import Any

import cv2
import numpy as np


MAX_EDGE = 1400


def _decode_image(image_bytes: bytes) -> np.ndarray:
    array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Unable to decode image bytes")
    return image


def _encode_jpeg(image: np.ndarray, quality: int = 92) -> bytes:
    ok, encoded = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    if not ok:
        raise ValueError("Unable to encode image as JPEG")
    return encoded.tobytes()


def _resize_if_needed(image: np.ndarray) -> tuple[np.ndarray, bool]:
    height, width = image.shape[:2]
    longest_edge = max(height, width)
    if longest_edge <= MAX_EDGE:
        return image, False

    scale = MAX_EDGE / float(longest_edge)
    resized = cv2.resize(
        image,
        (int(width * scale), int(height * scale)),
        interpolation=cv2.INTER_AREA,
    )
    return resized, True


def _apply_clahe(image_bgr: np.ndarray) -> np.ndarray:
    lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    l_enhanced = clahe.apply(l_channel)

    merged = cv2.merge((l_enhanced, a_channel, b_channel))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)


def _leaf_mask(image_bgr: np.ndarray) -> tuple[np.ndarray, float, bool]:
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    # Green healthy leaf ranges.
    mask_green = cv2.inRange(hsv, np.array([25, 35, 25]), np.array([95, 255, 255]))
    # Brown/yellow diseased patches ranges.
    mask_brown = cv2.inRange(hsv, np.array([5, 35, 20]), np.array([30, 255, 235]))

    combined = cv2.bitwise_or(mask_green, mask_brown)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    cleaned = cv2.morphologyEx(combined, cv2.MORPH_OPEN, kernel, iterations=1)
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel, iterations=2)

    full_pixels = cleaned.shape[0] * cleaned.shape[1]
    mask_ratio = float(cv2.countNonZero(cleaned)) / float(full_pixels) if full_pixels else 0.0

    # If the color mask is too weak, use full frame as fallback.
    if mask_ratio < 0.01:
        return np.full_like(cleaned, 255), mask_ratio, False

    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return cleaned, mask_ratio, False

    largest = max(contours, key=cv2.contourArea)
    contour_mask = np.zeros_like(cleaned)
    cv2.drawContours(contour_mask, [largest], -1, 255, thickness=cv2.FILLED)

    contour_ratio = float(cv2.countNonZero(contour_mask)) / float(full_pixels) if full_pixels else 0.0
    if contour_ratio < 0.01:
        return cleaned, mask_ratio, False

    return contour_mask, contour_ratio, True


def _build_compare_strip(original: np.ndarray, processed: np.ndarray) -> np.ndarray:
    target_height = min(480, max(original.shape[0], processed.shape[0]))

    def _fit_height(img: np.ndarray, h: int) -> np.ndarray:
        scale = h / float(img.shape[0])
        return cv2.resize(img, (int(img.shape[1] * scale), h), interpolation=cv2.INTER_AREA)

    left = _fit_height(original, target_height)
    right = _fit_height(processed, target_height)

    strip = np.hstack([left, right])

    cv2.putText(strip, "Original", (14, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(strip, "Preprocessed", (left.shape[1] + 14, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2, cv2.LINE_AA)
    return strip


def preprocess_leaf_image_bytes(image_bytes: bytes) -> tuple[bytes, bytes, dict[str, Any]]:
    """Apply CLAHE + HSV masking + Gaussian blur and return processed + comparison images."""
    original = _decode_image(image_bytes)
    resized, resized_flag = _resize_if_needed(original)

    clahe_img = _apply_clahe(resized)
    mask, mask_ratio, used_largest_contour = _leaf_mask(clahe_img)

    isolated = cv2.bitwise_and(clahe_img, clahe_img, mask=mask)
    processed = cv2.GaussianBlur(isolated, (5, 5), 0)

    compare_strip = _build_compare_strip(resized, processed)

    processed_bytes = _encode_jpeg(processed)
    compare_bytes = _encode_jpeg(compare_strip, quality=90)

    meta: dict[str, Any] = {
        "resized": bool(resized_flag),
        "mask_ratio": float(mask_ratio),
        "used_largest_contour": bool(used_largest_contour),
        "shape": {
            "height": int(processed.shape[0]),
            "width": int(processed.shape[1]),
        },
    }

    return processed_bytes, compare_bytes, meta
