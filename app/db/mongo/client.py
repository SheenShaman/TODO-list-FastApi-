from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "fast_api_project"

client = AsyncIOMotorClient(MONGO_URL)
mongo_db = client[DB_NAME]
