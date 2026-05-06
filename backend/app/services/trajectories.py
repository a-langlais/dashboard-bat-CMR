"""Services de filtrage et d'agregation des trajectoires cartographiques."""

import pandas as pd

from app.core.constants import PERIOD_MONTHS, SPECIES_COLORS
from app.repositories.csv_repository import CmrData
from app.schemas.filters import TrajectoryFilters
from app.schemas.map import (
    MapBounds,
    MapCenter,
    MapPoint,
    SiteMarker,
    Trajectory,
    TrajectoryMapResponse,
)


DEFAULT_CENTER = MapCenter(lat=46.493889, lon=2.602778, zoom=6)


def filter_trajectories(data: CmrData, filters: TrajectoryFilters) -> pd.DataFrame:
    """Applique les filtres cartographiques et agrege les liaisons.

    Les filtres geographiques ont une logique volontairement "individu" :
    lorsqu'un departement, une commune ou un site est selectionne, on conserve
    toutes les trajectoires des individus concernes. Cela permet de comprendre
    leurs deplacements complets autour du critere choisi, plutot que de couper
    artificiellement les liaisons au seul segment qui touche le filtre.
    """
    df = data.distances.copy()

    if filters.departements:
        # Un individu est conserve s'il a au moins une liaison dont le depart ou
        # l'arrivee se trouve dans l'un des departements selectionnes.
        equipped_pit = df[
            df["DPT_DEPART"].astype(str).isin(filters.departements)
            | df["DPT_ARRIVEE"].astype(str).isin(filters.departements)
        ]["NUM_PIT"].unique()
        df = df[df["NUM_PIT"].isin(equipped_pit)]

    if filters.species:
        df = df[df["CODE_ESP"].astype(str).isin(filters.species)]

    if filters.genders:
        df = df[df["SEXE"].astype(str).isin(filters.genders)]

    if filters.ages:
        df = df[df["AGE"].astype(str).isin(filters.ages)]

    if filters.communes:
        # Les communes sont traduites en noms de sites via `df_sites.csv`, puis
        # appliquees aux sites de depart/arrivee des distances.
        site_names = data.sites[
            data.sites["COMMUNE"].astype(str).isin(filters.communes)
        ]["LIEU_DIT"].dropna()
        site_pit = df[
            df["SITE_DEPART"].isin(site_names) | df["SITE_ARRIVEE"].isin(site_names)
        ]["NUM_PIT"].unique()
        df = df[df["NUM_PIT"].isin(site_pit)]

    if filters.sites:
        site_pit = df[
            df["SITE_DEPART"].isin(filters.sites) | df["SITE_ARRIVEE"].isin(filters.sites)
        ]["NUM_PIT"].unique()
        df = df[df["NUM_PIT"].isin(site_pit)]

    if filters.date_start:
        df = df[df["DATE_DEPART"] >= pd.Timestamp(filters.date_start)]

    if filters.date_end:
        df = df[df["DATE_ARRIVEE"] <= pd.Timestamp(filters.date_end)]

    selected_periods = filters.periods or list(PERIOD_MONTHS.keys())
    selected_months = [
        month
        for period in selected_periods
        for month in PERIOD_MONTHS.get(period, [])
    ]
    if selected_months:
        df = df[df["DATE_ARRIVEE"].dt.month.isin(selected_months)]

    # Avant de dedoublonner la liaison, on calcule le nombre d'individus uniques
    # qui l'ont realisee. C'est cette valeur qui est affichee au survol de la
    # carte et qui evite de confondre "nombre de lignes" et "nombre d'individus".
    group_columns = ["CODE_ESP", "SITE_DEPART", "SITE_ARRIVEE"]
    df["__individual_count"] = df.groupby(group_columns)["NUM_PIT"].transform("nunique")

    return df.drop_duplicates(
        subset=["CODE_ESP", "SITE_DEPART", "SITE_ARRIVEE"],
        keep="last",
    )


def build_trajectory_map(data: CmrData, filters: TrajectoryFilters) -> TrajectoryMapResponse:
    """Construit la reponse prete pour Leaflet.

    Le frontend recoit directement les lignes, les marqueurs, les bornes de
    cadrage et la palette. Il n'a donc pas besoin de connaitre la structure CSV
    ni de refaire des calculs lourds cote navigateur.
    """
    df = filter_trajectories(data, filters)

    if df.empty:
        return TrajectoryMapResponse(
            count=0,
            center=DEFAULT_CENTER,
            bounds=None,
            species_colors=SPECIES_COLORS,
            trajectories=[],
            sites=[],
        )

    latitudes = pd.concat([df["LAT_DEPART"], df["LAT_ARRIVEE"]])
    longitudes = pd.concat([df["LONG_DEPART"], df["LONG_ARRIVEE"]])
    center = MapCenter(
        lat=float(latitudes.mean()),
        lon=float(longitudes.mean()),
        zoom=6,
    )
    bounds = MapBounds(
        south=float(latitudes.min()),
        west=float(longitudes.min()),
        north=float(latitudes.max()),
        east=float(longitudes.max()),
    )

    trajectories = [
        _row_to_trajectory(index, row)
        for index, row in df.reset_index(drop=True).iterrows()
    ]

    return TrajectoryMapResponse(
        count=len(trajectories),
        center=center,
        bounds=bounds,
        species_colors=SPECIES_COLORS,
        trajectories=trajectories,
        sites=_build_site_markers(data, df),
    )


def _row_to_trajectory(index: int, row: pd.Series) -> Trajectory:
    """Convertit une ligne pandas en contrat Pydantic de trajectoire."""
    species = _optional_str(row.get("CODE_ESP"))
    return Trajectory(
        id=f"{_optional_str(row.get('NUM_PIT'))}-{index}",
        num_pit=_optional_str(row.get("NUM_PIT")) or "",
        species=species,
        gender=_optional_str(row.get("SEXE")),
        age=_optional_str(row.get("AGE")),
        individual_count=int(row.get("__individual_count", 1)),
        departure=MapPoint(
            site=_optional_str(row.get("SITE_DEPART")),
            departement=_optional_str(row.get("DPT_DEPART")),
            date=_optional_datetime(row.get("DATE_DEPART")),
            lat=float(row["LAT_DEPART"]),
            lon=float(row["LONG_DEPART"]),
        ),
        arrival=MapPoint(
            site=_optional_str(row.get("SITE_ARRIVEE")),
            departement=_optional_str(row.get("DPT_ARRIVEE")),
            date=_optional_datetime(row.get("DATE_ARRIVEE")),
            lat=float(row["LAT_ARRIVEE"]),
            lon=float(row["LONG_ARRIVEE"]),
        ),
        distance_km=round(float(row["DIST_KM"]), 3),
        color=SPECIES_COLORS.get(species or "", "gray"),
    )


def _build_site_markers(data: CmrData, df: pd.DataFrame) -> list[SiteMarker]:
    """Cree les points de sites visibles sur la carte.

    Le role sert au frontend a distinguer les sites seulement depart, seulement
    arrivee, ou les deux. Les coordonnees viennent de `df_sites.csv`, source
    geographique de reference du projet.
    """
    departures = set(df["SITE_DEPART"].dropna().astype(str).tolist())
    arrivals = set(df["SITE_ARRIVEE"].dropna().astype(str).tolist())
    site_names = departures | arrivals
    sites = data.sites[data.sites["LIEU_DIT"].astype(str).isin(site_names)]

    markers = []
    for _, site in sites.iterrows():
        name = str(site["LIEU_DIT"])
        role = "both" if name in departures and name in arrivals else "departure"
        if name in arrivals and name not in departures:
            role = "arrival"
        markers.append(
            SiteMarker(
                site=name,
                commune=_optional_str(site.get("COMMUNE")),
                departement=_optional_str(site.get("DEPARTEMENT")),
                lat=float(site["LAT_WGS"]),
                lon=float(site["LONG_WGS"]),
                role=role,
            )
        )
    return markers


def _optional_str(value: object) -> str | None:
    """Convertit une valeur pandas potentiellement vide en chaine optionnelle."""
    if pd.isna(value):
        return None
    return str(value)


def _optional_datetime(value: object):
    """Convertit une valeur date pandas en datetime serialisable par Pydantic."""
    if pd.isna(value):
        return None
    return pd.Timestamp(value).to_pydatetime()
