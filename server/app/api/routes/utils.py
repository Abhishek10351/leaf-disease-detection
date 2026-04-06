from fastapi import APIRouter, Request, Response, Query
import time
import uuid
from datetime import datetime, timezone

from app.utils.weather import (
    build_location_weather_context,
    build_location_weather_context_for_coordinates,
)

router = APIRouter(tags=["utils"])


@router.get("/ping")
async def ping(req: Request):
    data = {"test_field": "test_data", "_id": str(uuid.uuid4())}
    start_time = time.time()
    collection = req.app.mongodb
    new_document = await collection["test"].insert_one(data)
    end_time = time.time()
    duration = (end_time - start_time) * 1000
    await collection["test"].delete_one({"_id": new_document.inserted_id})
    return {
        "status": "healthy", 
        "message": f"Mongo ping: {duration:.2f} milliseconds",
        "database": "connected",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.get("/weather/forecast-test")
async def weather_forecast_test(
    latitude: float | None = Query(default=None, ge=-90, le=90),
    longitude: float | None = Query(default=None, ge=-180, le=180),
):
    """Return a weather snapshot for provided coordinates (or fallback when missing)."""
    context = (
        build_location_weather_context_for_coordinates(latitude, longitude)
        if latitude is not None and longitude is not None
        else build_location_weather_context()
    )
    if context is None:
        return {
            "status": "unhealthy",
            "forecast_ready": False,
            "location": "Assam fallback",
            "error": "Failed to resolve forecast data",
        }

    return {
        "status": "healthy",
        "forecast_ready": True,
        "location": {
            "name": context.location_name,
            "region": context.region,
            "country": context.country,
        },
        "forecast": {
            "avg_humidity": context.avg_humidity,
            "total_precipitation": context.total_precipitation,
            "max_precipitation_probability": context.max_precipitation_probability,
            "temperature_min": context.temperature_min,
            "temperature_max": context.temperature_max,
        },
        "summary": context.weather_summary,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
