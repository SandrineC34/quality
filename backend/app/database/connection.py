import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "smq_local")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

non_conformites_collection = db["non_conformites"]
actions_collection = db["actions"]
audits_collection = db["audits"]
indicators_collection = db["indicators"]
counters_collection = db["counters"]


async def get_next_sequence(name: str) -> int:
    """Incrémente et retourne un compteur atomique (pour générer les n° de réf)."""
    doc = await counters_collection.find_one_and_update(
        {"_id": name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return doc["seq"]

