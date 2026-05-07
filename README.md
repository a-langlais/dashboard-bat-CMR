# Dashboard CMR CCPNA

Application web pour explorer les données CMR du programme CCPNA : carte interactive des trajectoires, phénologie, statistiques globales et fiches sites.

Le projet a été refondu depuis l'ancienne application Taipy vers une architecture React/Vite + FastAPI. Le backend lit actuellement des CSV, tout en isolant cette lecture dans une couche `repositories` pour faciliter un futur passage vers SQL ou une autre source de données.

## Fonctionnalités

- Page d'accueil avec les financeurs, coordinations et partenaires du programme.
- Onglet Antennes avec carte Leaflet, filtres détaillés, légende repliable, export PNG de la carte et export GeoJSON des trajectoires affichées.
- Onglet Phénologie avec filtres par département et plage de dates.
- Onglet Statistiques avec KPI, graphiques Recharts, distributions, fréquences et table exploratoire des trajectoires.
- Onglet Fiche site avec synthèse ciblée par site équipé.
- Cache frontend en mémoire pour éviter de recalculer les mêmes onglets à chaque retour de navigation.

## Structure

```text
dashboard-bat-CMR/
|-- backend/        # API FastAPI, services métier, schémas Pydantic, lecture CSV
|-- frontend/       # Application React + Vite
|-- data/           # CSV utilisés par l'API
|-- Dockerfile      # Image Docker unique pour frontend + backend
|-- docker-compose.yml
`-- README.md
```

## Données

Le backend attend les fichiers suivants dans le dossier configuré par `CCPNA_DATA_DIR` :

```text
df_individus.csv
df_sites.csv
df_distances.csv
df_controls.csv
```

En Docker, `CCPNA_DATA_DIR` vaut `/data` et le Dockerfile racine copie le dossier local `data/` vers `/data`.

Le fichier `df_mapping_regions.csv` peut être conservé dans `data/` comme table de référence métier, mais l'application utilise aujourd'hui une table frontend centralisée pour les libellés et couleurs de départements.

## Lancement Local

Installer et lancer le backend :

```powershell
cd backend
python -m pip install -e .
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Installer et lancer le frontend :

```powershell
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

Application locale :

```text
http://127.0.0.1:5173/
```

API locale :

```text
http://127.0.0.1:8000/api
```

Documentation interactive :

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```

## Docker

### Image unique

Le Dockerfile racine construit le frontend, installe le backend, copie les CSV dans `/data`, puis lance FastAPI. FastAPI sert à la fois l'API `/api` et le frontend compilé.

```powershell
docker build -t dashboard-cmr-ccpna .
docker run --rm -p 8000:8000 dashboard-cmr-ccpna
```

Application :

```text
http://127.0.0.1:8000/
```

API :

```text
http://127.0.0.1:8000/api
```

### Docker Compose

Le `docker-compose.yml` historique lance deux conteneurs séparés : backend FastAPI et frontend Nginx.

```powershell
docker compose up --build
```

Services :

```text
frontend : http://127.0.0.1:5173/
backend  : http://127.0.0.1:8000/docs
```

## Déploiement Hugging Face Spaces

Le repo est compatible avec un Space Docker grâce au bloc YAML en tête de ce README.

Paramètres attendus :

```text
SDK: Docker
App port: 8000
Dockerfile: ./Dockerfile
```

Le Space doit contenir le dossier `data/` au moment du build si l'on veut embarquer les CSV dans l'image.

## Variables D'environnement

Backend :

```text
CCPNA_DATA_DIR=/data
FRONTEND_DIST_DIR=/app/frontend_dist
```

Frontend :

```text
VITE_API_BASE_URL=/api
```

En déploiement Docker unique, `VITE_API_BASE_URL=/api` suffit car FastAPI sert le frontend et l'API depuis le même domaine.

## API

Endpoints principaux :

- `GET /api/health`
- `GET /api/filters`
- `POST /api/map/trajectories`
- `GET /api/stats/global`
- `GET /api/phenology`
- `GET /api/sites/{site}/summary`

La documentation détaillée des contrats est disponible dans [backend/API.md](backend/API.md).
