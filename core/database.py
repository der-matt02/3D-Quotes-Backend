from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from core.config import settings
from models.user_model import User
# from models.quote_model import Quote

async def initiate_database():
    client = AsyncIOMotorClient(settings.mongo_uri)
    database = client[settings.mongo_db]
    await init_beanie(database, document_models=[User])
    #await init_beanie(database, document_models=[User, Quote])
