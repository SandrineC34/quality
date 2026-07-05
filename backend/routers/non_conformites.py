from datetime import datetime, date
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query

from database import non_conformites_collection, get_next_sequence
from models.non_conformite import NonConformiteCreate, NonConformiteUpdate

router = APIRouter(prefix="/non-conformites", tags=["non-conformites"])


def to_mongo_safe(value):
    """Convertit récursivement les objets date() en datetime() : bson ne sait encoder que datetime.
    Gère aussi les dicts et listes imbriqués (ex: actions_correctives)."""
    if isinstance(value, date) and not isinstance(value, datetime):
        return datetime(value.year, value.month, value.day)
    if isinstance(value, dict):
        return {k: to_mongo_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [to_mongo_safe(v) for v in value]
    return value


def serialize(doc: dict) -> dict:
    """Convertit un document Mongo en dict JSON-safe pour le frontend.

    Important : les champs date (y compris "date_cloture" dans chaque action
    corrective) sont stockés en datetime() (bson l'exige), mais <input type="date">
    côté frontend n'accepte QUE le format "YYYY-MM-DD". On force donc
    systématiquement la partie date pure ici.
    """
    doc["_id"] = str(doc["_id"])
    for field in ("date", "date_cloture"):
        value = doc.get(field)
        if isinstance(value, datetime):
            doc[field] = value.date().isoformat()
        elif isinstance(value, date):
            doc[field] = value.isoformat()
    for action in doc.get("actions_correctives") or []:
        value = action.get("date_cloture")
        if isinstance(value, datetime):
            action["date_cloture"] = value.date().isoformat()
        elif isinstance(value, date):
            action["date_cloture"] = value.isoformat()
    for field in ("created_at", "updated_at"):
        if isinstance(doc.get(field), datetime):
            doc[field] = doc[field].isoformat()
    return doc


@router.get("")
async def list_non_conformites(
    search: Optional[str] = Query(default=None),
    statut: Optional[str] = Query(default=None),
):
    query: dict = {}
    if statut and statut != "Tous les statuts":
        query["statut"] = statut
    if search:
        query["$or"] = [
            {"numero_ref": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"service_impacte": {"$regex": search, "$options": "i"}},
            {"source": {"$regex": search, "$options": "i"}},
            {"pilote": {"$regex": search, "$options": "i"}},
            {"actions_correctives.pilote": {"$regex": search, "$options": "i"}},
            {"actions_correctives.statut": {"$regex": search, "$options": "i"}},
        ]

    cursor = non_conformites_collection.find(query).sort("created_at", -1)
    results = [serialize(doc) async for doc in cursor]
    return results


@router.post("", status_code=201)
async def create_non_conformite(payload: NonConformiteCreate):
    seq = await get_next_sequence(f"nc_{datetime.utcnow().year}")
    now = datetime.utcnow()

    doc = to_mongo_safe(payload.model_dump())
    doc["numero_ref"] = f"NC-{datetime.utcnow().year}-{seq:03d}"
    doc["created_at"] = now
    doc["updated_at"] = now

    result = await non_conformites_collection.insert_one(doc)
    created = await non_conformites_collection.find_one({"_id": result.inserted_id})
    return serialize(created)


@router.get("/{nc_id}")
async def get_non_conformite(nc_id: str):
    if not ObjectId.is_valid(nc_id):
        raise HTTPException(status_code=400, detail="Identifiant invalide")
    doc = await non_conformites_collection.find_one({"_id": ObjectId(nc_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Non-conformité introuvable")
    return serialize(doc)


@router.put("/{nc_id}")
async def update_non_conformite(nc_id: str, payload: NonConformiteUpdate):
    if not ObjectId.is_valid(nc_id):
        raise HTTPException(status_code=400, detail="Identifiant invalide")

    update_data = to_mongo_safe(payload.model_dump(exclude_unset=True))
    update_data["updated_at"] = datetime.utcnow()

    result = await non_conformites_collection.update_one(
        {"_id": ObjectId(nc_id)}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Non-conformité introuvable")

    doc = await non_conformites_collection.find_one({"_id": ObjectId(nc_id)})
    return serialize(doc)


@router.delete("/{nc_id}", status_code=204)
async def delete_non_conformite(nc_id: str):
    if not ObjectId.is_valid(nc_id):
        raise HTTPException(status_code=400, detail="Identifiant invalide")
    result = await non_conformites_collection.delete_one({"_id": ObjectId(nc_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Non-conformité introuvable")
    return None