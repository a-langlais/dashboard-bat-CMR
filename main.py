from taipy import Gui
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm

from functions import *
from dashboard import *

# CHARGEMENT DES DONNEES
df_controls, df_individus, df_sites, df_distances, df_mapping = load_data_antenna()
liste_sites_antennes = sorted(["Brelouze", "Mairie d'Annepont", "Grottes de Loubeau", "Le Plessis", "Puy-Chenin", "Cézelle", "La Bourtière", "Goizet (W)", "Château de Gagemont", "Faye-L'Abbesse - Bourg", "Guibaud", "Cave Billard", "Grotte de Boisdichon", "Les Roches", "Barrage de l'Aigle", "Gouffre de la Fage",
                  "Ancienne citerne à eau", "Château de Verteuil", "Les Dames", "Château de Hautefort", "Les Tours de Merle - Tour Fulcon", "Le Petit Pin", "Maison Brousse", "Caves de Laubenheimer", "Château de Villandraut", "Tunnel ferroviaire", "Grotte de la carrière", "Centrale hydroélectrique de Claredent", "Fermette des Nobis",
                  "Beauregard", "Grotte de la Deveze", "Petexaenea (Site générique Galeries N&S)", "Gouffre de Bexanka", "Mikelauenziloa"])
ETUDE_valides = ["Diag CEN", "Diag NATURA 2000", "Diag FDS_Oléron", "ECOFECT (GR/CCPNA)", "ECOFECT (Hors GR)", "TRANSPY ESPAGNE", "TRANSPY FRANCE"]

# Initialisation des variables d'état
selected_dpt = []
selected_dpt_gant = []
selected_sp = []
selected_gender = []
selected_sites = []
selected_communes = []
selected_dates = [df_controls['DATE'].min(), df_controls['DATE'].max()]
dates_gant = [df_controls['DATE'].min(), df_controls['DATE'].max()]
df_empty = pd.DataFrame()

# CONTENU
## ROOT PAGE
FEDER = "images/FEDER-NA.png"
PREFET = "images/Prefet_NA.jpg"
VERT = "images/FranceNationVerte.jpg"

with open("pages/home.md", "r", encoding = "utf-8") as file:
    root_md = file.read()

## PAGE DE PRESENTATION
with open("pages/page1.md", "r", encoding = "utf-8") as file:
    page1 = file.read()

## VISUALISATION DES DONNEES D'ANTENNES
communes = sorted(df_controls['COMMUNE'].unique().tolist())
departements = sorted(df_controls['DEPARTEMENT'].unique().tolist())
species = sorted(df_distances['CODE_ESP'].unique().tolist())
genders = sorted(df_individus['SEXE'].dropna().unique().tolist())
sites = sorted(df_controls['LIEU_DIT'].dropna().unique().tolist())
dates = [df_controls['DATE'].min(), df_controls['DATE'].max()]

# Callback du sélécteur de sites
def refresh_sites(state):
    selected_communes = state.selected_communes or []
    
    if selected_communes:
        filtered_df = df_controls[df_controls['COMMUNE'].isin(selected_communes)]
    else:
        filtered_df = df_controls

    state.sites = sorted(filtered_df['LIEU_DIT'].unique().tolist())

m = generate_map(df_empty, df_sites)

with open("pages/page2.md", "r", encoding = "utf-8") as file:
    page2 = file.read()

# Callback de la carte
def refresh_map_button(state):
    df_filtered = df_distances.copy()
    
    # Filtrer par département d'origine
    if state.selected_dpt:
        equipped_pit = df_filtered[(df_filtered['DPT_DEPART'].isin(state.selected_dpt)) | (df_filtered['DPT_ARRIVEE'].isin(state.selected_dpt))]['NUM_PIT'].unique()
        df_filtered = df_filtered[df_filtered['NUM_PIT'].isin(equipped_pit)]
    
    # Filtrer par espèce
    if state.selected_sp:
        df_filtered = df_filtered[df_filtered['CODE_ESP'].isin(state.selected_sp)]

    # Filtrer par genre
    if state.selected_gender:
        df_filtered = df_filtered[df_filtered['SEXE'].isin(state.selected_gender)]

    # Filtrer par site d'origine
    if state.selected_sites:
        site_pit = df_filtered[(df_filtered['SITE_DEPART'].isin(state.selected_sites)) | (df_filtered['SITE_ARRIVEE'].isin(state.selected_sites))]['NUM_PIT'].unique()        
        df_filtered = df_filtered[df_filtered['NUM_PIT'].isin(site_pit)]
    
    # Filtrer par intervalle de dates
    if state.selected_dates and len(state.selected_dates) == 2:
        start_date = pd.Timestamp(state.selected_dates[0])
        end_date = pd.Timestamp(state.selected_dates[1])
        df_filtered = df_filtered[(df_filtered['DATE_DEPART'] >= start_date) & (df_filtered['DATE_ARRIVEE'] <= end_date)]
    
    # Rafraichir la carte
    state.m = generate_map(df_filtered, df_sites)

## PHENOLOGIES DES SITES
gant_global = gant_diagram(df_controls)

with open("pages/page3.md", "r", encoding = "utf-8") as file:
    page3 = file.read()

# Callbacks du diagramme de Gant
def update_gant(state):
    df_filtered_gant = df_controls.copy()
    df_filtered_gant = df_filtered_gant[df_filtered_gant['LIEU_DIT'].isin(liste_sites_antennes)]

    # Convertir les dates sélectionnées en objets Timestamp
    if state.selected_dpt_gant:
        df_filtered_gant = df_filtered_gant[df_filtered_gant['DEPARTEMENT'].isin(state.selected_dpt_gant)]

    if state.dates_gant and len(state.dates_gant) == 2:
        start_date = pd.Timestamp(state.dates_gant[0])
        end_date = pd.Timestamp(state.dates_gant[1])

        # Filtrer les dates
        df_filtered_gant = df_filtered_gant[(df_filtered_gant['DATE'] >= start_date) & (df_filtered_gant['DATE'] <= end_date)]

    state.gant_global = gant_diagram(df_filtered_gant)

## STATISTIQUES ANALYTIQUES
# Initialisation de tous les plots
df_controls_valide = df_controls[df_controls['ETUDE'].isin(ETUDE_valides)]
df_individus_valide = df_individus[df_individus['ETUDE'].isin(ETUDE_valides)]

plot_detection_year = detection_by_year(df_controls_valide)      # Barplot du nombre de détections par an et par espèce
plot_capture_year = capture_by_year(df_individus_valide)         # Barplot du nombre de captures par an et par espèces
plot_control_year = control_by_year(df_controls_valide)          # Barplot du nombre de contrôles par an et par espèces
plot_frequencies = detection_frequencies(df_controls_valide)     # Courbes de fréquences de détections par jour de l'année et par site
plot_pie_controled = pie_controled(df_controls_valide)           # Pieplot des individus contrôlés
plot_pie_marked = pie_marked(df_individus_valide)                # Pieplot des individus marqués
plot_top_detection = top_detection(df_controls_valide)           # Barplot horizontal des 10 individus les plus détectés
plot_box_distances = distance_boxplot(df_distances)              # Boxplot des distances par espèce

# Initialisation des variables à plot
total_recaptured = df_controls.query('ACTION == "C"')['NUM_PIT'].nunique()       # Individus contrôlés
total_marked = df_individus['NUM_PIT'].nunique()                                 # Individus marqués
sites_capture = df_individus['LIEU_DIT'].nunique()                               # Sites capturés au moins une fois
sites_antennes = df_sites['LIEU_DIT'].nunique()                                  # Sites contrôlés au moins une fois
transition_table_plot = df_distances[['NUM_PIT', 'CODE_ESP', 'DATE_DEPART', 'SITE_DEPART', 'DATE_ARRIVEE', 'SITE_ARRIVEE', 'DIST_KM']].sort_values(by='DIST_KM', ascending = False)
transition_table_plot['DIST_KM'] = transition_table_plot['DIST_KM'].round(2)

with open("pages/page4.md", "r", encoding = "utf-8") as file:
    page4 = file.read()

## FICHE SITE
# Initialisation du sélecteur et des plots
selection_fiche = ['Ancienne citerne à eau']
df_controls_fiche = df_controls[df_controls['LIEU_DIT'].isin(selection_fiche)]
df_individus_fiche = df_individus[df_individus['LIEU_DIT'].isin(selection_fiche)]
df_distances_fiche = df_distances[(df_distances['SITE_DEPART'].isin(selection_fiche)) | (df_distances['SITE_ARRIVEE'].isin(selection_fiche))]

plot_detection_year_fiche = detection_by_year(df_controls_fiche)      # Barplot du nombre de détections par an et par espèce
plot_capture_year_fiche = capture_by_year(df_individus_fiche)         # Barplot du nombre de captures par an et par espèces
plot_control_year_fiche = control_by_year(df_controls_fiche)          # Barplot du nombre de contrôles par an et par espèces
plot_frequencies_fiche = detection_frequencies(df_controls_fiche)     # Courbes de fréquences de détections par jour de l'année et par site
plot_pie_controled_fiche = pie_controled(df_controls_fiche)           # Pieplot des individus contrôlés
plot_pie_marked_fiche = pie_marked(df_individus_fiche)                # Pieplot des individus marqués

# Initialisation des variables à plot
total_recaptured_fiche = df_controls_fiche['NUM_PIT'].nunique()       # Individus contrôlés
total_marked_fiche = df_individus_fiche['NUM_PIT'].nunique()          # Individus marqués
sites_antennes_fiche = df_sites['LIEU_DIT'].nunique()                 # Sites contrôlés au moins une fois
map_fiche = generate_map(df_distances_fiche, df_sites)                # Map du site et des connexions
gant_diagram_fiche = gant_diagram_concat(df_controls_fiche)

def update_fiche(state):
    # Filtrage en fonction de la sélection
    selected_sites = [state.selection_fiche]
    df_controls_fiche = df_controls[df_controls['LIEU_DIT'].isin(selected_sites)]
    df_individus_fiche = df_individus[df_individus['LIEU_DIT'].isin(selected_sites)]
    df_distances_fiche = df_distances[(df_distances['SITE_DEPART'].isin(selected_sites)) | (df_distances['SITE_ARRIVEE'].isin(selected_sites))]
    
    # Mise à jour des visualisations
    state.plot_detection_year_fiche = detection_by_year(df_controls_fiche)
    state.plot_capture_year_fiche = capture_by_year(df_individus_fiche)
    state.plot_control_year_fiche = control_by_year(df_controls_fiche)
    state.plot_frequencies_fiche = detection_frequencies(df_controls_fiche)
    state.plot_pie_controled_fiche = pie_controled(df_controls_fiche)
    state.plot_pie_marked_fiche = pie_marked(df_individus_fiche)
    state.map_fiche = generate_map(df_distances_fiche, df_sites)
    state.gant_diagram_fiche = gant_diagram_concat(df_controls_fiche)
    
    # Mise à jour des variables globales
    state.total_recaptured_fiche = df_controls_fiche['NUM_PIT'].nunique()
    state.total_marked_fiche = df_individus_fiche['NUM_PIT'].nunique()
    state.sites_antennes_fiche = df_sites['LIEU_DIT'].nunique()

with open("pages/page5.md", "r", encoding = "utf-8") as file:
    page5 = file.read()

# DEMARRAGE DE L'APPLICATION
pages = {
    "/": root_md,
    # "presentation": page1,
    "antennes": page2,
    "phenologie": page3,
    "statistiques": page4,
    "fiche_site": page5
}

Gui.register_content_provider(Map, expose_folium)
gui = Gui(pages = pages, css_file = "assets/styles.css")
gui.run(host = '0.0.0.0', port = 5000, use_session = True, dark_mode = False, stylekit = False)