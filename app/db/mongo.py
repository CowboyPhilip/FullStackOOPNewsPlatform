from motor.core import AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.config import settings
from odmantic import AIOEngine


class MongoConnection:
    _instance = None
    mongo_client: AsyncIOMotorClient | None
    engine: AIOEngine
    
    def __new__(cls):
        if cls._instance is None:
            if settings.MONGO_URI is None:
                raise ValueError("MONGO_URI is not set in the settings.")
            if settings.DB_NAME is None:
                raise ValueError("DB_NAME is not set in the settings.")

            cls._instance = super().__new__(cls)
            cls._instance.mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
            cls._instance.engine = AIOEngine(
                client=cls._instance.mongo_client,
                database=settings.DB_NAME,
            )
        return cls._instance
    
    
    def get_db(self) -> AgnosticDatabase:
        """Return Motor raw Mongo database object."""
        if self.mongo_client is None:
            raise RuntimeError("Mongo client is not initialized.")
        if settings.DB_NAME is None:
            raise RuntimeError("Database name is not set in settings.")
        return self.mongo_client[settings.DB_NAME]
    
    def getEngine(self) -> AIOEngine:
        if self.engine is None:
            raise ValueError("mongoEngine is not initialized")
        return self.engine
    
    async def ping(self):
      await self.get_db().command("ping")

  
def getEngine() -> AIOEngine:
    return  MongoConnection().getEngine()

    __all__ = ["get_db",'ping']