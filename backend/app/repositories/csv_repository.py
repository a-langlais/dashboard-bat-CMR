"""Repository CSV du backend CMR.

Ce module est le seul endroit qui connait les fichiers CSV et leur structure
physique. Les services consomment ensuite un objet `CmrData`, ce qui rend le
futur remplacement par une couche SQL beaucoup plus simple : il suffira de
fournir les memes DataFrames ou des objets equivalents.
"""

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import pandas as pd

from app.core.config import get_settings


@dataclass(frozen=True)
class CmrData:
    """Jeu de donnees charge en memoire et partage par les services.

    Les DataFrames sont consideres comme des donnees sources. Les services qui
    les filtrent font leurs propres copies quand ils ajoutent des colonnes
    techniques, afin d'eviter les effets de bord entre endpoints.
    """

    controls: pd.DataFrame
    individus: pd.DataFrame
    sites: pd.DataFrame
    distances: pd.DataFrame
    mapping: pd.DataFrame


def _read_csv(path: Path, usecols: list[str] | None = None) -> pd.DataFrame:
    """Lit un CSV en ne chargeant que les colonnes utiles a l'application."""
    return pd.read_csv(path, usecols=usecols, low_memory=False)


def _load_data(data_dir: Path) -> CmrData:
    """Charge et normalise les CSV utilises par l'API.

    Les `usecols` sont volontairement explicites pour limiter l'empreinte
    memoire, notamment sur les controles. Les conversions de dates et les
    enrichissements sexe/age sont faits ici pour que les services travaillent
    sur des colonnes deja coherentes.
    """
    individus = _read_csv(
        data_dir / "df_individus.csv",
        usecols=["DATE", "COMMUNE", "LIEU_DIT", "CODE_ESP", "SEXE", "AGE", "NUM_PIT", "ETUDE"],
    )
    sites = _read_csv(
        data_dir / "df_sites.csv",
        usecols=["COMMUNE", "LIEU_DIT", "DEPARTEMENT", "LAT_WGS", "LONG_WGS"],
    )
    distances = _read_csv(
        data_dir / "df_distances.csv",
        usecols=[
            "NUM_PIT",
            "CODE_ESP",
            "DATE_DEPART",
            "SITE_DEPART",
            "DPT_DEPART",
            "LAT_DEPART",
            "LONG_DEPART",
            "DATE_ARRIVEE",
            "SITE_ARRIVEE",
            "DPT_ARRIVEE",
            "LAT_ARRIVEE",
            "LONG_ARRIVEE",
            "DIST_KM",
        ],
    )
    controls = _read_csv(
        data_dir / "df_controls.csv",
        usecols=["DATE", "COMMUNE", "LIEU_DIT", "DEPARTEMENT", "CODE_ESP", "ACTION", "NUM_PIT", "ETUDE"],
    )
    mapping = pd.DataFrame()

    # Les dates invalides deviennent NaT ; les filtres en aval peuvent ainsi
    # s'appuyer sur pandas sans gerer chaque format d'erreur manuellement.
    controls["DATE"] = pd.to_datetime(controls["DATE"], errors="coerce")
    individus["DATE"] = pd.to_datetime(individus["DATE"], errors="coerce")
    distances["DATE_DEPART"] = pd.to_datetime(distances["DATE_DEPART"], errors="coerce")
    distances["DATE_ARRIVEE"] = pd.to_datetime(distances["DATE_ARRIVEE"], errors="coerce")

    # Les controles ne contiennent pas toujours le sexe. Quand il est absent ou
    # vide, on le rattache depuis la table individus par NUM_PIT.
    if "SEXE" not in controls.columns or controls["SEXE"].isna().all():
        controls = controls.drop(columns=["SEXE"], errors="ignore")
        controls = controls.merge(
            individus[["NUM_PIT", "SEXE"]].drop_duplicates("NUM_PIT"),
            on="NUM_PIT",
            how="left",
        )

    # Les distances sont le socle des trajectoires cartographiques ; on y ajoute
    # les attributs individuels necessaires aux filtres sans alourdir le frontend.
    distances = distances.merge(
        individus[["NUM_PIT", "SEXE", "AGE"]].drop_duplicates("NUM_PIT"),
        on="NUM_PIT",
        how="left",
    )

    # On garde seulement les trajectoires exploitables sur une carte et on
    # dedoublonne par individu/espece/liaison. Le comptage multi-individus est
    # fait plus tard avant l'agregation cartographique.
    distances = (
        distances.dropna(
            subset=["LAT_DEPART", "LONG_DEPART", "LAT_ARRIVEE", "LONG_ARRIVEE"]
        )
        .drop_duplicates(
            subset=["NUM_PIT", "CODE_ESP", "SITE_DEPART", "SITE_ARRIVEE"],
            keep="last",
        )
        .query("DIST_KM > 0")
    )

    return CmrData(
        controls=controls,
        individus=individus,
        sites=sites,
        distances=distances,
        mapping=mapping,
    )


@lru_cache
def get_cmr_data() -> CmrData:
    """Charge les CSV une seule fois par processus FastAPI.

    Ce cache evite de relire plusieurs millions de lignes a chaque requete.
    Pour forcer un rechargement en developpement, redemarrer le serveur suffit.
    """
    return _load_data(get_settings().data_dir)
