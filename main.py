from taipy import Gui
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# CHARGEMENT DES DONNEES

def load_data_antenna():
    df_antenna = pd.read_csv(r'data/df_clean.csv', engine = "pyarrow", dtype_backend = "pyarrow")
    df_antenna['DATE'] = df_antenna['DATE'].astype('datetime64[ns]')
    df_antenna['HEURE'] = pd.to_datetime(df_antenna['HEURE'], format = '%H:%M:%S').dt.time
    df_antenna['ANNEE'] = df_antenna['ANNEE'].astype('int')
    df_antenna['COMMUNE'] = df_antenna['COMMUNE'].astype('str')
    df_antenna['LIEU_DIT'] = df_antenna['LIEU_DIT'].astype('str')
    df_antenna['PRECISION_MILIEU'] = df_antenna['PRECISION_MILIEU'].astype('str')
    df_antenna['DEPARTEMENT'] = df_antenna['DEPARTEMENT'].astype('str')
    df_antenna['CODE_ESP'] = df_antenna['CODE_ESP'].astype('str')
    df_antenna['MASSE'] = df_antenna['MASSE'].astype('str')
    df_antenna['AB'] = df_antenna['AB'].astype('str')
    df_antenna['SEXE'] = df_antenna['SEXE'].astype('str')
    df_antenna['ACTION'] = df_antenna['ACTION'].astype('str')
    df_antenna['ID_PIT'] = df_antenna['ID_PIT'].astype('str')
    df_antenna['NUM_PIT'] = df_antenna['NUM_PIT'].astype('str')
    df_antenna['LONG_L93'] = df_antenna['LONG_L93'].astype('float')
    df_antenna['LAT_L93'] = df_antenna['LAT_L93'].astype('float')
    df_antenna['LONG_WGS'] = df_antenna['LONG_WGS'].astype('float')
    df_antenna['LAT_WGS'] = df_antenna['LAT_WGS'].astype('float')
    return df_antenna

df_antenna = load_data_antenna()
df_empty = pd.DataFrame()

# Initialisation des variables d'état
selected_dpt = []
selected_dpt_gant = []
selected_sp = []
selected_gender = []
selected_sites = []
selected_dates = [df_antenna['DATE'].min(), df_antenna['DATE'].max()]
filtered_df = df_antenna.copy()
dates_gant = [df_antenna['DATE'].min(), df_antenna['DATE'].max()]

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
departements = sorted(df_antenna['DEPARTEMENT'].unique().tolist())
species = sorted(df_antenna['CODE_ESP'].unique().tolist())
genders = sorted(df_antenna['SEXE'].unique().tolist())
sites = sorted(df_antenna['LIEU_DIT'].unique().tolist())
dates = [df_antenna['DATE'].min(), df_antenna['DATE'].max()]

def create_trajectories_map(df, width = 1200, height = 1000):
    if df.empty:
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(mapbox_style = "carto-positron", mapbox_zoom = 6, mapbox_center = {"lat": 46.493889, "lon": 2.602778}, height = height, width = width)
        return fig

    center_lat, center_lon = df['LAT_WGS'].mean(), df['LONG_WGS'].mean() # Centre de la carte définie sur la moyenne des coordonnées des points

    fig = go.Figure()

    # Extraction des liaisons uniques entre sites
    unique_connections = df.sort_values('DATE').drop_duplicates(subset = ['LAT_WGS', 'LONG_WGS'], keep = 'first')

    # Tracer les liaisons
    last_point = None
    for _, row in unique_connections.iterrows():
        if last_point is not None:
            fig.add_trace(go.Scattermapbox(
                lat = [last_point['LAT_WGS'], row['LAT_WGS']],
                lon = [last_point['LONG_WGS'], row['LONG_WGS']],
                mode = 'lines',
                line = dict(color = 'violet', width = 2),
                showlegend = False
            ))
        last_point = row

    # Ajout des marqueurs pour les sites
    sites = df.drop_duplicates(subset = ['LAT_WGS', 'LONG_WGS', 'LIEU_DIT'])
    for _, site in sites.iterrows():
        fig.add_trace(go.Scattermapbox(
            lat = [site['LAT_WGS']],
            lon = [site['LONG_WGS']],
            mode = 'markers+text',
            marker = go.scattermapbox.Marker(size=9, color='blue'),
            textfont = dict(color = 'black'),  # Couleur du texte
            text = site['LIEU_DIT'],
            textposition = "bottom right",
            name = site['LIEU_DIT'],           # Utiliser la bonne étiquette comme nom de site
            showlegend = False
        ))

    fig.update_layout(
        mapbox_style = "carto-positron",       # Utilisation d'un fond de carte en noir et blanc
        mapbox_zoom = 6,
        mapbox_center = {"lat": center_lat, "lon": center_lon},
        height = height,
        width = width
    )
    return fig

def create_transition_matrix(df, remove_self_loops = True, reduce_self_loops = False, reduction_factor = 0.5):
    # Tri par individu et date pour suivre les transitions
    df = df.sort_values(by = ['NUM_PIT', 'DATE'])

    # Créer une colonne pour le lieu précédent
    df['LIEU_PRECEDENT'] = df.groupby('NUM_PIT')['LIEU_DIT'].shift()

    # Filtrer pour obtenir seulement les transitions valides (non nulles)
    df_transitions = df.dropna(subset = ['LIEU_PRECEDENT'])

    # Compter les transitions de chaque lieu vers un autre
    transition_counts = df_transitions.groupby(['LIEU_PRECEDENT', 'LIEU_DIT']).size().reset_index(name = 'count')

    # Retirer les transitions où source == target si demandé
    if remove_self_loops:
        transition_counts = transition_counts[transition_counts['LIEU_PRECEDENT'] != transition_counts['LIEU_DIT']]

    # Réduire le poids des transitions de recontrôle (si demandé)
    if reduce_self_loops:
        transition_counts.loc[transition_counts['LIEU_PRECEDENT'] == transition_counts['LIEU_DIT'], 'count'] *= reduction_factor

    # Construire une matrice de transition
    lieux = sorted(set(df['LIEU_DIT'].unique()) | set(df['LIEU_PRECEDENT'].dropna().unique()))
    transition_matrix = pd.DataFrame(0, index = lieux, columns = lieux)

    for _, row in transition_counts.iterrows():
        transition_matrix.at[row['LIEU_PRECEDENT'], row['LIEU_DIT']] = row['count']

    return transition_matrix, lieux

def process_transition_matrix(transition_matrix, df, threshold = 9):
    # Transformer la matrice en table de connexions
    transition_table = transition_matrix.stack().reset_index()
    transition_table.columns = ['source', 'target', 'count']

    # Assurer l'ordre alphabétique des paires (source, target) pour un regroupement correct
    transition_table['site_pair'] = transition_table.apply(
        lambda row: tuple(sorted([row['source'], row['target']])), axis = 1
    )

    # Grouper par paire de sites et sommer les counts
    transition_table = transition_table.groupby('site_pair', as_index = False).agg(
        count = ('count', 'sum')  # Somme des counts
    )

    # Séparer les paires de sites dans des colonnes distinctes
    transition_table[['source', 'target']] = pd.DataFrame(transition_table['site_pair'].tolist(), index = transition_table.index)

    # Filtrer pour ne garder que les connexions avec au moins un certain nombre d'occurrences
    transition_table = transition_table[transition_table['count'] > threshold] # Valeur du seuil de significativité à sélectionner

    # Obtenir les limites pour normaliser les valeurs de count
    min_count = transition_table['count'].min()
    max_count = transition_table['count'].max()
    mean_count = transition_table['count'].mean()
    std_count = transition_table['count'].std()

    # Normaliser les valeurs de count entre 0 et 1
    #transition_table['normalized_count'] = (transition_table['count'] - min_count) / (max_count - min_count) # Normer
    transition_table['normalized_count'] = (transition_table['count'] - mean_count) / std_count # Centrer-normer

    # Création d'une colormap personnalisée
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "CustomGreenYellowOrangeRed",
        ["#808080", "#4B4B4B", "#FC4C02", "#FF8C00", "#FF0000"]
    )

    # Calculer les couleurs basées sur les counts standardisés
    transition_table['color'] = transition_table['normalized_count'].apply(lambda x: mcolors.to_hex(cmap(x)))

    # Fusionner les coordonnées du df dans transition_table pour source et target
    coords = df[['LIEU_DIT', 'LAT_WGS', 'LONG_WGS']].drop_duplicates()
    coords = coords.set_index('LIEU_DIT')

    transition_table = transition_table.merge(coords, left_on = 'source', right_index = True)
    transition_table = transition_table.merge(coords, left_on = 'target', right_index = True, suffixes = ('_source', '_target'))

    return transition_table

def create_trajectories_map_from_matrix(df, transition_table, width = 1200, height = 1000):
    fig = go.Figure()

    # Tracer chaque connexion individuellement avec sa couleur
    for _, row in transition_table.iterrows():
        fig.add_trace(go.Scattermapbox(
            lat = [row['LAT_WGS_source'], row['LAT_WGS_target']],
            lon = [row['LONG_WGS_source'], row['LONG_WGS_target']],
            mode = 'lines',
            line = dict(width = 1, color = row['color']),  # Utiliser la couleur calculée
            hovertext = f"Count: {row['count']}",          # Ajout du texte de survol
            hoverinfo = 'text',                            # Afficher le texte de survol
            showlegend = False
        ))

    # Ajouter tous les marqueurs pour les lieux d'un seul coup
    coords = df[['LIEU_DIT', 'LAT_WGS', 'LONG_WGS']].drop_duplicates()
    for _, coord in coords.iterrows():
            fig.add_trace(go.Scattermapbox(
                lat = [coord['LAT_WGS']],
                lon = [coord['LONG_WGS']],
                mode = 'markers+text',
                marker = go.scattermapbox.Marker(
                    size = 6,
                    color = '#8467D7',  # Violet clair
                ),
                textfont = dict(color = 'grey'),
                text = [coord['LIEU_DIT']],
                textposition = "bottom right",
                showlegend = False
                ))

    # Définir le centre de la carte
    center_lat, center_lon = df['LAT_WGS'].mean(), df['LONG_WGS'].mean()

    fig.update_layout(
        mapbox_style = "carto-positron",  # Utiliser le style de carte noir et blanc
        mapbox_zoom = 6,
        mapbox_center = {"lat": center_lat, "lon": center_lon},
        font = dict(color = 'black'),
        height = height,
        width = width
    )

    return fig

transition_matrix, labels = create_transition_matrix(df_antenna)
transition_table = process_transition_matrix(transition_matrix, df_antenna)
create_trajectories_map_from_matrix(df_antenna, transition_table)

map_section = create_trajectories_map(df_empty)

with open("pages/page2.md", "r", encoding = "utf-8") as file:
    page2 = file.read()

def refresh_button(state):
    df_filtered = df_antenna.copy()
    
    # Filtrer par département d'origine
    if state.selected_dpt:
        equipped_pit = df_filtered[(df_filtered['ACTION'] == 'T') & 
                                   (df_filtered['DEPARTEMENT'].isin(state.selected_dpt))]['NUM_PIT'].unique()
        df_filtered = df_filtered[df_filtered['NUM_PIT'].isin(equipped_pit)]
    
    # Filtrer par espèce
    if state.selected_sp:
        df_filtered = df_filtered[df_filtered['CODE_ESP'].isin(state.selected_sp)]

    # Filtrer par genre
    if state.selected_gender:
        df_filtered = df_filtered[df_filtered['SEXE'].isin(state.selected_gender)]

    # Filtrer par site d'origine
    if state.selected_sites:
        site_pit = df_filtered[(df_filtered['ACTION'] == 'T') & 
                               (df_filtered['LIEU_DIT'].isin(state.selected_sites))]['NUM_PIT'].unique()        
        df_filtered = df_filtered[df_filtered['NUM_PIT'].isin(site_pit)]
    
    # Filtrer par intervalle de dates
    if state.selected_dates and len(state.selected_dates) == 2:
        start_date = pd.Timestamp(state.selected_dates[0])
        end_date = pd.Timestamp(state.selected_dates[1])
        df_filtered = df_filtered[(df_filtered['DATE'] >= start_date) & (df_filtered['DATE'] <= end_date)]
    
    # Rafraichir la carte
    transition_matrix_filtered, labels_filtered = create_transition_matrix(df_filtered)
    transition_table_filtered = process_transition_matrix(transition_matrix_filtered, df_filtered)
    state.map_section = create_trajectories_map_from_matrix(df_filtered, transition_table_filtered)

## PHENOLOGIES DES SITES

def gant_diagram(df_original):
    # Créer une copie du DataFrame original par sécurité
    df_filtered = df_original[df_original['ACTION'] == "C"].copy()
    
    # Convertir la colonne DATE en datetime et localiser en UTC
    df_filtered['DATE'] = pd.to_datetime(df_filtered['DATE'])
    df_filtered['DATE'] = df_filtered['DATE'].dt.tz_localize('UTC')
    
    # Trier les valeurs par DATE
    df_filtered = df_filtered.sort_values(by = 'DATE', ascending = True)
    
    # Ajouter des colonnes pour les visites précédentes et les nouvelles visites
    df_filtered['Prev_DATE'] = df_filtered.groupby(['LIEU_DIT'])['DATE'].shift(1)
    df_filtered['New_Visit'] = (df_filtered['DATE'] - df_filtered['Prev_DATE']).dt.days > 1
    df_filtered['New_Visit'].fillna(True, inplace = True)
    df_filtered['Visit_ID'] = df_filtered.groupby(['LIEU_DIT'])['New_Visit'].cumsum()
    
    # Supprimer les LIEU_DIT qui n'ont aucune visite détectée
    df_filtered = df_filtered.dropna(subset = ['Visit_ID'])
    
    # Calculer min/max dates pour chaque visite
    result = df_filtered.groupby(['LIEU_DIT', 'Visit_ID']).agg(
        Start = pd.NamedAgg(column = 'DATE', aggfunc = 'min'),
        Finish = pd.NamedAgg(column = 'DATE', aggfunc = 'max'),
        Departement = pd.NamedAgg(column = 'DEPARTEMENT', aggfunc = 'first')
    ).reset_index()
    
    # Supprimer les LIEU_DIT qui n'ont pas de dates valides
    result = result.dropna(subset = ['Start', 'Finish'])

    # Filtrer les LIEU_DIT qui ont des résultats
    result = result[result['Finish'] > result['Start']]

    # Trier les sites par ordre alphabétique et les départements pour la légende
    result = result.sort_values(by = ['Departement', 'LIEU_DIT'])
    result['Start'] = pd.to_datetime(result['Start'])
    result['Finish'] = pd.to_datetime(result['Finish'])

    # Déterminer la hauteur de la figure en fonction du nombre de sites
    num_sites = result['LIEU_DIT'].nunique()
    height_per_site = 50        # Hauteur allouée par site en pixels
    base_height = 100           # Hauteur de base pour la figure
    max_height = 20000          # Hauteur maximale de la figure
    fig_height = min(base_height + num_sites * height_per_site, max_height)

    # Créer le diagramme de Gantt
    fig = px.timeline(
        result,
        x_start = 'Start',
        x_end = 'Finish',
        y = 'LIEU_DIT',
        color = 'Departement',  # Changer la couleur en fonction du département
        color_discrete_sequence = px.colors.qualitative.Plotly,
        labels = {'LIEU_DIT': 'Site'},
        title = 'Présence sur chaque site'
    )

    # Ajout de lignes verticales pour chaque 1er janvier
    start_year = result['Start'].dt.year.min()
    end_year = result['Finish'].dt.year.max()
    for year in range(start_year, end_year + 1):
        fig.add_vline(
            x = pd.Timestamp(f'{year}-01-01'),
            line = dict(color = 'grey', dash = 'dash', width = 1)
        )

    fig.update_layout(legend = dict(traceorder = "normal"), margin = dict(l = 300))

    # Mise à jour des étiquettes et de l'orientation de l'axe des ordonnées
    fig.update_yaxes(categoryorder = 'total ascending')  # Tri les sites par date de début (si nécessaire)
    fig.update_layout(
        xaxis_title = 'Date',
        yaxis_title = 'Site',
        xaxis = dict(tickformat = '%Y-%m-%d'),           # Format des dates sur l'axe X pour plus de clarté
        height = fig_height,
        legend = dict(bgcolor = 'rgba(0, 0, 0, 0)')
    )

    return fig

gant_global = gant_diagram(df_antenna)

with open("pages/page3.md", "r", encoding = "utf-8") as file:
    page3 = file.read()

def update_gant(state):
    df_filtered_gant = df_antenna.copy()
    df_filtered_gant = df_filtered_gant[df_filtered_gant['ACTION'] == "C"]

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

def detection_by_year(df_antenna):
    df_antenna['YEAR'] = df_antenna['DATE'].dt.year
    grouped_data = df_antenna.groupby(['YEAR', 'CODE_ESP']).size().reset_index(name = 'Detections')
    
    fig = px.bar(grouped_data, x = 'YEAR', y = 'Detections', color = 'CODE_ESP',
                 labels = {'Detections': 'Nombre de détections', 'CODE_ESP': 'Espèce'},
                 )

    fig.update_layout(
        height = 400,
        width = 400,
        yaxis_title = 'Nombre de détections',
        xaxis_title = None,
        xaxis = {'type': 'category', 'tickmode': 'linear'},  # Afficher toutes les années
        barmode = 'stack',
        legend = dict(
            bgcolor = 'rgba(0, 0, 0, 0)',
            orientation = 'h',  # Légende horizontale
            x = 0.5,            # Centrer la légende horizontalement
            y = -0.2,           # Placer la légende en dessous de la figure
            xanchor = 'center', # Ancrer la légende au centre
            yanchor = 'top'     # Ancrer la légende au-dessus de l'axe x
        ),
        margin = dict(b = 100)
    )

    return fig

def capture_by_year(df_antenna):
    df_filtre = df_antenna[df_antenna['ACTION'] == 'T']
    df_filtre['YEAR'] = df_filtre['DATE'].dt.year
    df_grouped = df_filtre.groupby(['YEAR', 'CODE_ESP'])['NUM_PIT'].nunique().reset_index()
    df_grouped.rename(columns = {'NUM_PIT': 'Nombre d\'individus uniques'}, inplace = True)
    
    fig = px.bar(df_grouped, x = 'YEAR', y = 'Nombre d\'individus uniques', color = 'CODE_ESP',
                 labels = {'Nombre d\'individus uniques': 'Nombre d\'individus uniques', 'CODE_ESP': 'Espèce'}
                 )

    fig.update_layout(
        height = 400,
        width = 400,
        yaxis_title = 'Nombre d\'individus uniques',
        xaxis_title = None,
        xaxis = {'type': 'category', 'tickmode': 'linear'},  # Afficher toutes les années
        legend = dict(
            bgcolor ='rgba(0, 0, 0, 0)',
            orientation = 'h',  # Légende horizontale
            x = 0.5,            # Centrer la légende horizontalement
            y = -0.2,           # Placer la légende en dessous de la figure
            xanchor = 'center', # Ancrer la légende au centre
            yanchor = 'top'     # Ancrer la légende au-dessus de l'axe x
        ),
        margin = dict(b = 100)
    )  

    return fig

def control_by_year(df_antenna):
    df_filtre = df_antenna[df_antenna['ACTION'] == 'C']
    df_filtre['YEAR'] = df_filtre['DATE'].dt.year
    df_grouped = df_filtre.groupby(['YEAR', 'CODE_ESP'])['NUM_PIT'].nunique().reset_index()
    df_grouped.rename(columns = {'NUM_PIT': 'Nombre d\'individus'}, inplace = True)
    
    fig = px.bar(df_grouped, x = 'YEAR', y = 'Nombre d\'individus', color = 'CODE_ESP',
                 labels = {'Nombre d\'individus': 'Nombre d\'individus', 'CODE_ESP': 'Espèce'},
                 )

    fig.update_layout(
        height = 400,
        width = 400,
        yaxis_title = 'Nombre d\'individus',
        xaxis_title = None,
        xaxis = {'type': 'category', 'tickmode': 'linear'},  # Afficher toutes les années
        legend = dict(
            bgcolor = 'rgba(0, 0, 0, 0)',
            orientation = 'h',  # Légende horizontale
            x = 0.5,            # Centrer la légende horizontalement
            y = -0.2,           # Placer la légende en dessous de la figure
            xanchor = 'center', # Ancrer la légende au centre
            yanchor = 'top'     # Ancrer la légende au-dessus de l'axe x
        ),
        margin = dict(b = 100)
    )  

    return fig

def detection_frequencies(df_antenna):
    df_antenna['MONTH_DAY'] = df_antenna['DATE'].dt.strftime('%m-%d')
    global_freq = df_antenna.groupby('MONTH_DAY').size().reset_index(name = 'Global Detections')

    # Calculer les fréquences par site
    site_freq = df_antenna.groupby(['MONTH_DAY', 'LIEU_DIT']).size().reset_index(name = 'Detections')
    sites = site_freq['LIEU_DIT'].unique()

    # Préparer l'ordre chronologique
    months_days = pd.date_range('2021-01-01', '2021-12-31').strftime('%m-%d')
    global_freq['MONTH_DAY'] = pd.Categorical(global_freq['MONTH_DAY'], categories = months_days, ordered = True)
    global_freq = global_freq.sort_values('MONTH_DAY')

    # Création du graphique
    fig = go.Figure()

    # Ajouter la courbe globale
    fig.add_trace(go.Scatter(x = global_freq['MONTH_DAY'], y = global_freq['Global Detections'],
                            mode = 'lines', name = 'Global'))

    # Ajouter une courbe pour chaque site
    for site in sites:
        site_data = site_freq[site_freq['LIEU_DIT'] == site]
        site_data['MONTH_DAY'] = pd.Categorical(site_data['MONTH_DAY'], categories = months_days, ordered = True)
        site_data = site_data.sort_values('MONTH_DAY')
        fig.add_trace(go.Scatter(x = site_data['MONTH_DAY'], y = site_data['Detections'],
                                mode = 'lines', name = site))

    # Mise à jour du layout
    fig.update_layout(
        xaxis_title = 'Jour de l\'année',
        yaxis_title = 'Nombre de détections',
        xaxis = dict(type = 'category', categoryorder = 'array', categoryarray = [md for md in months_days]),
        legend = dict(bgcolor = 'rgba(0, 0, 0, 0)'),
        #yaxis = dict(range = [0, global_freq['Global Detections'].max() + 10])
    )
    return fig

def pie_controled(df_antenna):
    species_counts = df_antenna[df_antenna['ACTION'] == 'C']['CODE_ESP'].value_counts().reset_index()
    species_counts.columns = ['Species', 'Count']

    # Créer un diagramme circulaire
    fig = px.pie(species_counts, 
                values = 'Count', names = 'Species', 
                color_discrete_sequence = px.colors.qualitative.Pastel,
                hole = 0.5,)

    # Personnalisation supplémentaire
    fig.update_layout(legend_title_text = 'Espèce',
                    showlegend = True,
                    legend = dict(bgcolor = 'rgba(0, 0, 0, 0)')
                        )
    return fig

def pie_marked(df_antenna):
    marked_species = df_antenna[df_antenna['ACTION'] == 'T']
    species_counts = marked_species['CODE_ESP'].value_counts().reset_index()
    species_counts.columns = ['Species', 'Count']

    # Créer un diagramme circulaire
    fig = px.pie(species_counts, 
                values = 'Count', names = 'Species', 
                color_discrete_sequence = px.colors.qualitative.Pastel,
                hole = 0.5)

    # Personnalisation supplémentaire
    fig.update_layout(legend_title_text = 'Espèce',
                    showlegend = True,
                    legend = dict(bgcolor = 'rgba(0, 0, 0, 0)')
                        )
    return fig

def top_detection(df_antenna):
    df_antenna['NUM_PIT'] = "n° " + df_antenna['NUM_PIT'].astype(str)

    # Obtenir les dix catégories les plus fréquentes avec leurs occurrences
    top_categories = df_antenna['NUM_PIT'].value_counts().head(10)

    # Créer un DataFrame à partir des dix premières catégories
    df_top_categories = pd.DataFrame({'NUM_PIT': top_categories.index, 'Occurrences': top_categories.values})
    df_top_categories = df_top_categories.sort_values(by = 'Occurrences', ascending = False)

    # Créer le diagramme en barres horizontales
    fig = px.bar(df_top_categories, x = 'Occurrences', y = 'NUM_PIT', orientation = 'h',
                 labels = {'Occurrences': "Nombre d'occurrences", 'NUM_PIT': ''},
                 color = 'NUM_PIT', color_discrete_sequence = px.colors.qualitative.Set3)

    # Ajuster la hauteur en fonction du nombre de catégories (avec une hauteur minimale de 400 pixels)
    bar_height = 50  # Hauteur de chaque barre
    min_height = 400  # Hauteur minimale du graphique
    calculated_height = max(min_height, len(df_top_categories) * bar_height)

    # Mettre à jour la mise en page avec des marges ajustées
    fig.update_layout(
        height = calculated_height,     # Hauteur dynamique
        showlegend = False,
        margin = dict(l = 200),         # Augmenter la marge gauche pour mieux lire les annotations
        legend = dict(bgcolor = 'rgba(0, 0, 0, 0)')
    )

    return fig

# Initialisation de tous les plots
plot_detection_year = detection_by_year(df_antenna)      # Barplot du nombre de détections par an et par espèce
plot_capture_year = capture_by_year(df_antenna)          # Barplot du nombre de captures par an et par espèces
plot_control_year = control_by_year(df_antenna)          # Barplot du nombre de contrôles par an et par espèces
plot_frequencies = detection_frequencies(df_antenna)     # Courbes de fréquences de détections par jour de l'année et par site
plot_pie_controled = pie_controled(df_antenna)           # Pieplot des individus contrôlés
plot_pie_marked = pie_marked(df_antenna)                 # Pieplot des individus marqués
plot_top_detection = top_detection(df_antenna)           # Barplot horizontal des 10 individus les plus détectés
table_plot_raw = process_transition_matrix(transition_matrix, df_antenna, threshold = 0)    
transition_table_plot = table_plot_raw[['source', 'target', 'count']].sort_values(by = 'count', ascending = False)  # Table des trajectoires 

# Initialisation des variables à plot
total_captured = len(df_antenna[(df_antenna['ACTION'] == 'T') | (df_antenna['ACTION'] == 'M')]) # Individus capturés
total_recaptured = df_antenna[df_antenna['ACTION'] == 'C']['NUM_PIT'].nunique()                 # Individus contrôlés
total_marked = df_antenna[df_antenna['ACTION'] == 'T']['NUM_PIT'].nunique()                     # Individus marqués
sites_capture = df_antenna[df_antenna['ACTION'] == 'T']['LIEU_DIT'].nunique()                   # Sites capturés au moins une fois
sites_antennes = df_antenna['LIEU_DIT'].nunique()                                               # Sites contrôlés au moins une fois

with open("pages/page4.md", "r", encoding = "utf-8") as file:
    page4 = file.read()

# DEMARRAGE DE L'APPLICATION
pages = {
    "/": root_md,
    "presentation": page1,
    "antennes": page2,
    "phenologie": page3,
    "statistiques": page4
}

gui = Gui(pages = pages, css_file = "assets/styles.css")
gui.run(host = '0.0.0.0', port = 5000, use_session = True) # use_session = True pour permettre l'usage de plusieurs users en même temps
