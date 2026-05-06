"""Schemas Pydantic lies aux filtres exposes par l'API."""

from datetime import date

from pydantic import BaseModel, Field


class FilterOptions(BaseModel):
    """Toutes les listes necessaires pour initialiser les formulaires frontend."""

    departements: list[str]
    departements_antennes: list[str]
    communes: list[str]
    species: list[str]
    genders: list[str]
    ages: list[str]
    sites: list[str]
    sites_by_commune: dict[str, list[str]]
    antenna_sites: list[str]
    periods: list[str]
    date_min: date | None
    date_max: date | None


class TrajectoryFilters(BaseModel):
    """Filtres applicables a la carte des trajectoires.

    Toutes les listes vides signifient "ne pas filtrer sur cette dimension".
    Les dates bornent les mouvements par depart/arrivee, et les periodes sont
    converties en mois via `PERIOD_MONTHS`.
    """

    departements: list[str] = Field(default_factory=list)
    species: list[str] = Field(default_factory=list)
    genders: list[str] = Field(default_factory=list)
    ages: list[str] = Field(default_factory=list)
    communes: list[str] = Field(default_factory=list)
    sites: list[str] = Field(default_factory=list)
    date_start: date | None = None
    date_end: date | None = None
    periods: list[str] = Field(default_factory=lambda: ["Transit", "Parturition", "Hivernale"])
