"""Schemas Pydantic de la carte des trajectoires."""

from datetime import datetime

from pydantic import BaseModel


class MapPoint(BaseModel):
    """Point geographique d'une extremite de trajectoire."""

    site: str | None
    departement: str | None
    date: datetime | None
    lat: float
    lon: float


class Trajectory(BaseModel):
    """Liaison cartographique agregee entre deux sites pour une espece."""

    id: str
    num_pit: str
    species: str | None
    gender: str | None
    age: str | None
    individual_count: int
    departure: MapPoint
    arrival: MapPoint
    distance_km: float
    color: str


class SiteMarker(BaseModel):
    """Marqueur de site a afficher sur la carte Leaflet."""

    site: str
    commune: str | None
    departement: str | None
    lat: float
    lon: float
    role: str


class MapBounds(BaseModel):
    """Emprise geographique permettant au frontend de cadrer la carte."""

    south: float
    west: float
    north: float
    east: float


class MapCenter(BaseModel):
    """Centre de secours ou centre moyen de la carte."""

    lat: float
    lon: float
    zoom: int = 6


class TrajectoryMapResponse(BaseModel):
    """Reponse complete consommee par le composant cartographique."""

    count: int
    center: MapCenter
    bounds: MapBounds | None
    species_colors: dict[str, str]
    trajectories: list[Trajectory]
    sites: list[SiteMarker]
