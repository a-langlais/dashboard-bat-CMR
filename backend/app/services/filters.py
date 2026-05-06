"""Construction des options de filtres exposees au frontend."""

import pandas as pd

from app.core.constants import ANTENNA_SITES, PERIOD_MONTHS
from app.repositories.csv_repository import CmrData
from app.schemas.filters import FilterOptions


def _sorted_values(series: pd.Series) -> list[str]:
    """Transforme une colonne pandas en liste de valeurs uniques triables."""
    values = series.dropna().astype(str).unique().tolist()
    return sorted(values)


def get_filter_options(data: CmrData) -> FilterOptions:
    """Produit le contrat complet des filtres disponibles.

    Les options sont derivees des donnees chargees afin que l'interface reste
    synchronisee avec les CSV actuels. Les filtres plus metier, comme les
    periodes saisonnieres, viennent des constantes applicatives.
    """
    controls = data.controls
    distances = data.distances

    antenna_controls = controls[controls["LIEU_DIT"].isin(ANTENNA_SITES)]

    return FilterOptions(
        departements=_sorted_values(controls["DEPARTEMENT"]),
        departements_antennes=_sorted_values(antenna_controls["DEPARTEMENT"]),
        communes=_sorted_values(controls["COMMUNE"]),
        species=_sorted_values(distances["CODE_ESP"]),
        genders=_sorted_values(data.individus["SEXE"]),
        ages=_sorted_values(data.individus["AGE"]),
        sites=_sorted_values(controls["LIEU_DIT"]),
        sites_by_commune=_sites_by_commune(controls),
        antenna_sites=ANTENNA_SITES,
        periods=list(PERIOD_MONTHS.keys()),
        date_min=controls["DATE"].min().date() if controls["DATE"].notna().any() else None,
        date_max=controls["DATE"].max().date() if controls["DATE"].notna().any() else None,
    )


def _sites_by_commune(controls: pd.DataFrame) -> dict[str, list[str]]:
    """Indexe les sites par commune pour filtrer dynamiquement le formulaire."""
    scoped = controls[["COMMUNE", "LIEU_DIT"]].dropna().copy()
    grouped = scoped.groupby("COMMUNE")["LIEU_DIT"].unique()
    return {
        str(commune): sorted(str(site) for site in sites)
        for commune, sites in grouped.items()
    }
