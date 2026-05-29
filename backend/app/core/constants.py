# Sites actuellement consideres comme equipes d'antennes. Cette liste provient
# du cadrage metier historique et sert aux filtres "antennes" et a la phenologie.
ANTENNA_SITES = sorted(
    [
        "Brelouze",
        "Mairie d'Annepont",
        "Grottes de Loubeau",
        "Le Plessis",
        "Puy-Chenin",
        "Cézelle",
        "La Bourtière",
        "Goizet (W)",
        "Château de Gagemont",
        "Faye-L'Abbesse - Bourg",
        "Guibaud",
        "Cave Billard",
        "Grotte de Boisdichon",
        "Les Roches",
        "Barrage de l'Aigle",
        "Gouffre de la Fage",
        "Ancienne citerne à eau",
        "Château de Verteuil",
        "Grotte de Rancogne",
        "Les Dames",
        "Château de Hautefort",
        "Les Tours de Merle - Tour Fulcon",
        "Le Petit Pin",
        "Maison Brousse",
        "Caves de Laubenheimer",
        "Château de Villandraut",
        "Tunnel ferroviaire",
        "Grotte de la carrière",
        "Centrale hydroélectrique de Claredent",
        "Fermette des Nobis",
        "Beauregard",
        "Grotte de la Deveze",
        "Petexaenea (Site générique Galeries N&S)",
        "Gouffre de Bexanka",
        "Mikelauenziloa",
    ]
)

# Definition metier des saisons utilisees par les filtres de trajectoires.
PERIOD_MONTHS = {
    "Transit": [3, 4, 5, 9, 10, 11],
    "Parturition": [6, 7, 8],
    "Hivernale": [12, 1, 2],
}

# Palette stable partagee avec le frontend pour garder une couleur constante
# par espece, quel que soit le graphique ou la carte.
SPECIES_COLORS = {
    "MINSCH": "#1f77b4",
    "RHIFER": "#2ca02c",
    "MYOEMA": "#d62728",
    "RHIEUR": "#9467bd",
    "MYONAT": "#ff7f0e",
    "MYODAU": "#8c564b",
}
