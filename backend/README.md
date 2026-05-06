# Backend FastAPI

Ce dossier contient le backend Python de l'application CMR CCPNA. Il expose les donnees CSV actuelles via FastAPI et isole l'acces aux donnees pour faciliter un futur branchement SQL.

## Installation

Depuis la racine du projet :

```powershell
cd backend
python -m pip install -e .
```

## Lancement

```powershell
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

La documentation interactive est disponible sur :

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Endpoints disponibles

Une documentation exhaustive des payloads, parametres et reponses est disponible dans [`API.md`](API.md).

### `GET /api/health`

Verifie que l'API repond.

### `GET /api/filters`

Expose les options de filtres issues des CSV actuels :

- departements
- communes
- especes
- sexes
- ages
- sites
- sites equipes d'antennes
- periodes
- bornes temporelles

### `POST /api/map/trajectories`

Retourne les trajectoires cartographiques pretes a afficher dans un frontend JavaScript.

Payload minimal :

```json
{
  "species": ["RHIFER"],
  "periods": ["Transit"]
}
```

Payload complet :

```json
{
  "departements": ["16", "17"],
  "species": ["RHIFER"],
  "genders": ["M"],
  "ages": ["AD"],
  "communes": ["VERTEUIL-SUR-CHARENTE"],
  "sites": ["Chateau de Verteuil"],
  "date_start": "2018-01-01",
  "date_end": "2024-12-31",
  "periods": ["Transit", "Parturition", "Hivernale"]
}
```

La reponse contient :

- `center` et `bounds` pour cadrer la carte
- `species_colors` pour harmoniser les couleurs cote frontend
- `trajectories` pour tracer les lignes
- `sites` pour afficher les marqueurs

### `GET /api/stats/global`

Retourne les KPI, séries temporelles, répartitions par espèces, distances et table des trajectoires.

### `GET /api/phenology`

Retourne les périodes de présence des sites équipés, avec filtres optionnels `departements`, `date_start` et `date_end`.

### `GET /api/sites/{site}/summary`

Retourne les KPI et séries d'une fiche site.

## Organisation

```text
backend/
|-- app/
|   |-- api/             # Routes FastAPI
|   |-- core/            # Configuration et constantes metier
|   |-- repositories/    # Acces aux donnees CSV, futur point de remplacement SQL
|   |-- schemas/         # Contrats Pydantic exposes a l'API
|   `-- services/        # Logique metier de filtres et trajectoires
`-- pyproject.toml
```
