import pyproj
import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium, folium_static
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def convert_l93_to_latlon(x, y):
    transformer = pyproj.Transformer.from_crs("epsg:2154", "epsg:4326", always_xy=True)
    lon, lat = transformer.transform(x, y)
    return lat, lon

def create_interactive_map(df):
    if df.empty:
        # Créer une carte vide
        m = folium.Map(location=[46.493889, 2.602778], zoom_start=6)
    else:
        # Centre de la carte (peut être ajusté selon vos données)
        df = df.dropna(subset=['LAT_WGS', 'LONG_WGS'])
        m = folium.Map(location=[df['LAT_WGS'].mean(), df['LONG_WGS'].mean()], zoom_start=9)

        # Générer une palette de couleurs pour les trajectoires
        num_individuals = df['NUM_PIT'].nunique()
        cmap_trajectories = plt.get_cmap('tab10', num_individuals)
        colors_trajectories = {ind: mcolors.rgb2hex(cmap_trajectories(i / num_individuals)) for i, ind in enumerate(df['NUM_PIT'].unique())}

        # Tracer les trajectoires entre les sites pour chaque individu
        trajectories = folium.FeatureGroup(name='Trajectoires')
        for ind, color in colors_trajectories.items():
            individual_data = df[df['NUM_PIT'] == ind].sort_values('DATE')
            lat_lon_pairs = list(zip(individual_data['LAT_WGS'], individual_data['LONG_WGS']))
            folium.PolyLine(lat_lon_pairs, color=color, weight=2).add_to(trajectories)
        trajectories.add_to(m)

        # Ajouter des marqueurs pour chaque site
        site_markers = folium.FeatureGroup(name='Sites')
        for i, (_, row) in enumerate(df.drop_duplicates('LIEU_DIT').iterrows()):
            lat, lon = row['LAT_WGS'], row['LONG_WGS']
            lieu_dit = row['LIEU_DIT']
            dept = row['DEPARTEMENT']
            popup_content = f'<div class="custom-popup">{dept}<br>{lieu_dit}</div>'
            popup = folium.Popup(popup_content, max_width=300)
            folium.CircleMarker(location=[lat, lon], radius=3, popup=popup, color='red', fill=True, fill_opacity=1).add_to(site_markers)
        site_markers.add_to(m)

        # Ajouter les contrôles de couches
        folium.LayerControl().add_to(m)

        # Ajouter le style CSS pour ajuster la largeur de la popup
        m.get_root().header.add_child(folium.Element("<style>.custom-popup {max-width:100%;}</style>"))

    return m

def show_map(df, width = 700, height = 500):
    m = create_interactive_map(df)
    folium_static(m, width = width, height = height)


