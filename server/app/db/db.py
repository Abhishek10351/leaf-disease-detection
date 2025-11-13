from pymongo import AsyncMongoClient, ASCENDING, DESCENDING
from fastapi import FastAPI
from core.config import settings


async def connect(app: FastAPI) -> None:
    client = AsyncMongoClient(str(settings.MONGODB_URI))
    mongodb = client.get_database(settings.MONGODB_DB_NAME)
    app.mongo_client = client
    app.mongodb = mongodb

    await mongodb["users"].create_index([("email", ASCENDING)], unique=True)
    await mongodb["uploaded_images"].create_index([("user_id", ASCENDING)])
    await mongodb["uploaded_images"].create_index([("uploaded_at", DESCENDING)])
    await mongodb["analysis_history"].create_index([("user_id", ASCENDING)])
    await mongodb["analysis_history"].create_index([("timestamp", DESCENDING)])
    await mongodb["analysis_history"].create_index([("analysis_type", ASCENDING)])
    await mongodb["analysis_history"].create_index([("image_id", ASCENDING)])

    print(f"Database connected to {settings.MONGODB_DB_NAME}")


async def disconnect(app: FastAPI) -> None:
    await app.mongo_client.close()
    print("Database disconnected")
