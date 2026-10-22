import os
from pymongo import MongoClient

# Same defaults as the backend
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "smq_local")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
swot_collection = db["swot"]

TYPE_PREFIX = {"strength": "F", "weakness": "W", "opportunity": "O", "threat": "R"}

def main():
    cursor = swot_collection.find().sort("id", 1)
    items_by_type = {t: [] for t in TYPE_PREFIX}
    for doc in cursor:
        items_by_type.setdefault(doc.get("type"), []).append(doc)
    for type_key, docs in items_by_type.items():
        # Determine current max number from existing refs
        max_num = 0
        for d in docs:
            ref = d.get("ref")
            if ref and ref.startswith(TYPE_PREFIX.get(type_key, "")):
                try:
                    num = int(ref[len(TYPE_PREFIX[type_key]):])
                    if num > max_num:
                        max_num = num
                except ValueError:
                    pass
        # Assign missing refs sequentially
        next_num = max_num + 1
        for d in docs:
            if "ref" not in d:
                new_ref = f"{TYPE_PREFIX[type_key]}{next_num}"
                swot_collection.update_one({"_id": d["_id"]}, {"$set": {"ref": new_ref}})
                next_num += 1

if __name__ == "__main__":
    main()

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from app.database.connection import swot_collection

TYPE_PREFIX = {"strength": "F", "weakness": "W", "opportunity": "O", "threat": "R"}

async def main():
    # Load all items grouped by type, sorted by id to keep order stable
    cursor = swot_collection.find().sort("id", 1)
    items_by_type = {t: [] for t in TYPE_PREFIX}
    async for doc in cursor:
        items_by_type.setdefault(doc.get("type"), []).append(doc)

    for type_key, docs in items_by_type.items():
        # Determine current max number from existing refs
        max_num = 0
        for d in docs:
            ref = d.get("ref")
            if ref and ref.startswith(TYPE_PREFIX.get(type_key, "")):
                try:
                    num = int(ref[len(TYPE_PREFIX[type_key]):])
                    if num > max_num:
                        max_num = num
                except ValueError:
                    pass
        # Assign missing refs sequentially
        next_num = max_num + 1
        for d in docs:
            if "ref" not in d:
                new_ref = f"{TYPE_PREFIX[type_key]}{next_num}"
                await swot_collection.update_one({"_id": d["_id"]}, {"$set": {"ref": new_ref}})
                next_num += 1

if __name__ == "__main__":
    asyncio.run(main())
