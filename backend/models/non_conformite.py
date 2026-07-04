from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# Valeurs autorisées (alignées sur la maquette). On les garde en str libres
# côté modèle pour rester tolérant, mais le frontend n'exposera que ces choix.
SOURCES = ["Audit interne", "Client", "Fournisseur", "Réclamation", "Interne"]
SERVICES = ["Management", "Production", "Qualité", "Achats", "Logistique", "RH", "Commercial"]
GRAVITES = ["Mineure", "Majeure", "Critique"]
STATUTS = ["Ouverte", "En cours", "Clôturée"]
ACTION_STATUTS = ["À faire", "En cours", "Abandonnée", "Reportée"]


class ActionCorrective(BaseModel):
    """Une action corrective individuelle, avec son propre suivi."""

    description: Optional[str] = None
    pilote: Optional[str] = None
    date_cloture: Optional[date] = None
    statut: str = "À faire"


class NonConformiteBase(BaseModel):
    date: date
    source: str
    service_impacte: str
    pilote: Optional[str] = None
    description: str
    gravite: str
    statut: str = "Ouverte"
    analyse_causes: Optional[str] = None
    actions_correctives: List[ActionCorrective] = Field(default_factory=list)
    date_cloture: Optional[date] = None


class NonConformiteCreate(NonConformiteBase):
    pass


class NonConformiteUpdate(BaseModel):
    date: Optional[date] = None
    source: Optional[str] = None
    service_impacte: Optional[str] = None
    pilote: Optional[str] = None
    description: Optional[str] = None
    gravite: Optional[str] = None
    statut: Optional[str] = None
    analyse_causes: Optional[str] = None
    actions_correctives: Optional[List[ActionCorrective]] = None
    date_cloture: Optional[date] = None


class NonConformiteOut(NonConformiteBase):
    id: str = Field(alias="_id")
    numero_ref: str
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {date: lambda d: d.isoformat()}