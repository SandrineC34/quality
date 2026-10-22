import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.actions.routers import non_conformites, suivi_actions
from app.indicators.routers import indicateurs
from app.audits.routers import audits

app = FastAPI(title="SMQ Qualité API")

# ---------------------------------------------------------------------
# Startup: ensure SWOT collection contains default data when empty
# ---------------------------------------------------------------------
@app.on_event("startup")
async def populate_swot_defaults():
    from app.database.connection import swot_collection, counters_collection
    from app.swot.default_data import default_swot
    # Verify collection is empty
    count = await swot_collection.count_documents({})
    if count == 0:
        # Insert default items (already contain refs)
        await swot_collection.insert_many(default_swot)
        # Initialise counter for future ids (max existing + 1)
        max_id = max(item["id"] for item in default_swot)
        await counters_collection.update_one(
            {"_id": "swot_id"},
            {"$set": {"seq": max_id}},
            upsert=True,
        )
    else:
        # Collection already has data – ensure every document has a "ref"
        TYPE_PREFIX = {"strength": "F", "weakness": "W", "opportunity": "O", "threat": "R"}
        # Group docs by type preserving order by id
        cursor = swot_collection.find().sort("id", 1)
        docs_by_type = {t: [] for t in TYPE_PREFIX}
        async for doc in cursor:
            docs_by_type.setdefault(doc.get("type"), []).append(doc)
        for type_key, docs in docs_by_type.items():
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


cors_origins = os.environ.get("CORS_ORIGINS", "*")
origins = ["*"] if cors_origins == "*" else cors_origins.split(",")

# allow_credentials=True est incompatible avec allow_origins=["*"] selon la spec CORS :
# certains navigateurs bloquent alors la requête sans même renvoyer d'erreur exploitable.
# Cette API n'utilise ni cookies ni auth, donc credentials n'est pas nécessaire.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(non_conformites.router, prefix="/api")
app.include_router(suivi_actions.router, prefix="/api")
app.include_router(indicateurs.router, prefix="/api")
app.include_router(audits.router, prefix="/api")
# Include SWOT TOWS export router
from app.swot.routers import router as swot_router
app.include_router(swot_router, prefix="")


@app.get("/api/health")
async def health():
    return {"status": "ok"}
