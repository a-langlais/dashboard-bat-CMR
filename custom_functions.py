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
    if 'map' not in st.session_state or st.session_state.map is None:
        # Centre de la carte (peut être ajusté selon vos données)
        df = df.dropna(subset = ['LAT_WGS', 'LONG_WGS'])
        m = folium.Map(location=[df['LAT_WGS'].mean(), df['LONG_WGS'].mean()], zoom_start=12)

        # Générer une palette de couleurs
        num_individuals = df['NUM_PIT'].unique().shape[0]
        cmap = plt.get_cmap('tab20', num_individuals)
        
        # Créer un dictionnaire pour associer chaque individu à une couleur
        colors = {ind: mcolors.rgb2hex(cmap(i / num_individuals)) for i, ind in enumerate(df['NUM_PIT'].unique())}

        # Tracer les trajectoires et positions pour chaque individu
        for ind, color in colors.items():
            individual_data = df[df['NUM_PIT'] == ind].sort_values('DATE')
            lat_lon_pairs = list(zip(individual_data['LAT_WGS'], individual_data['LONG_WGS']))

            # Vérifier que la liste des positions n'est pas vide
            if lat_lon_pairs:
                # Tracer la trajectoire de l'individu
                folium.PolyLine(lat_lon_pairs, color=color, weight=2).add_to(m)

                # Ajouter des marqueurs pour chaque position
                for lat, lon in lat_lon_pairs:
                    folium.CircleMarker(location=[lat, lon], radius=5, color=color, fill=True, fill_color=color, fill_opacity=1).add_to(m)
            else:
                print(f"No location data available for individual {ind}")
    return m

def show_map(df):
    m = create_interactive_map(df)
    folium_static(m)


