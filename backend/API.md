# Documentation API

Cette API FastAPI expose les donnees CMR actuelles au frontend React. Elle lit
aujourd'hui les CSV du dossier `data/`, mais la logique est isolee dans
`app/repositories/` pour permettre un futur branchement SQL.

Base locale en développement séparé :

```text
http://127.0.0.1:8000/api
```

En Docker unique ou sur Hugging Face Spaces, FastAPI sert le frontend compilé
et l'API depuis le même domaine. Le frontend appelle alors :

```text
/api
```

## Conventions

- Les dates sont serialisees en ISO 8601 (`YYYY-MM-DD` ou datetime ISO).
- Les listes vides dans les filtres signifient "pas de filtre".
- Les codes especes utilisent les codes metier des CSV, par exemple `RHIFER`, `MINSCH`, `MYOEMA`.
- Les distances sont exprimees en kilometres.
- Les coordonnees sont en latitude/longitude WGS84.
- Les reponses peuvent etre reutilisees par le cache memoire du frontend quand la meme cle de requete est demandee plusieurs fois.

## Endpoints

| Methode | Chemin | Usage |
| --- | --- | --- |
| `GET` | `/health` | Controle de disponibilite |
| `GET` | `/filters` | Options des formulaires |
| `POST` | `/map/trajectories` | Donnees de la carte des trajectoires |
| `GET` | `/stats/global` | Donnees de l'onglet Statistiques |
| `GET` | `/phenology` | Timeline de presence par site antenne |
| `GET` | `/sites/{site}/summary` | Fiche analytique d'un site |

## `GET /health`

Verifie que l'API repond.

Reponse :

```json
{
  "status": "ok"
}
```

## `GET /filters`

Retourne toutes les options necessaires aux formulaires du frontend.

Exemple de reponse :

```json
{
  "departements": ["16", "17", "24"],
  "departements_antennes": ["16", "17"],
  "communes": ["ANNEPONT", "VERTEUIL-SUR-CHARENTE"],
  "species": ["MINSCH", "RHIFER"],
  "genders": ["F", "M"],
  "ages": ["AD", "JUV"],
  "sites": ["Chateau de Verteuil"],
  "sites_by_commune": {
    "VERTEUIL-SUR-CHARENTE": ["Chateau de Verteuil"]
  },
  "antenna_sites": ["Chateau de Verteuil"],
  "periods": ["Transit", "Parturition", "Hivernale"],
  "date_min": "2016-01-01",
  "date_max": "2025-12-31"
}
```

Champs importants :

- `departements` : departements disponibles dans les controles.
- `departements_antennes` : departements restreints aux sites equipes.
- `sites_by_commune` : index utilise pour filtrer les sites apres selection d'une commune.
- `periods` : periodes metier converties en mois cote backend.

## `POST /map/trajectories`

Retourne les donnees pretes pour la carte Leaflet : trajectoires, sites,
bornes de cadrage et palette d'especes. Les couleurs de departements visibles
dans la legende sont gerees cote frontend dans la table de reference des
departements.

Payload minimal :

```json
{}
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
  "periods": ["Transit", "Parturition"]
}
```

Filtres :

- `departements` : conserve les individus ayant au moins une liaison touchant un departement selectionne.
- `species` : filtre sur `CODE_ESP`.
- `genders` : filtre sur `SEXE`.
- `ages` : filtre sur `AGE`.
- `communes` : traduit les communes en sites, puis conserve les individus lies a ces sites.
- `sites` : conserve les individus lies aux sites selectionnes.
- `date_start` : borne basse sur `DATE_DEPART`.
- `date_end` : borne haute sur `DATE_ARRIVEE`.
- `periods` : converties en mois via `PERIOD_MONTHS`.

Exemple de reponse :

```json
{
  "count": 128,
  "center": {
    "lat": 46.12,
    "lon": 0.42,
    "zoom": 6
  },
  "bounds": {
    "south": 44.9,
    "west": -1.2,
    "north": 47.4,
    "east": 1.3
  },
  "species_colors": {
    "RHIFER": "#2ca02c"
  },
  "trajectories": [
    {
      "id": "123456-0",
      "num_pit": "123456",
      "species": "RHIFER",
      "gender": "M",
      "age": "AD",
      "individual_count": 12,
      "departure": {
        "site": "Site A",
        "departement": "16",
        "date": "2021-04-12T00:00:00",
        "lat": 45.92,
        "lon": 0.25
      },
      "arrival": {
        "site": "Site B",
        "departement": "17",
        "date": "2021-05-03T00:00:00",
        "lat": 46.1,
        "lon": -0.32
      },
      "distance_km": 43.7,
      "color": "#2ca02c"
    }
  ],
  "sites": [
    {
      "site": "Site A",
      "commune": "COMMUNE A",
      "departement": "16",
      "lat": 45.92,
      "lon": 0.25,
      "role": "departure"
    }
  ]
}
```

Notes metier :

- Les trajectoires sont dedoublonnees par `CODE_ESP`, `SITE_DEPART`, `SITE_ARRIVEE`.
- `individual_count` correspond au nombre d'individus distincts ayant realise cette liaison au moins une fois.
- `role` vaut `departure`, `arrival` ou `both` selon la presence du site dans les liaisons filtrees.

## `GET /stats/global`

Retourne tout le payload de l'onglet Statistiques.

Exemple de structure :

```json
{
  "kpis": {
    "total_marked": 1200,
    "total_recaptured": 430,
    "capture_sites": 85,
    "antenna_sites": 34
  },
  "detections_by_year": [
    { "year": 2022, "species": "RHIFER", "count": 1200 }
  ],
  "captures_by_year": [
    { "year": 2022, "species": "RHIFER", "count": 42 }
  ],
  "controls_by_year": [
    { "year": 2022, "species": "RHIFER", "count": 35 }
  ],
  "detected_species": [
    { "label": "RHIFER", "count": 1200 }
  ],
  "marked_species": [
    { "label": "RHIFER", "count": 130 }
  ],
  "daily_frequency": [
    { "month_day": "04-12", "count": 81 }
  ],
  "top_detections": [
    { "label": "123456", "count": 98 }
  ],
  "distances": [
    { "species": "RHIFER", "distance_km": 43.7 }
  ],
  "transitions": [
    {
      "num_pit": "123456",
      "species": "RHIFER",
      "date_depart": "2021-04-12T00:00:00",
      "site_depart": "Site A",
      "date_arrivee": "2021-05-03T00:00:00",
      "site_arrivee": "Site B",
      "distance_km": 43.7
    }
  ]
}
```

Notes :

- `detections_by_year` compte les lignes de detection.
- `captures_by_year` et `controls_by_year` comptent des individus uniques.
- `daily_frequency` agrege par jour du calendrier, toutes annees confondues.
- `transitions` est limite aux trajectoires les plus longues pour alimenter une table exploratoire.

## `GET /phenology`

Retourne les periodes continues de presence par site antenne.

Parametres query :

| Nom | Type | Defaut | Description |
| --- | --- | --- | --- |
| `departements` | `list[str]` | aucun | Filtre les sites par departement |
| `date_start` | `date` | aucun | Date minimale incluse |
| `date_end` | `date` | aucun | Date maximale incluse |
| `gap_days` | `int` | `7` | Nombre de jours maximum entre deux detections pour les fusionner |

Exemple :

```text
GET /api/phenology?departements=16&departements=17&date_start=2020-01-01&gap_days=10
```

Reponse :

```json
[
  {
    "site": "Chateau de Verteuil",
    "departement": "16",
    "visits": [
      {
        "start": "2021-04-12",
        "finish": "2021-04-20"
      }
    ]
  }
]
```

Notes :

- Les detections ponctuelles d'un seul jour sont ignorees pour garder une timeline lisible.
- Le regroupement se fait independamment pour chaque site.

## `GET /sites/{site}/summary`

Retourne les statistiques detaillees pour un site.

Exemple :

```text
GET /api/sites/Chateau%20de%20Verteuil/summary
```

Reponse :

```json
{
  "site": "Chateau de Verteuil",
  "kpis": {
    "total_marked": 42,
    "total_recaptured": 18,
    "capture_sites": 1,
    "antenna_sites": 34
  },
  "detections_by_year": [
    { "year": 2022, "species": "RHIFER", "count": 120 }
  ],
  "captures_by_year": [
    { "year": 2022, "species": "RHIFER", "count": 8 }
  ],
  "controls_by_year": [
    { "year": 2022, "species": "RHIFER", "count": 6 }
  ],
  "detected_species": [
    { "label": "RHIFER", "count": 120 }
  ],
  "marked_species": [
    { "label": "RHIFER", "count": 8 }
  ],
  "daily_frequency": [
    { "month_day": "04-12", "count": 7 }
  ],
  "phenology": [
    {
      "site": "Chateau de Verteuil",
      "departement": "16",
      "visits": [
        { "start": "2021-04-12", "finish": "2021-04-20" }
      ]
    }
  ]
}
```

## Erreurs possibles

FastAPI renvoie automatiquement :

- `422 Unprocessable Entity` si un payload ou parametre ne respecte pas les types attendus.
- `500 Internal Server Error` si les CSV attendus sont absents ou si une colonne obligatoire manque.

En deploiement Docker ou Hugging Face Spaces, un `500` sur `/api/filters`
indique souvent que le dossier `data/` n'a pas ete copie dans l'image ou que
`CCPNA_DATA_DIR` ne pointe pas vers le bon emplacement.

## Fichiers CSV attendus

Le repository CSV attend notamment :

- `df_individus.csv`
- `df_sites.csv`
- `df_distances.csv`
- `df_controls.csv`

Ces fichiers sont lus depuis `Settings.data_dir`, configurable avec la variable
`CCPNA_DATA_DIR`.

Le Dockerfile racine utilise par defaut :

```text
CCPNA_DATA_DIR=/data
```
