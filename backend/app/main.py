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
        # Insert default items
        await swot_collection.insert_many(default_swot)
        # Initialise counter for future ids (max existing + 1)
        max_id = max(item["id"] for item in default_swot)
        await counters_collection.update_one(
            {"_id": "swot_id"},
            {"$set": {"seq": max_id}},
            upsert=True,
        )


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
