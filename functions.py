import pandas as pd
import folium
import tempfile
import plotly.express as px
from folium import Map, Popup
from folium.elements import Element

def load_data_antenna():
    # Chargement des jeux de données
    df_individus = pd.read_csv(r'data/df_individus.csv', engine = "pyarrow", dtype_backend = "pyarrow")
    df_sites = pd.read_csv(r'data/df_sites.csv', engine = "pyarrow", dtype_backend = "pyarrow")
    df_distances = pd.read_csv(r'data/df_distances.csv', engine = "pyarrow", dtype_backend = "pyarrow")
    df_controls = pd.read_csv(r'data/df_controls.csv', engine = "pyarrow", dtype_backend = "pyarrow")
    df_mapping = pd.read_csv(r'data/df_mapping_regions.csv', engine = "pyarrow", dtype_backend = "pyarrow")

    # Ajout du SEXE sur df_controls
    df_controls = df_controls.merge(df_individus[['NUM_PIT', 'SEXE']], left_on='NUM_PIT', right_on='NUM_PIT', how='left')

    # Ajout du SEXE sur df_distances
    df_distances = df_distances.merge(df_individus[['NUM_PIT', 'SEXE']], left_on='NUM_PIT', right_on='NUM_PIT', how='left')

    # Nettoyer df_distances
    df_distances = (
    df_distances
    .dropna(subset=['LAT_DEPART', 'LONG_DEPART', 'LAT_ARRIVEE', 'LONG_ARRIVEE'])
    .drop_duplicates(subset=['NUM_PIT', 'CODE_ESP', 'SITE_DEPART', 'SITE_ARRIVEE'], keep='last')
    .query('DIST_KM > 0')
)
    return df_controls, df_individus, df_sites, df_distances, df_mapping

def expose_folium(fol_map: Map):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
        fol_map.save(temp_file.name)
        with open(temp_file.name, "rb") as f:
            return f.read()

def generate_map(df_distances, df_sites):

    if df_distances.empty:
        m = folium.Map(location=[46.493889, 2.602778], zoom_start=6, tiles='CartoDB positron')
        return m

    # Calcul du centre de la carte
    lat_mean = df_distances[['LAT_DEPART', 'LAT_ARRIVEE']].mean().mean()
    lon_mean = df_distances[['LONG_DEPART', 'LONG_ARRIVEE']].mean().mean()

    # Création de la carte
    m = folium.Map(location=[lat_mean, lon_mean], zoom_start=6, tiles='CartoDB positron')

    # Couleurs pour chaque espèce
    color_map = {
        'RHIFER': 'blue',
        'MYOEMA': 'green',
        'RHIEUR': 'red',
        'MINSCH': 'purple',
        'MYOMYO': 'pink',
        'MYODAU': 'black'
    }

    # Tracer les lignes de déplacement
    for _, row in df_distances.iterrows():
        folium.PolyLine(
            locations=[(row['LAT_DEPART'], row['LONG_DEPART']), (row['LAT_ARRIVEE'], row['LONG_ARRIVEE'])],
            color=color_map.get(row['CODE_ESP'], 'gray'),
            weight=1,
            opacity=0.4
        ).add_to(m)

    # Ajouter les marqueurs pour chaque site
    sites_depart = df_distances['SITE_DEPART'].unique().tolist()
    sites_arrivee = df_distances['SITE_ARRIVEE'].unique().tolist()
    sites = list(set(sites_depart + sites_arrivee))
    df_sites = df_sites[df_sites['LIEU_DIT'].isin(sites)]

    for _, site in df_sites.iterrows():
        folium.CircleMarker(
            location=(site['LAT_WGS'], site['LONG_WGS']),
            radius=2,
            color='red',
            opacity=0.8,
            fill=True,
            fill_color='red',
            fill_opacity=1,
            popup=Popup(site['LIEU_DIT'], max_width=300)
        ).add_to(m)

   # Identifier les espèces présentes
    species_present = df_distances['CODE_ESP'].unique()

    # Construire la légende dynamique
    legend_html = """
    <div style="position: fixed; 
                 top: 10px; 
                 left: 10px; 
                 width: 150px; 
                 height: auto; 
                 background-color: white; 
                 border: 2px solid grey; 
                 z-index: 9999; 
                 font-size: 14px;
                 padding: 10px;
                 ">
        <b>Légende</b><br>
    """
    for species in species_present:
        if species in color_map:
            legend_html += f"""
            <i style="background: {color_map[species]}; width: 12px; height: 12px; display: inline-block;"></i> {species}<br>
            """
    legend_html += "</div>"
    
    m.get_root().html.add_child(Element(legend_html))

    return m

def gant_diagram(df_controls):
    # Créer une copie du DataFrame original par sécurité
    df_filtered = df_controls.copy()
    df_filtered = df_filtered[df_filtered['LIEU_DIT'].isin(["Brelouze", "Mairie d'Annepont", "Grottes de Loubeau", "Le Plessis", "Puy-Chenin", "Cézelle", "La Bourtière", "Goizet (W)", "Château de Gagemont", "Faye-L'Abbesse - Bourg", "Guibaud", "Cave Billard", "Grotte de Boisdichon", "Les Roches", "Barrage de l'Aigle", "Gouffre de la Fage",
                  "Ancienne citerne à eau", "Château de Verteuil", "Les Dames", "Château de Hautefort", "Les Tours de Merle - Tour Fulcon", "Le Petit Pin", "Maison Brousse", "Caves de Laubenheimer", "Château de Villandraut", "Tunnel ferroviaire", "Grotte de la carrière", "Centrale hydroélectrique de Claredent", "Fermette des Nobis",
                  "Beauregard", "Grotte de la Deveze", "Petexaenea (Site générique Galeries N&S)", "Gouffre de Bexanka", "Mikelauenziloa"])]
    
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

def gant_diagram_concat(df_original, concat_year = True, year_reference=2023):
    df_filtered = df_original.copy()
    df_filtered['DATE'] = pd.to_datetime(df_filtered['DATE'])
    df_filtered['DATE'] = df_filtered['DATE'].dt.tz_localize('UTC')
    df_filtered = df_filtered.sort_values(by = 'DATE', ascending = True)
    
    df_filtered['Prev_DATE'] = df_filtered.groupby(['LIEU_DIT'])['DATE'].shift(1)
    df_filtered['New_Visit'] = (df_filtered['DATE'] - df_filtered['Prev_DATE']).dt.days > 1
    df_filtered['New_Visit'].fillna(True, inplace = True)
    df_filtered['Visit_ID'] = df_filtered.groupby(['LIEU_DIT'])['New_Visit'].cumsum()
    df_filtered = df_filtered.dropna(subset = ['Visit_ID'])
    
    result = df_filtered.groupby(['LIEU_DIT', 'Visit_ID']).agg(
        Start = pd.NamedAgg(column = 'DATE', aggfunc = 'min'),
        Finish = pd.NamedAgg(column = 'DATE', aggfunc = 'max'),
        Departement = pd.NamedAgg(column = 'DEPARTEMENT', aggfunc = 'first')
    ).reset_index()
    
    result = result.dropna(subset = ['Start', 'Finish'])
    result = result[result['Finish'] > result['Start']]

    # Ajuster les dates si concat_year est True
    if concat_year:
        def adjust_year(date):
            try:
                return date.replace(year = year_reference)
            except ValueError:
                # Pour le 29 février dans une année non-bissextile, le remplace par le 28 février
                return date.replace(year = year_reference, day = 28)
        result['Start'] = result['Start'].apply(adjust_year)
        result['Finish'] = result['Finish'].apply(adjust_year)
    
    # Trier les sites par ordre alphabétique et les départements pour la légende
    result = result.sort_values(by = ['Departement', 'LIEU_DIT'])
    result['Start'] = pd.to_datetime(result['Start'])
    result['Finish'] = pd.to_datetime(result['Finish'])

    # Déterminer la hauteur de la figure en fonction du nombre de sites
    num_sites = result['LIEU_DIT'].nunique()

    # Créer le diagramme de Gantt
    fig = px.timeline(
        result,
        x_start = 'Start',
        x_end = 'Finish',
        y = 'LIEU_DIT',
        labels = {'LIEU_DIT': 'Site'},
        title = 'Présence sur chaque site'
    )

    # Ajouter des lignes verticales pour chaque 1er janvier (si concat_year est False)
    if not concat_year:
        start_year = result['Start'].dt.year.min()
        end_year = result['Finish'].dt.year.max()
        for year in range(start_year, end_year + 1):
            fig.add_vline(
                x = pd.Timestamp(f'{year}-01-01'),
                line = dict(color = 'grey', dash = 'dash', width = 1)
            )
    else:
        # Ajouter uniquement une ligne pour l'année de référence
        fig.add_vline(
            x = pd.Timestamp(f'{year_reference}-01-01'),
            line = dict(color = 'grey', dash = 'dash', width = 1)
        )

    fig.update_layout(legend = dict(traceorder = "normal"))

    # Mise à jour des étiquettes et de l'orientation de l'axe des ordonnées
    fig.update_yaxes(categoryorder = 'total ascending')
    fig.update_layout(
        xaxis_title = '',
        yaxis_title = '',
        xaxis = dict(tickformat = '%m'),
        yaxis = dict(showgrid = True, zeroline = False, title = "Phase de présence"),
        height = 300
    )

    return fig

def distance_boxplot(df_distances):
    # Couleurs pour chaque espèce
    color_map = {
        'RHIFER' : 'blue',
        'MYOEMA' : 'green',
        'RHIEUR' : 'red',
        'MINSCH' : 'purple',
        'MYOMYO' : 'pink',
        'MYODAU' : 'black'
    }

    fig = px.box(
        df_distances,
        x = 'CODE_ESP',
        y = 'DIST_KM',
        color = 'CODE_ESP',  # Utilisation des couleurs basées sur les espèces
        color_discrete_map = color_map,
        title = ''
    )

    fig.update_layout(
        xaxis_title = '',
        yaxis_title = 'Distance entre deux sites (km)',
        showlegend = False
    )

    return fig