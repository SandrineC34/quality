from datetime import datetime, date
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query

from app.database.connection import suivi_actions_collection, get_next_sequence
from app.actions.models.suivi_action import SuiviActionCreate, SuiviActionUpdate

router = APIRouter(prefix="/actions", tags=["suivi-actions"])


def to_mongo_safe(value):
    if isinstance(value, date) and not isinstance(value, datetime):
        return datetime(value.year, value.month, value.day)
    if isinstance(value, dict):
        return {k: to_mongo_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [to_mongo_safe(v) for v in value]
    return value


def serialize(doc: dict) -> dict:
    doc["_id"] = str(doc["_id"])
    for field in ("date_creation", "date_prevue", "date_cloture", "date_mesure_efficacite"):
        value = doc.get(field)
        if isinstance(value, datetime):
            doc[field] = value.date().isoformat()
        elif isinstance(value, date):
            doc[field] = value.isoformat()
    for field in ("created_at", "updated_at"):
        if isinstance(doc.get(field), datetime):
            doc[field] = doc[field].isoformat()
    return doc


@router.get("")
async def list_suivi_actions(
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
            {"origine": {"$regex": search, "$options": "i"}},
            {"responsable": {"$regex": search, "$options": "i"}},
        ]

    cursor = suivi_actions_collection.find(query).sort("created_at", -1)
    results = [serialize(doc) async for doc in cursor]
    return results


@router.post("", status_code=201)
async def create_suivi_action(payload: SuiviActionCreate):
    seq = await get_next_sequence(f"act_{datetime.utcnow().year}")
    now = datetime.utcnow()

    doc = to_mongo_safe(payload.model_dump())
    doc["numero_ref"] = f"ACT-{datetime.utcnow().year}-{seq:03d}"
    doc["created_at"] = now
    doc["updated_at"] = now

    result = await suivi_actions_collection.insert_one(doc)
    created = await suivi_actions_collection.find_one({"_id": result.inserted_id})
    return serialize(created)


@router.get("/{action_id}")
async def get_suivi_action(action_id: str):
    if not ObjectId.is_valid(action_id):
        raise HTTPException(status_code=400, detail="Identifiant invalide")
    doc = await suivi_actions_collection.find_one({"_id": ObjectId(action_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Action de suivi introuvable")
    return serialize(doc)


@router.put("/{action_id}")
async def update_suivi_action(action_id: str, payload: SuiviActionUpdate):
    if not ObjectId.is_valid(action_id):
        raise HTTPException(status_code=400, detail="Identifiant invalide")

    update_data = to_mongo_safe(payload.model_dump(exclude_unset=True))
    update_data["updated_at"] = datetime.utcnow()

    result = await suivi_actions_collection.update_one(
        {"_id": ObjectId(action_id)}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Action de suivi introuvable")

    doc = await suivi_actions_collection.find_one({"_id": ObjectId(action_id)})
    return serialize(doc)


@router.delete("/{action_id}", status_code=204)
async def delete_suivi_action(action_id: str):
    if not ObjectId.is_valid(action_id):
        raise HTTPException(status_code=400, detail="Identifiant invalide")
    result = await suivi_actions_collection.delete_one({"_id": ObjectId(action_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Action de suivi introuvable")
    return None