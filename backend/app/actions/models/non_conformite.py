# ==============================================================================
# MODELES PYDANTIC - Gestion des Non-Conformités
# ------------------------------------------------------------------------------
#
# Ce fichier définit la structure des données utilisées par l'application.
#
# Les modèles Pydantic servent à plusieurs choses :
#
# • Vérifier automatiquement les données reçues du frontend Vue3.
# • Générer automatiquement la documentation Swagger de FastAPI.
# • Garantir que les données envoyées à MongoDB sont cohérentes.
# • Faciliter l'autocomplétion dans l'éditeur de code.
#
# On peut voir ce fichier comme le "plan" ou la "fiche d'identité"
# d'une non-conformité.
#
# ==============================================================================

from datetime import date, datetime
from typing import Optional, List

# BaseModel est la classe principale de Pydantic.
# Toutes nos classes hériteront de BaseModel.
from pydantic import BaseModel, Field


# ==============================================================================
# Listes de valeurs proposées dans le frontend
# ==============================================================================
#
# Ces constantes représentent les choix disponibles dans les listes déroulantes.
#
# Elles servent essentiellement au frontend Vue3.
#
# Le backend reste volontairement souple :
# il accepte n'importe quelle chaîne de caractères.
#
# Plus tard on pourra renforcer les contrôles avec des Enum.
# ==============================================================================

SOURCES = [
    "Audit interne",
    "Client",
    "Fournisseur",
    "Réclamation",
    "Interne",
]

SERVICES = [
    "Management",
    "Production",
    "Qualité",
    "Achats",
    "Logistique",
    "RH",
    "Commercial",
]

GRAVITES = [
    "Mineure",
    "Majeure",
    "Critique",
]

STATUTS = [
    "Ouverte",
    "En cours",
    "Clôturée",
]

ACTION_STATUTS = [
    "À faire",
    "En cours",
    "Abandonnée",
    "Reportée",
]


# ==============================================================================
# Modèle représentant UNE action corrective
# ==============================================================================
#
# Une non-conformité peut posséder plusieurs actions correctives.
#
# Exemple :
#
# NC-2026-001
#
#    Action 1
#    Action 2
#    Action 3
#
# Cette classe représente UNE seule action.
# ==============================================================================
class ActionCorrective(BaseModel):

    """Une action corrective individuelle."""

    # Description de l'action
    description: Optional[str] = None

    # Responsable de cette action
    pilote: Optional[str] = None

    # Date prévue  clôture
    date_objectif: Optional[date] = None

    # Date réelle de clôture
    date_cloture: Optional[date] = None

    # Efficacité de l'action
    efficacite: Optional[str] = None

    # Etat de l'action
    statut: str = "À faire"


# ==============================================================================
# Classe de base d'une Non-Conformité
# ==============================================================================
#
# Cette classe contient tous les champs communs.
#
# Elle sera réutilisée par plusieurs autres modèles :
#
#       NonConformiteBase
#              ▲
#      ┌───────┴─────────┐
#      │                 │
# Create             Out
#
# Cela évite de recopier les mêmes champs plusieurs fois.
# ==============================================================================
class NonConformiteBase(BaseModel):

    # Date de détection
    date: date

    # Origine de la NC
    source: str

    # Service concerné
    service_impacte: str

    # Responsable de suivi
    pilote: Optional[str] = None

    # Description de la non-conformité
    description: str

    # Gravité
    gravite: str

    # Statut actuel
    statut: str = "Ouverte"

    # Analyse des causes
    analyse_causes: Optional[str] = None

    # Action curative immédiate
    action_curative: Optional[str] = None
    date_action_curative: Optional[date] = None

    # Liste des actions correctives.
    #
    # default_factory=list crée automatiquement une liste vide.
    #
    # Sans cela, plusieurs objets pourraient partager
    # la même liste en mémoire.
    actions_correctives: List[ActionCorrective] = Field(
        default_factory=list
    )

    # Date de clôture globale
    date_cloture: Optional[date] = None


    # Preuves/commentaires
    preuves: Optional[str] = None


# ==============================================================================
# Modèle utilisé lors de la création
# ==============================================================================
#
# Lorsqu'un utilisateur crée une nouvelle non-conformité,
# FastAPI utilise cette classe.
#
# Elle hérite directement de NonConformiteBase.
#
# Aucun champ supplémentaire n'est nécessaire.
# ==============================================================================
class NonConformiteCreate(NonConformiteBase):
    pass


# ==============================================================================
# Modèle utilisé lors d'une modification
# ==============================================================================
#
# Lors d'une mise à jour, l'utilisateur ne modifie
# généralement que quelques champs.
#
# Exemple :
#
# {
#      "statut":"Clôturée"
# }
#
# Tous les champs deviennent donc Optionnels.
#
# FastAPI mettra uniquement à jour ceux présents
# dans la requête.
# ==============================================================================
class NonConformiteUpdate(BaseModel):

    date: Optional[date] = None

    source: Optional[str] = None

    service_impacte: Optional[str] = None

    pilote: Optional[str] = None

    description: Optional[str] = None

    gravite: Optional[str] = None

    statut: Optional[str] = None

    analyse_causes: Optional[str] = None

    action_curative: Optional[str] = None
    date_action_curative: Optional[date] = None

    actions_correctives: Optional[
        List[ActionCorrective]
    ] = None

    date_cloture: Optional[date] = None


# ==============================================================================
# Modèle renvoyé au frontend
# ==============================================================================
#
# Lorsque le frontend demande une non-conformité,
# c'est cette classe qui représente les données renvoyées.
#
# Elle contient les informations de NonConformiteBase
# auxquelles s'ajoutent les informations techniques
# créées par MongoDB.
# ==============================================================================
class NonConformiteOut(NonConformiteBase):

    # Identifiant MongoDB
    #
    # Dans MongoDB il s'appelle "_id".
    #
    # Dans Python on préfère "id".
    id: str = Field(alias="_id")

    # Référence automatique
    #
    # Exemple :
    # NC-2026-001
    numero_ref: str

    # Date de création
    created_at: datetime

    # Dernière modification
    updated_at: datetime

    # --------------------------------------------------------------------------
    # Configuration Pydantic
    # --------------------------------------------------------------------------
    class Config:

        # Autorise l'utilisation du nom Mongo "_id"
        # ou du nom Python "id".
        populate_by_name = True

        # Toutes les dates seront automatiquement
        # converties en texte ISO.
        #
        # Exemple :
        #
        # 2026-05-18
        #
        json_encoders = {
            date: lambda d: d.isoformat()
        }