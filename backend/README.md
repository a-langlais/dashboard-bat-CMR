# Backend FastAPI

Ce dossier contient l'API Python du dashboard CMR CCPNA. Elle expose les données CSV au frontend React et regroupe la logique métier de filtres, trajectoires, statistiques, phénologie et fiches sites.

## Rôle

- Charger les CSV depuis `CCPNA_DATA_DIR`.
- Normaliser les dates et enrichir les tables nécessaires aux calculs.
- Exposer des endpoints JSON sous le préfixe `/api`.
- Servir le frontend compilé lorsque `FRONTEND_DIST_DIR` pointe vers un build Vite disponible.

## Installation Locale

Depuis la racine du projet :

```powershell
cd backend
python -m pip install -e .
```

## Lancement Local

```powershell
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Documentation interactive :

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```

## Configuration

Variables prises en compte :

```text
CCPNA_DATA_DIR      # dossier contenant les CSV, par défaut ../data en local
FRONTEND_DIST_DIR   # dossier du frontend compilé, par défaut ../frontend/dist
```

En Docker racine, ces variables valent :

```text
CCPNA_DATA_DIR=/data
FRONTEND_DIST_DIR=/app/frontend_dist
```

## CSV Attendus

```text
df_individus.csv
df_sites.csv
df_distances.csv
df_controls.csv
```

Le backend charge ces fichiers une seule fois par processus grâce à un cache `lru_cache`. Les réponses API peuvent ensuite être mises en cache côté frontend pour éviter de rappeler les mêmes endpoints lors des changements d'onglets.

## Endpoints

Une documentation exhaustive des payloads, paramètres et réponses est disponible dans [API.md](API.md).

- `GET /api/health`
- `GET /api/filters`
- `POST /api/map/trajectories`
- `GET /api/stats/global`
- `GET /api/phenology`
- `GET /api/sites/{site}/summary`

## Organisation

```text
backend/
|-- app/
|   |-- api/             # Routes FastAPI
|   |-- core/            # Configuration et constantes métier
|   |-- repositories/    # Accès aux CSV
|   |-- schemas/         # Contrats Pydantic
|   `-- services/        # Logique métier
|-- Dockerfile           # Image backend seule, conservée pour usage séparé
|-- pyproject.toml
`-- README.md
```
