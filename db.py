from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

class DatabaseConnection:
    client: AsyncIOMotorClient = None
    db = None

    @classmethod
    async def connect_mongodb(cls, uri: str = "mongodb+srv://mohdjamikhann:<password>@cluster0.08tpi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", database_name: str = "student_management"):
        cls.client = AsyncIOMotorClient(uri)
        cls.db = cls.client[database_name]
        return cls.db

    @classmethod
    async def close_mongodb(cls):
        if cls.client:
            cls.client.close()

def get_sync_mongo_client(uri: str = "mongodb+srv://mohdjamikhann:<password>@cluster0.08tpi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"):
    return MongoClient(uri)
