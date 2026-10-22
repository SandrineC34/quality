from fastapi import APIRouter, HTTPException, Body, Depends
import os
from typing import List

from app.database.connection import swot_collection, get_next_sequence

router = APIRouter()

TYPE_PREFIX = {"strength": "F", "weakness": "W", "opportunity": "O", "threat": "R"}

# --- CRUD for SWOT items -------------------------------------------------

@router.get("/api/swot")
async def get_swot_items():
    """Return all SWOT items ordered by id."""
    items = []
    cursor = swot_collection.find().sort("id", 1)
    async for doc in cursor:
        doc.pop("_id", None)  # Remove Mongo internal id
        items.append(doc)
    return items

@router.post("/api/swot")
async def create_swot_item(item: dict = Body(...)):
    """Create a new SWOT item. Expected fields: type (str), text (str)."""
    if "type" not in item or "text" not in item:
        raise HTTPException(status_code=422, detail="Missing 'type' or 'text' fields")
    new_id = await get_next_sequence("swot_id")
    count = await swot_collection.count_documents({"type": item["type"]}) + 1
    prefix = TYPE_PREFIX.get(item["type"], "")
    ref = f"{prefix}{count}"
    doc = {"id": new_id, "type": item["type"], "text": item["text"], "ref": ref}
    await swot_collection.insert_one(doc)
    return doc

@router.put("/api/swot/{item_id}")
async def update_swot_item(item_id: int, payload: dict = Body(...)):
    """Update the text of a SWOT item. Payload must contain 'text'."""
    if "text" not in payload:
        raise HTTPException(status_code=422, detail="Missing 'text' field")
    result = await swot_collection.find_one_and_update(
        {"id": item_id},
        {"$set": {"text": payload["text"]}},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    result.pop("_id", None)
    return result

@router.delete("/api/swot/{item_id}")
async def delete_swot_item(item_id: int):
    """Delete a SWOT item by its id."""
    result = await swot_collection.delete_one({"id": item_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"status": "deleted", "id": item_id}

# --- TOWS export --------------------------------------------------------

@router.post("/api/swot/tows")
async def save_tows(html: str = Body(..., media_type="text/plain")):
    # Determine the absolute path to the TOWS HTML file in the frontend public folder
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/public/Enjeux"))
    file_path = os.path.join(base_dir, "2-tows.html")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
        return {"status": "saved", "path": file_path}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
