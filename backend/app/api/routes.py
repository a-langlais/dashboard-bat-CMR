"""Routes HTTP exposees par le backend.

Les handlers gardent une responsabilite minimale : valider les parametres via
FastAPI/Pydantic, recuperer le jeu de donnees mis en cache, deleguer la logique
aux services, puis serialiser explicitement les modeles Pydantic. Cette forme
limite le cout de validation sur les gros payloads tout en conservant des
contrats internes types.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.repositories.csv_repository import CmrData, get_cmr_data
from app.schemas.filters import TrajectoryFilters
from app.services.filters import get_filter_options
from app.services.stats import get_global_stats, get_phenology, get_site_summary
from app.services.trajectories import build_trajectory_map

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """Endpoint leger pour verifier que le processus API repond."""
    return {"status": "ok"}


@router.get("/filters")
def filters(data: CmrData = Depends(get_cmr_data)):
    """Retourne toutes les valeurs necessaires aux formulaires de filtres."""
    return get_filter_options(data).model_dump(mode="json")


@router.post("/map/trajectories")
def map_trajectories(
    filters: TrajectoryFilters,
    data: CmrData = Depends(get_cmr_data),
):
    """Construit les trajectoires cartographiques deja agregees et colorisees."""
    return build_trajectory_map(data, filters).model_dump(mode="json")


@router.get("/stats/global")
def global_stats(data: CmrData = Depends(get_cmr_data)):
    """Retourne les KPI et series alimentant l'onglet Statistiques."""
    return get_global_stats(data).model_dump(mode="json")


@router.get("/phenology")
def phenology(
    departements: Annotated[list[str] | None, Query()] = None,
    date_start: str | None = None,
    date_end: str | None = None,
    gap_days: int = 7,
    data: CmrData = Depends(get_cmr_data),
):
    """Agrege les presences par site antenne pour l'onglet Phenologie.

    `gap_days` controle la fusion de detections proches : deux passages sur un
    meme site separes d'au plus cette valeur sont consideres comme appartenant
    a une meme periode de presence.
    """
    return [
        item.model_dump(mode="json")
        for item in get_phenology(
            data,
            departements=departements,
            date_start=date_start,
            date_end=date_end,
            gap_days=gap_days,
        )
    ]


@router.get("/sites/{site}/summary")
def site_summary(site: str, data: CmrData = Depends(get_cmr_data)):
    """Retourne une fiche analytique pour un site equipe donne."""
    return get_site_summary(data, site).model_dump(mode="json")
