"""Configuration runtime du backend."""

from functools import lru_cache
import os
from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    """Parametres applicatifs centralises.

    `CCPNA_DATA_DIR` permet de changer la source des CSV sans modifier le code :
    localement le backend lit `../data`, tandis que Docker monte ce meme dossier
    dans `/data`.
    """

    app_name: str = "CCPNA CMR Dashboard API"
    api_prefix: str = "/api"
    data_dir: Path = Path(os.getenv("CCPNA_DATA_DIR", Path(__file__).resolve().parents[3] / "data"))


@lru_cache
def get_settings() -> Settings:
    """Instancie une seule fois la configuration pour tout le processus."""
    return Settings()
