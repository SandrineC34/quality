import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.actions.routers import non_conformites, suivi_actions
from app.indicators.routers import indicateurs
from app.audits.routers import audits

app = FastAPI(title="SMQ Qualité API")

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


@app.get("/api/health")
async def health():
    return {"status": "ok"}
