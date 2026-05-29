"""Schemas Pydantic des statistiques et fiches sites."""

from datetime import date, datetime

from pydantic import BaseModel


class Kpis(BaseModel):
    """Indicateurs synthétiques affiches en haut des pages analytiques."""

    total_marked: int
    total_recaptured: int
    capture_sites: int
    antenna_sites: int
    local_control_rate: float | None = None
    follow_up_years: int | None = None


class YearCount(BaseModel):
    """Valeur annuelle par espece pour les graphiques empiles."""

    year: int
    species: str
    count: int


class CategoryCount(BaseModel):
    """Comptage generique label/valeur pour donuts et barres."""

    label: str
    count: int


class DailyFrequency(BaseModel):
    """Nombre de detections par jour du calendrier, au format MM-DD."""

    month_day: str
    count: int


class DistanceValue(BaseModel):
    """Distance individuelle rattachee a une espece."""

    species: str
    distance_km: float


class TransitionRow(BaseModel):
    """Ligne de la table exploratoire des trajectoires."""

    num_pit: str
    species: str | None
    date_depart: datetime | None
    site_depart: str | None
    date_arrivee: datetime | None
    site_arrivee: str | None
    distance_km: float


class GlobalStats(BaseModel):
    """Payload complet de l'onglet Statistiques."""

    kpis: Kpis
    detections_by_year: list[YearCount]
    captures_by_year: list[YearCount]
    controls_by_year: list[YearCount]
    detected_species: list[CategoryCount]
    marked_species: list[CategoryCount]
    daily_frequency: list[DailyFrequency]
    top_detections: list[CategoryCount]
    distances: list[DistanceValue]
    transitions: list[TransitionRow]


class PhenologySegment(BaseModel):
    """Periode continue de presence sur un site."""

    start: date
    finish: date


class SitePhenology(BaseModel):
    """Timeline de presence pour un site antenne."""

    site: str
    departement: str | None
    visits: list[PhenologySegment]


class SiteSummary(BaseModel):
    """Payload d'une fiche site."""

    site: str
    kpis: Kpis
    detections_by_year: list[YearCount]
    captures_by_year: list[YearCount]
    controls_by_year: list[YearCount]
    detected_species: list[CategoryCount]
    marked_species: list[CategoryCount]
    daily_frequency: list[DailyFrequency]
    phenology: list[SitePhenology]
