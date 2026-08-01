from datetime import datetime, date
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query

from app.database.connection import audits_collection, get_next_sequence
from app.audits.models.audit import AuditCreate, AuditUpdate

router = APIRouter(prefix="/audits", tags=["audits"])


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
    for field in ("date_planifiee", "date_realisation", "date_cloture", "prochain_audit"):
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
async def list_audits(
    search: Optional[str] = Query(default=None),
    statut: Optional[str] = Query(default=None),
):
    query: dict = {}
    if statut and statut != "Tous les statuts":
        query["statut"] = statut
    if search:
        query["$or"] = [
            {"numero_ref": {"$regex": search, "$options": "i"}},
            {"processus": {"$regex": search, "$options": "i"}},
            {"auditeur": {"$regex": search, "$options": "i"}},
            {"constats": {"$regex": search, "$options": "i"}},
        ]

    cursor = audits_collection.find(query).sort("created_at", -1)
    results = [serialize(doc) async for doc in cursor]
    return results


@router.post("", status_code=201)
async def create_audit(payload: AuditCreate):
    seq = await get_next_sequence(f"aud_{datetime.utcnow().year}")
    now = datetime.utcnow()

    doc = to_mongo_safe(payload.model_dump())
    doc["numero_ref"] = f"AUD-{datetime.utcnow().year}-{seq:03d}"
    doc["created_at"] = now
    doc["updated_at"] = now

    result = await audits_collection.insert_one(doc)
    created = await audits_collection.find_one({"_id": result.inserted_id})
    return serialize(created)


@router.get("/{audit_id}")
async def get_audit(audit_id: str):
    if not ObjectId.is_valid(audit_id):
        raise HTTPException(status_code=400, detail="Identifiant invalide")
    doc = await audits_collection.find_one({"_id": ObjectId(audit_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Audit introuvable")
    return serialize(doc)


@router.put("/{audit_id}")
async def update_audit(audit_id: str, payload: AuditUpdate):
    if not ObjectId.is_valid(audit_id):
        raise HTTPException(status_code=400, detail="Identifiant invalide")

    update_data = to_mongo_safe(payload.model_dump(exclude_unset=True))
    update_data["updated_at"] = datetime.utcnow()

    result = await audits_collection.update_one(
        {"_id": ObjectId(audit_id)}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Audit introuvable")

    doc = await audits_collection.find_one({"_id": ObjectId(audit_id)})
    return serialize(doc)


@router.delete("/{audit_id}", status_code=204)
async def delete_audit(audit_id: str):
    if not ObjectId.is_valid(audit_id):
        raise HTTPException(status_code=400, detail="Identifiant invalide")
    result = await audits_collection.delete_one({"_id": ObjectId(audit_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Audit introuvable")
    return None