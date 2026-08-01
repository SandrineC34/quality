from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class SuiviActionCreate(BaseModel):
    date_creation: date
    origine: str
    origine_ref: Optional[str] = None
    type_action: str
    description: str
    responsable: str
    date_prevue: date
    priorite: str
    statut: str = "À faire"
    date_cloture: Optional[date] = None
    preuves: Optional[str] = None
    criteres_efficacite: Optional[str] = None
    date_mesure_efficacite: Optional[date] = None
    resultat_efficacite: str = "Non évaluée"
    commentaire_efficacite: Optional[str] = None
    valide_par: Optional[str] = None


class SuiviActionUpdate(BaseModel):
    date_creation: Optional[date] = None
    origine: Optional[str] = None
    origine_ref: Optional[str] = None
    type_action: Optional[str] = None
    description: Optional[str] = None
    responsable: Optional[str] = None
    date_prevue: Optional[date] = None
    priorite: Optional[str] = None
    statut: Optional[str] = None
    date_cloture: Optional[date] = None
    preuves: Optional[str] = None
    criteres_efficacite: Optional[str] = None
    date_mesure_efficacite: Optional[date] = None
    resultat_efficacite: Optional[str] = None
    commentaire_efficacite: Optional[str] = None
    valide_par: Optional[str] = None


class SuiviActionOut(SuiviActionCreate):
    id: str = Field(alias="_id")
    numero_ref: str
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {
            date: lambda d: d.isoformat()
        }