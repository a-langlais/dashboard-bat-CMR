# Dashboard CMR CCPNA

Application web pour explorer les donnees CMR du programme CCPNA : statistiques, phenologie, fiches sites et carte interactive des trajectoires.

Le projet a ete nettoye de l'ancienne application Taipy. La structure cible est maintenant :

```text
bat_CMR_dashboard_rework/
|-- backend/       # API FastAPI, lecture CSV aujourd'hui, futur branchement SQL
|-- frontend/      # Application React + Vite
|-- data/          # Donnees CSV locales, ignorees si volumineuses
`-- README.md
```

## Backend

Installation depuis la racine :

```powershell
cd backend
python -m pip install -e .
```

Lancement :

```powershell
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Endpoints principaux :

- `GET /api/health`
- `GET /api/filters`
- `POST /api/map/trajectories`
- `GET /api/stats/global`
- `GET /api/phenology`
- `GET /api/sites/{site}/summary`

Documentation detaillee des contrats API :

- [backend/API.md](backend/API.md)

Documentation interactive :

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Frontend

Installation :

```powershell
cd frontend
npm install
```

Lancement :

```powershell
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

Application :

- http://127.0.0.1:5173/

## Docker

L'application peut etre lancee avec Docker Compose. Le frontend est servi par Nginx sur le port `5173`, avec un proxy `/api` vers le backend FastAPI.

```powershell
docker compose up --build
```

Services :

- frontend : http://127.0.0.1:5173/
- backend : http://127.0.0.1:8000/docs

Le dossier `data/` est monte en lecture seule dans le conteneur backend sur `/data`.

## Donnees

Les CSV actuels restent dans `data/`. Le backend encapsule leur lecture dans `backend/app/repositories/`, ce qui permettra de remplacer progressivement cette couche par des extractions SQL sans modifier le frontend.
