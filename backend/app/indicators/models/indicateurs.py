from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class IndicateurCreate(BaseModel):
    processus: str
    reference_interne: Optional[str] = None
    reference_iso: Optional[str] = None
    description: str
    unite: str
    cible: float
    sens_cible: str
    methode_calcul: str
    frequence: str
    valeurs: Optional[List[float]] = None
    resultat_annuel: Optional[float] = None
    ecart_cible: Optional[float] = None
    statut: Optional[str] = None
    responsable: Optional[str] = None
    commentaires: Optional[str] = None


class IndicateurUpdate(BaseModel):
    processus: Optional[str] = None
    reference_interne: Optional[str] = None
    reference_iso: Optional[str] = None
    description: Optional[str] = None
    unite: Optional[str] = None
    cible: Optional[float] = None
    sens_cible: Optional[str] = None
    methode_calcul: Optional[str] = None
    frequence: Optional[str] = None
    valeurs: Optional[List[float]] = None
    resultat_annuel: Optional[float] = None
    ecart_cible: Optional[float] = None
    statut: Optional[str] = None
    responsable: Optional[str] = None
    commentaires: Optional[str] = None


class IndicateurOut(IndicateurCreate):
    id: str = Field(alias="_id")
    numero_ref: str
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {
            date: lambda d: d.isoformat()
        }