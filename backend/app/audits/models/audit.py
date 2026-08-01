from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class AuditCreate(BaseModel):
    processus: str
    auditeur: str
    date_planifiee: date
    statut: str = "Planifié"
    perimetre: Optional[str] = None
    date_realisation: Optional[date] = None
    constats: Optional[str] = None
    rapport_reference: Optional[str] = None
    date_cloture: Optional[date] = None
    prochain_audit: Optional[date] = None


class AuditUpdate(BaseModel):
    processus: Optional[str] = None
    auditeur: Optional[str] = None
    date_planifiee: Optional[date] = None
    statut: Optional[str] = None
    perimetre: Optional[str] = None
    date_realisation: Optional[date] = None
    constats: Optional[str] = None
    rapport_reference: Optional[str] = None
    date_cloture: Optional[date] = None
    prochain_audit: Optional[date] = None


class AuditOut(AuditCreate):
    id: str = Field(alias="_id")
    numero_ref: str
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {
            date: lambda d: d.isoformat()
        }