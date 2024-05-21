import pyproj
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import math

def convert_l93_to_latlon(x, y):
    transformer = pyproj.Transformer.from_crs("epsg:2154", "epsg:4326", always_xy=True)
    lon, lat = transformer.transform(x, y)
    return lat, lon

def haversine_distance(lat1, lon1, lat2, lon2):
    # Convertir les degrés en radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Rayon de la Terre en kilomètres
    R = 6371.0
    
    # Différences de coordonnées
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Formule de Haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distance en kilomètres
    distance = R * c
    return distance

def distance_parcourue_par_individu(df):
    total_distance = 0
    
    # Trier le DataFrame par ordre chronologique
    df = df.sort_values(by='DATE')
    
    # Itérer sur les lignes du DataFrame
    for i in range(len(df) - 1):
        lat1, lon1 = df.iloc[i]['LAT_WGS'], df.iloc[i]['LONG_WGS']
        lat2, lon2 = df.iloc[i + 1]['LAT_WGS'], df.iloc[i + 1]['LONG_WGS']
        total_distance += haversine_distance(lat1, lon1, lat2, lon2)
    
    return total_distance

def create_interactive_map(df, selected_site=None, height=1500):
    if df.empty:
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(mapbox_style="open-street-map", mapbox_zoom=6, mapbox_center={"lat": 46.493889, "lon": 2.602778}, height=height)
        return st.plotly_chart(fig, use_container_width=True)

    # Définir les centres de la carte basés sur les moyennes des latitudes et longitudes
    center_lat, center_lon = df['LAT_WGS'].mean(), df['LONG_WGS'].mean()

    fig = go.Figure()

    # Tracer les trajectoires pour chaque individu
    tracked_connections = set()
    for ind in df['NUM_PIT'].unique():
        individual_data = df[df['NUM_PIT'] == ind].sort_values('DATE')
        previous_coords = None
        for _, row in individual_data.iterrows():
            current_coords = (row['LAT_WGS'], row['LONG_WGS'])
            if previous_coords and (previous_coords, current_coords) not in tracked_connections:
                fig.add_trace(go.Scattermapbox(
                    lat=[previous_coords[0], current_coords[0]],
                    lon=[previous_coords[1], current_coords[1]],
                    mode='lines',
                    line=dict(color='violet', width=2),
                    showlegend=False
                ))
                # Ajouter la trajectoire dans les deux directions pour éviter les doublons
                tracked_connections.add((previous_coords, current_coords))
                tracked_connections.add((current_coords, previous_coords))
            previous_coords = current_coords

    # Ajouter des marqueurs pour chaque site en bleu
    unique_sites = df.drop_duplicates(subset=['LAT_WGS', 'LONG_WGS', 'LIEU_DIT'])
    for _, site in unique_sites.iterrows():
        fig.add_trace(go.Scattermapbox(
            lat=[site['LAT_WGS']],
            lon=[site['LONG_WGS']],
            mode='markers+text',
            marker=go.scattermapbox.Marker(size=9, color='blue'),
            text=f"{site['LIEU_DIT']}",
            textposition="bottom right",
            textfont=dict(color='black'),  # Spécifiez la couleur du texte en noir
            hoverinfo = 'text',
            showlegend=False
        ))

    # Ajouter un marqueur rouge pour le site sélectionné
    if selected_site:
        selected_site_data = unique_sites[unique_sites['LIEU_DIT'] == selected_site]
        for _, site in selected_site_data.iterrows():
            fig.add_trace(go.Scattermapbox(
                lat=[site['LAT_WGS']],
                lon=[site['LONG_WGS']],
                mode='markers+text',
                marker=go.scattermapbox.Marker(size=9, color='red'),
                text=f"{site['LIEU_DIT']}",
                textposition="bottom right",
                textfont=dict(color='black'),  # Spécifiez la couleur du texte en noir
                showlegend=False
            ))

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=9,
        mapbox_center={"lat": center_lat, "lon": center_lon},
        height=height,
        showlegend=False
    )
    return st.plotly_chart(fig, use_container_width=True)

def create_trajectories_map(df, width = 1000, height = 1000):
    if df.empty:
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(mapbox_style="open-street-map", mapbox_zoom=6, mapbox_center={"lat": 46.493889, "lon": 2.602778}, height = height, width = width)
        return st.plotly_chart(fig)

    # Définir les centres de la carte basés sur les moyennes des latitudes et longitudes
    center_lat, center_lon = df['LAT_WGS'].mean(), df['LONG_WGS'].mean()

    fig = go.Figure()

    # Extraction des liaisons uniques entre sites
    unique_connections = df.sort_values('DATE').drop_duplicates(subset=['LAT_WGS', 'LONG_WGS'], keep='first')

    # Tracer les liaisons
    last_point = None
    for _, row in unique_connections.iterrows():
        if last_point is not None:
            fig.add_trace(go.Scattermapbox(
                lat=[last_point['LAT_WGS'], row['LAT_WGS']],
                lon=[last_point['LONG_WGS'], row['LONG_WGS']],
                mode='lines',
                line=dict(width=2),
                showlegend=False
            ))
        last_point = row

    # Ajouter les marqueurs pour les sites, avec noms dans la légende
    sites = df.drop_duplicates(subset=['LAT_WGS', 'LONG_WGS', 'LIEU_DIT'])
    for _, site in sites.iterrows():
        fig.add_trace(go.Scattermapbox(
            lat=[site['LAT_WGS']],
            lon=[site['LONG_WGS']],
            mode='markers+text',
            marker=go.scattermapbox.Marker(size=9, color='blue'),
            text=site['LIEU_DIT'],
            textposition="bottom right",
            name=site['LIEU_DIT'],  # Utiliser le lieu dit comme nom dans la légende
            showlegend = False
        ))

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=6,
        mapbox_center={"lat": center_lat, "lon": center_lon},
        height = height,
        width = width
    )
    return st.plotly_chart(fig)

def plot_trajectories_from_site(df, site, width=1000, height=1000):
    if df.empty:
        fig = go.Figure(go.Scattermapbox())
        fig.update_layout(mapbox_style="open-street-map", mapbox_zoom=6, mapbox_center={"lat": 46.493889, "lon": 2.602778}, width=width, height=height)
        return st.plotly_chart(fig)

    # Définir les centres de la carte basés sur les moyennes des latitudes et longitudes
    center_lat, center_lon = df['LAT_WGS'].mean(), df['LONG_WGS'].mean()
    fig = go.Figure()

    # Filtrer les individus par site sélectionné
    individuals = df[df['LIEU_DIT'] == site]['NUM_PIT'].unique()

    # Tracer les trajectoires pour chaque individu
    for ind in individuals:
        ind_df = df[df['NUM_PIT'] == ind].sort_values('DATE')
        fig.add_trace(go.Scattermapbox(
            lat=ind_df['LAT_WGS'],
            lon=ind_df['LONG_WGS'],
            mode='lines+markers',
            line=dict(color='blue', width=1),
            marker=dict(color='blue', size=5),
            showlegend = False
        ))

    # Ajouter un marqueur pour chaque site unique
    unique_sites = df.drop_duplicates(subset=['LAT_WGS', 'LONG_WGS', 'LIEU_DIT'])
    for _, site in unique_sites.iterrows():
        fig.add_trace(go.Scattermapbox(
            lat=[site['LAT_WGS']],
            lon=[site['LONG_WGS']],
            mode='markers',
            marker=go.scattermapbox.Marker(size=9, color='red'),
            text=f"{site['DEPARTEMENT']}<br>{site['LIEU_DIT']}",
            showlegend = False
        ))

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=9,
        mapbox_center={"lat": center_lat, "lon": center_lon},
        height=height,
        width=width
    )
    return st.plotly_chart(fig)

def gant_diagram_site(df):
    df['Prev_DATE'] = df.groupby(['NUM_PIT', 'LIEU_DIT'])['DATE'].shift(1)
    df['New_Visit'] = (df['DATE'] - df['Prev_DATE']).dt.days > 1
    df['Visit_ID'] = df.groupby(['NUM_PIT', 'LIEU_DIT'])['New_Visit'].cumsum()

    # Calculer min/max dates pour chaque visite
    result = df.groupby(['NUM_PIT', 'LIEU_DIT', 'Visit_ID']).agg(
        Start=pd.NamedAgg(column='DATE', aggfunc='min'),
        Finish=pd.NamedAgg(column='DATE', aggfunc='max')
    ).reset_index()

    # Assurez-vous que les colonnes de date sont au format datetime si ce n'est pas déjà le cas
    result['Start'] = pd.to_datetime(result['Start'])
    result['Finish'] = pd.to_datetime(result['Finish'])

    # Créer le diagramme de Gantt
    fig = px.timeline(
        result,
        x_start='Start',
        x_end='Finish',
        y='LIEU_DIT',  # ou 'NUM_PIT' si vous préférez regrouper par individu
        color='NUM_PIT',  # Changer la couleur selon l'individu
        color_discrete_sequence=px.colors.qualitative.Plotly,
        labels={'LIEU_DIT': 'Site', 'NUM_PIT': 'Individu'},
        title='Présence des individus sur chaque site'
    )

    # Ajouter des lignes verticales pour chaque 1er janvier
    start_year = result['Start'].dt.year.min()
    end_year = result['Finish'].dt.year.max()
    for year in range(start_year, end_year + 1):
        fig.add_vline(
            x=pd.Timestamp(f'{year}-01-01'),
            line=dict(color='grey', dash='dash', width = 1)
        )

    # Mise à jour des étiquettes et de l'orientation de l'axe des ordonnées
    fig.update_yaxes(categoryorder='total ascending')  # Cela trie les sites par date de début si nécessaire
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Site',
        xaxis=dict(tickformat='%Y-%m'),  # Format des dates sur l'axe X pour plus de clarté
        legend_title_text='Individu',
        legend_orientation="h",  # Horizontale
        legend=dict(
            x=0,  # Centre la légende horizontalement
            y=-0.3,  # Positionne la légende en dessous du graphique
            xanchor="left",  # Ancrage au centre pour le centrage horizontal
            yanchor="top"  # Ancrage en haut pour positionnement au-dessous
        )
    )
    return st.plotly_chart(fig)

def gant_diagram(df):
    df['Prev_DATE'] = df.groupby(['LIEU_DIT'])['DATE'].shift(1)
    df['New_Visit'] = (df['DATE'] - df['Prev_DATE']).dt.days > 1
    df['Visit_ID'] = df.groupby(['LIEU_DIT'])['New_Visit'].cumsum()

    # Calculer min/max dates pour chaque visite
    result = df.groupby(['LIEU_DIT', 'Visit_ID']).agg(
        Start=pd.NamedAgg(column='DATE', aggfunc='min'),
        Finish=pd.NamedAgg(column='DATE', aggfunc='max'),
        Department=pd.NamedAgg(column='DEPARTEMENT', aggfunc='first')
    ).reset_index()

    # Trier les sites par ordre alphabétique et les départements pour la légende
    result = result.sort_values(by=['Department', 'LIEU_DIT'])

    # Assurez-vous que les colonnes de date sont au format datetime si ce n'est pas déjà le cas
    result['Start'] = pd.to_datetime(result['Start'])
    result['Finish'] = pd.to_datetime(result['Finish'])

    # Créer le diagramme de Gantt
    fig = px.timeline(
        result,
        x_start='Start',
        x_end='Finish',
        y='LIEU_DIT',
        color='Department',  # Changer la couleur en fonction du département
        color_discrete_sequence=px.colors.qualitative.Plotly,
        labels={'LIEU_DIT': 'Site'},
        title='Présence sur chaque site'
    )

    # Ajouter des lignes verticales pour chaque 1er janvier
    start_year = result['Start'].dt.year.min()
    end_year = result['Finish'].dt.year.max()
    for year in range(start_year, end_year + 1):
        fig.add_vline(
            x=pd.Timestamp(f'{year}-01-01'),
            line=dict(color='grey', dash='dash', width = 1)
        )

    # La légende est implicitement triée par le tri des données
    fig.update_layout(legend=dict(traceorder="normal"))

    # Mise à jour des étiquettes et de l'orientation de l'axe des ordonnées
    fig.update_yaxes(categoryorder='total ascending')  # Cela trie les sites par date de début si nécessaire
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Site',
        xaxis=dict(tickformat='%Y-%m-%d'),  # Format des dates sur l'axe X pour plus de clarté
        height=1500
    )

    return st.plotly_chart(fig, use_container_width=True)  # Hauteur fixe avec possibilité de scroller
