"""Services statistiques du dashboard.

Les fonctions de ce module transforment les CSV nettoyes en petites structures
adaptees aux composants React : KPI, series annuelles, repartitions, frequences
journalieres, phenologie et table de trajectoires. Les traitements restent ici
pour garder la couche API legere et permettre de tester chaque aggregation
independamment.
"""

import pandas as pd

from app.core.constants import ANTENNA_SITES
from app.repositories.csv_repository import CmrData
from app.schemas.stats import (
    CategoryCount,
    DailyFrequency,
    DistanceValue,
    GlobalStats,
    Kpis,
    PhenologySegment,
    SitePhenology,
    SiteSummary,
    TransitionRow,
    YearCount,
)

VALID_STUDIES = [
    "Diag CEN",
    "Diag NATURA 2000",
    "Diag FDS_Oléron",
    "ECOFECT (GR/CCPNA)",
    "ECOFECT (Hors GR)",
    "TRANSPY ESPAGNE",
    "TRANSPY FRANCE",
]


def get_global_stats(data: CmrData) -> GlobalStats:
    """Construit toutes les donnees de l'onglet Statistiques.

    Les graphiques descriptifs sont limites aux etudes validees, tandis que les
    KPI globaux restent calcules sur les donnees sources completes afin de ne pas
    masquer l'ampleur du jeu CMR disponible.
    """
    controls = _valid_studies(data.controls)
    individus = _valid_studies(data.individus)

    return GlobalStats(
        kpis=_kpis(data.controls, data.individus, data.sites),
        detections_by_year=_counts_by_year(controls, unique_individuals=False),
        captures_by_year=_counts_by_year(individus, unique_individuals=True),
        controls_by_year=_counts_by_year(controls, unique_individuals=True),
        detected_species=_category_counts(controls, "CODE_ESP"),
        marked_species=_category_counts(individus, "CODE_ESP"),
        daily_frequency=_daily_frequency(controls),
        top_detections=_top_detections(controls),
        distances=_distances(data.distances),
        transitions=_transitions(data.distances),
    )


def get_phenology(
    data: CmrData,
    departements: list[str] | None = None,
    date_start: str | None = None,
    date_end: str | None = None,
    sites: list[str] | None = None,
    gap_days: int = 7,
) -> list[SitePhenology]:
    """Agrege les detections en periodes de presence par site.

    L'entree brute peut contenir des millions de controles independants. Pour la
    visualisation, on ne renvoie pas chaque detection : on regroupe par site les
    dates proches, separees par plus de `gap_days`, en segments debut/fin.
    """
    controls = data.controls
    selected_sites = sites or ANTENNA_SITES
    controls = controls.loc[
        controls["LIEU_DIT"].isin(selected_sites),
        ["DATE", "LIEU_DIT", "DEPARTEMENT"],
    ]

    if departements:
        controls = controls[controls["DEPARTEMENT"].astype(str).isin(departements)]
    if date_start:
        controls = controls[controls["DATE"] >= pd.Timestamp(date_start)]
    if date_end:
        controls = controls[controls["DATE"] <= pd.Timestamp(date_end)]

    if controls.empty:
        return []

    visits = _presence_visits(controls, gap_days=gap_days)
    return _aggregate_phenology_by_site(visits)


def get_site_summary(data: CmrData, site: str) -> SiteSummary:
    """Produit une fiche analytique centree sur un seul site antenne."""
    controls = data.controls[data.controls["LIEU_DIT"] == site]
    individus = data.individus[data.individus["LIEU_DIT"] == site]
    distances = data.distances[
        (data.distances["SITE_DEPART"] == site) | (data.distances["SITE_ARRIVEE"] == site)
    ]

    return SiteSummary(
        site=site,
        kpis=_site_kpis(controls, individus, data.sites),
        detections_by_year=_counts_by_year(controls, unique_individuals=False),
        captures_by_year=_counts_by_year(individus, unique_individuals=True),
        controls_by_year=_counts_by_year(controls, unique_individuals=True),
        detected_species=_category_counts(controls, "CODE_ESP"),
        marked_species=_category_counts(individus, "CODE_ESP"),
        daily_frequency=_daily_frequency(controls),
        phenology=get_phenology(data, sites=[site]),
    )


def _aggregate_phenology_by_site(visits: pd.DataFrame) -> list[SitePhenology]:
    """Convertit les visites calculees en modeles Pydantic par site."""
    result = []
    for site, site_visits in visits.groupby("LIEU_DIT", sort=True):
        rows = [
            PhenologySegment(
                start=pd.Timestamp(row["Start"]).date(),
                finish=pd.Timestamp(row["Finish"]).date(),
            )
            for _, row in site_visits.sort_values("Start").iterrows()
        ]
        if rows:
            departement = _optional_str(site_visits["Departement"].dropna().iloc[0]) if site_visits["Departement"].notna().any() else None
            result.append(
                SitePhenology(
                    site=str(site),
                    departement=departement,
                    visits=rows,
                )
            )
    return result


def _valid_studies(df: pd.DataFrame) -> pd.DataFrame:
    """Filtre les donnees aux etudes retenues pour les graphiques descriptifs."""
    if "ETUDE" not in df.columns:
        return df
    return df[df["ETUDE"].isin(VALID_STUDIES)].copy()


def _kpis(controls: pd.DataFrame, individus: pd.DataFrame, sites: pd.DataFrame) -> Kpis:
    """Calcule les indicateurs synthétiques affiches en tete de page."""
    return Kpis(
        total_marked=int(individus["NUM_PIT"].nunique()) if "NUM_PIT" in individus else 0,
        total_recaptured=int(controls.query('ACTION == "C"')["NUM_PIT"].nunique())
        if "ACTION" in controls and "NUM_PIT" in controls
        else 0,
        capture_sites=int(individus["LIEU_DIT"].nunique()) if "LIEU_DIT" in individus else 0,
        antenna_sites=int(sites["LIEU_DIT"].nunique()) if "LIEU_DIT" in sites else 0,
    )


def _site_kpis(controls: pd.DataFrame, individus: pd.DataFrame, sites: pd.DataFrame) -> Kpis:
    """Calcule les KPI d'une fiche site."""
    kpis = _kpis(controls, individus, sites)
    return kpis.model_copy(
        update={
            "local_control_rate": _local_control_rate(controls, individus),
            "follow_up_years": _follow_up_years(controls),
        }
    )


def _local_control_rate(controls: pd.DataFrame, individus: pd.DataFrame) -> float | None:
    """Part des individus equipes sur le site recontroles au moins une fois sur ce meme site."""
    if individus.empty or "NUM_PIT" not in individus or "NUM_PIT" not in controls or "ACTION" not in controls:
        return None

    equipped = _pit_values(individus["NUM_PIT"])
    if not equipped:
        return None

    local_recaptures = controls[controls["ACTION"] == "C"]
    recaptured = _pit_values(local_recaptures["NUM_PIT"])
    return round((len(equipped & recaptured) / len(equipped)) * 100, 1)


def _pit_values(series: pd.Series) -> set[str]:
    return set(series.dropna().astype(str).str.replace(r"\.0$", "", regex=True))


def _follow_up_years(controls: pd.DataFrame) -> int:
    """Nombre d'annees avec au moins un individu controle sur le site."""
    if controls.empty or "DATE" not in controls or "NUM_PIT" not in controls:
        return 0
    scoped = controls.dropna(subset=["DATE", "NUM_PIT"]).copy()
    if scoped.empty:
        return 0
    return int(pd.to_datetime(scoped["DATE"], errors="coerce").dt.year.dropna().nunique())


def _counts_by_year(df: pd.DataFrame, unique_individuals: bool) -> list[YearCount]:
    """Compte par annee et espece.

    `unique_individuals=True` compte les NUM_PIT distincts, utile pour les
    captures/controles d'individus. `False` compte les lignes, utile pour le
    volume brut de detections.
    """
    if df.empty or "DATE" not in df or "CODE_ESP" not in df:
        return []
    scoped = df.copy()
    scoped["YEAR"] = pd.to_datetime(scoped["DATE"], errors="coerce").dt.year
    scoped = scoped.dropna(subset=["YEAR", "CODE_ESP"])
    if unique_individuals and "NUM_PIT" in scoped:
        grouped = scoped.groupby(["YEAR", "CODE_ESP"])["NUM_PIT"].nunique()
    else:
        grouped = scoped.groupby(["YEAR", "CODE_ESP"]).size()
    result = grouped.reset_index(name="count").sort_values(["YEAR", "CODE_ESP"])
    return [
        YearCount(year=int(row["YEAR"]), species=str(row["CODE_ESP"]), count=int(row["count"]))
        for _, row in result.iterrows()
    ]


def _category_counts(df: pd.DataFrame, column: str) -> list[CategoryCount]:
    """Retourne une repartition simple d'une colonne categorielle."""
    if df.empty or column not in df:
        return []
    counts = df[column].dropna().astype(str).value_counts().reset_index()
    return [
        CategoryCount(label=str(row[column]), count=int(row["count"]))
        for _, row in counts.iterrows()
    ]


def _daily_frequency(df: pd.DataFrame) -> list[DailyFrequency]:
    """Agrege les detections par jour de l'annee, toutes annees confondues."""
    if df.empty or "DATE" not in df:
        return []
    scoped = df.copy()
    scoped["MONTH_DAY"] = pd.to_datetime(scoped["DATE"], errors="coerce").dt.strftime("%m-%d")
    counts = scoped.dropna(subset=["MONTH_DAY"]).groupby("MONTH_DAY").size().reset_index(name="count")
    counts = counts.sort_values("MONTH_DAY")
    return [
        DailyFrequency(month_day=str(row["MONTH_DAY"]), count=int(row["count"]))
        for _, row in counts.iterrows()
    ]


def _top_detections(df: pd.DataFrame) -> list[CategoryCount]:
    """Retourne les individus les plus souvent detectes."""
    if df.empty or "NUM_PIT" not in df:
        return []
    counts = df["NUM_PIT"].dropna().astype(str).value_counts().head(10).reset_index()
    return [
        CategoryCount(label=str(row["NUM_PIT"]), count=int(row["count"]))
        for _, row in counts.iterrows()
    ]


def _distances(df: pd.DataFrame) -> list[DistanceValue]:
    """Expose les distances individuelles pour les resumes par espece."""
    if df.empty:
        return []
    scoped = df[["CODE_ESP", "DIST_KM"]].dropna().copy()
    return [
        DistanceValue(species=str(row["CODE_ESP"]), distance_km=round(float(row["DIST_KM"]), 3))
        for _, row in scoped.iterrows()
    ]


def _transitions(df: pd.DataFrame, limit: int = 500) -> list[TransitionRow]:
    """Retourne les trajectoires les plus longues pour la table exploratoire."""
    if df.empty:
        return []
    scoped = df.sort_values("DIST_KM", ascending=False).head(limit)
    return [
        TransitionRow(
            num_pit=str(row["NUM_PIT"]),
            species=_optional_str(row.get("CODE_ESP")),
            date_depart=_optional_datetime(row.get("DATE_DEPART")),
            site_depart=_optional_str(row.get("SITE_DEPART")),
            date_arrivee=_optional_datetime(row.get("DATE_ARRIVEE")),
            site_arrivee=_optional_str(row.get("SITE_ARRIVEE")),
            distance_km=round(float(row["DIST_KM"]), 2),
        )
        for _, row in scoped.iterrows()
    ]


def _presence_visits(controls: pd.DataFrame, gap_days: int = 7) -> pd.DataFrame:
    """Fusionne les detections proches en visites continues.

    Pour chaque site, une nouvelle visite commence lorsqu'une detection est
    separee de la precedente par plus de `gap_days`. Les visites ponctuelles
    d'un seul jour sont ensuite ignorees pour garder une timeline lisible.
    """
    scoped = controls.copy()
    scoped["DATE"] = pd.to_datetime(scoped["DATE"], errors="coerce")
    scoped = scoped.dropna(subset=["DATE", "LIEU_DIT"]).sort_values("DATE")
    scoped["Prev_DATE"] = scoped.groupby("LIEU_DIT")["DATE"].shift(1)
    scoped["New_Visit"] = (scoped["DATE"] - scoped["Prev_DATE"]).dt.days > gap_days
    scoped["New_Visit"] = scoped["New_Visit"].fillna(True)
    scoped["Visit_ID"] = scoped.groupby("LIEU_DIT")["New_Visit"].cumsum()
    result = (
        scoped.groupby(["LIEU_DIT", "Visit_ID"])
        .agg(
            Start=pd.NamedAgg(column="DATE", aggfunc="min"),
            Finish=pd.NamedAgg(column="DATE", aggfunc="max"),
            Departement=pd.NamedAgg(column="DEPARTEMENT", aggfunc="first"),
        )
        .reset_index()
    )
    result = result[result["Finish"] > result["Start"]]
    return result.sort_values(["Departement", "LIEU_DIT", "Start"])


def _optional_str(value: object) -> str | None:
    """Convertit une valeur pandas potentiellement vide en chaine optionnelle."""
    if pd.isna(value):
        return None
    return str(value)


def _optional_datetime(value: object):
    """Convertit une date pandas en datetime optionnel."""
    if pd.isna(value):
        return None
    return pd.Timestamp(value).to_pydatetime()
