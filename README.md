# Tableau de bords d'analyse des données de CMR des chauves-souris

## Présentation

Le projet CCPNA, mené par France Nature Environnement Nouvelle-Aquitaine depuis 2016, vise à étudier diverses espèces de chauves-souris selon quatre axes : génétique, écotoxicologie, épidémiologie et déplacements. Il utilise des méthodes telles que la génétique pour définir les populations, l'écotoxicologie pour identifier les polluants, l'épidémiologie pour comprendre la circulation des virus, et le suivi des déplacements via des puces sous-cutanées. De nombreux sites équipés d'antennes automatiques permettent de collecter une très grande quantité données sur le passage des individus marqués. Un tableau de bord interactif permet aux associations d’explorer les données pour leur prise de décision.

Porté par France Nature Environnement Nouvelle-Aquitaine, le projet [Chiroptères Cavernicoles Prioritaires de Nouvelle-Aquitaine](https://vimeo.com/435059221/7a3f18d6ba) (CCPNA) est un programme à large échelle démarré en 2016 dans l’objectif d’étudier plusieurs espèces de chauves-souris afin d’aborder quatre thématiques : 

- **La génétique**, afin de définir les contours des populations et mettre en évidence d’éventuelles frein aux échanges génétiques ;
- L’**écotoxicologie,** pour tenter d’aborder à quels polluants les espèces peuvent être exposées ;
- L’**épidémiologie**, ou l’étude de la circulation des
virus, permet de mettre en lumière d’éventuels risques d’exposition pour ces dernières comme de comprendre des mécanismes de circulation couplés au paysage ou à leurs mœurs ;
- **Les déplacements**, avec la pose de puces sous cutanées, RFID ou Pit-tag, inertes avec un identifiant unique chez les Grands Rhinolophes, Murin à oreilles échancrées et le Minioptère de
Schreibers. Les contrôles d’individus marqués permettent de retracer leurs déplacements. À terme, ces données pourraient permettre d’établir des taux de survie et de comprendre comment les individus utilisent les différents connus au cours de leur vie.

## Organisation du répértoire

Ce répertoire suit une hiérarchie classique et facile à explorer. Les données étant volumineuses, elles ne sont pas disponibles sur ce repo.

```shell
dashboard-bat-CMR/
├── .vscode/            
|
├── assets/                 # Scripts de customisation visuelle
├── data/                   # Données brutes et traitées
├── images/                 # Images utilisées sur l'application
├── notebooks/              # Notebooks de test et d'expérimentation
├── pages/                  # Pages de l'application Taipy
├── plots/                  # Figures fixes
├── streamlit_old/          # Ancien prototype Streamlit (old)
|
├── custom_functions.py     # Fonctions additionnelles
├── main.py                 # Script de l'application Taipy
|
├── dockerfile              # Fichier docker pour containeurisation
├── requirements.txt        # Liste des packages nécessaires pour le projet
|
├── .dockerignore
├── .gitignore
└── README.md               # Lisez-moi
```

## Installation

Dans un premier temps, clonez le dépôt sur votre machine locale via votre méthode préférée ou en utilisant la commande suivante :

```shell
git clone https://github.com/a-langlais/dashboard-bat-CMR.git
```

Ensuite, deux solutions s'offrent à vous si vous souhaitez relancer ce projet dans les mêmes conditions que lorsqu'il a été conçu.

Vous pouvez créer un environnement virtuel en téléchargeant spécifiquement les dépéndances Python nécessaires via le fichier `requirements.txt`.

```shell
pip install -r requirements.txt
```

Si vous utilisez Conda, vous pouvez tout simplement recréer un environnement en utiliser le fichier `environment.yml`.

```shell
conda env create -f environment.yml
conda activate environment
```

## Taipy app

L'application Taipy est constituée de quatre onglets :
- **Présentation** : afin de présenter le programme dans sa globalité
- **Antennes** : permet de filtrer les données pour afficher une carte des trajectoires empruntées par les individus marqués.
- **Phénologie** : permet de visualiser les données temporelles phénologiques de présence des individus marqués sur les différents sites étudiés.
- **Statistiques** : tableau de bord des différentes métriques statistiques, principalement descriptives, du projet.

Pour lancer l'application Taipy :

```shell
conda create --name ccpna_dashboard python=3.11.9
conda activate ccpna_dashboard
pip install -r requirements.txt
python run main.py
```

L'application devrait être disponible à [localhost:5000](http://localhost:5000).