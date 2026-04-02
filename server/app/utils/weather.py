"""Weather and location helpers for climate-aware agricultural guidance."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Optional

import openmeteo_requests
import requests_cache
from retry_requests import retry

logger = logging.getLogger(__name__)

OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
ASSAM_FALLBACK_LOCATION = {
    "name": "Guwahati",
    "region": "Assam",
    "country": "India",
    "latitude": 26.1445,
    "longitude": 91.7362,
}

HOURLY_VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "precipitation_probability",
    "weather_code",
]


@dataclass(slots=True)
class LocationClimateContext:
    location_name: str
    region: str
    country: str
    avg_humidity: float
    total_precipitation: float
    max_precipitation_probability: float
    temperature_min: float
    temperature_max: float
    weather_summary: str


@lru_cache(maxsize=1)
def _get_openmeteo_client() -> openmeteo_requests.Client:
    """Create a cached Open-Meteo client with retries."""
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=3, backoff_factor=0.2)
    return openmeteo_requests.Client(session=retry_session)


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def _to_float_list(source: Any) -> list[float]:
    return list(source) if source is not None else []


def _describe_risk(
    avg_humidity: float,
    total_precipitation: float,
    max_precipitation_probability: float,
    temperature_min: float,
    temperature_max: float,
) -> str:
    rainy_or_humid = avg_humidity >= 80 or total_precipitation >= 6 or max_precipitation_probability >= 60
    warm = temperature_max >= 22
    cool = temperature_min <= 16

    if rainy_or_humid and warm:
        return (
            "High fungal pressure expected. Prioritize fungal diseases such as powdery mildew, leaf spot, downy mildew, rust, and blights. "
            "Delay contact sprays before rain and favor systemic or rain-safe treatments when timing matters."
        )

    if rainy_or_humid:
        return (
            "Moderate fungal pressure expected. Watch for leaf spots, mildew, and soft rots, especially on dense canopies and water-sensitive crops."
        )

    if warm and not cool:
        return (
            "Warm conditions may increase stress-related issues and some insect pressure; keep an eye on drought stress, mites, and secondary infections."
        )

    return (
        "Mixed climate conditions suggest a balanced differential; local disease risk should be interpreted alongside crop type and canopy moisture."
    )


def _fetch_forecast(latitude: float, longitude: float) -> dict[str, Any]:
    client = _get_openmeteo_client()
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": HOURLY_VARIABLES,
        "forecast_days": 2,
        "timezone": "auto",
    }
    responses = client.weather_api(OPEN_METEO_FORECAST_URL, params=params)
    if not responses:
        raise RuntimeError("Open-Meteo returned no forecast data")

    response = responses[0]
    hourly = response.Hourly()

    return {
        "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
        "relative_humidity_2m": hourly.Variables(1).ValuesAsNumpy(),
        "precipitation": hourly.Variables(2).ValuesAsNumpy(),
        "precipitation_probability": hourly.Variables(3).ValuesAsNumpy(),
        "weather_code": hourly.Variables(4).ValuesAsNumpy(),
    }


def _build_weather_summary() -> LocationClimateContext:
    latitude = ASSAM_FALLBACK_LOCATION["latitude"]
    longitude = ASSAM_FALLBACK_LOCATION["longitude"]
    location_name = ASSAM_FALLBACK_LOCATION["name"]
    region = ASSAM_FALLBACK_LOCATION["region"]
    country = ASSAM_FALLBACK_LOCATION["country"]
    forecast_data = _fetch_forecast(latitude, longitude)

    humidity_values = _to_float_list(forecast_data.get("relative_humidity_2m"))
    precipitation_values = _to_float_list(forecast_data.get("precipitation"))
    precipitation_probability_values = _to_float_list(forecast_data.get("precipitation_probability"))
    temperature_values = _to_float_list(forecast_data.get("temperature_2m"))

    humidity_window = humidity_values[:48]
    precipitation_window = precipitation_values[:48]
    precipitation_probability_window = precipitation_probability_values[:48]
    temperature_window = temperature_values[:48]

    avg_humidity = sum(_safe_float(item) for item in humidity_window) / len(humidity_window) if humidity_window else 0.0
    total_precipitation = sum(_safe_float(item) for item in precipitation_window) if precipitation_window else 0.0
    max_precipitation_probability = max((_safe_float(item) for item in precipitation_probability_window), default=0.0)
    temperature_min = min((_safe_float(item) for item in temperature_window), default=0.0)
    temperature_max = max((_safe_float(item) for item in temperature_window), default=0.0)

    risk_summary = _describe_risk(
        avg_humidity=avg_humidity,
        total_precipitation=total_precipitation,
        max_precipitation_probability=max_precipitation_probability,
        temperature_min=temperature_min,
        temperature_max=temperature_max,
    )

    climate_summary = (
        f"Location: {location_name}{', ' + region if region else ''}{', ' + country if country else ''}. "
        f"Next-48-hour climate snapshot: average humidity about {avg_humidity:.0f}%, total precipitation about {total_precipitation:.1f} mm, "
        f"peak rain probability about {max_precipitation_probability:.0f}%, temperature range {temperature_min:.0f}°C to {temperature_max:.0f}°C. "
        f"{risk_summary} "
        "Use local extension-style guidance and bias differential diagnosis toward weather-linked fungal diseases when humidity or rainfall is high. "
        "In humid subtropical or tropical conditions, common crop contexts often include rice, tea, banana, citrus, tomato, and leafy vegetables."
    )

    return LocationClimateContext(
        location_name=location_name,
        region=region,
        country=country,
        avg_humidity=avg_humidity,
        total_precipitation=total_precipitation,
        max_precipitation_probability=max_precipitation_probability,
        temperature_min=temperature_min,
        temperature_max=temperature_max,
        weather_summary=climate_summary,
    )


def build_location_weather_context() -> Optional[LocationClimateContext]:
    """Fetch weather and coarse location context for the default Assam location."""
    try:
        return _build_weather_summary()
    except Exception as exc:
        logger.warning("Failed to resolve weather context: %s", exc)
        return None
