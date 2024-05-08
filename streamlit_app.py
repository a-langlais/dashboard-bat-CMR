import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from custom_functions import create_interactive_map, show_map

st.set_page_config(page_title = "Panneau de contrôle CMR CCPNA", layout = "wide", page_icon = "")

st.markdown("<h1 style='text-align: left; color: white;'>Panneau de contrôle CCPNA</h1>", unsafe_allow_html = True)
st.header("", divider = 'gray')

df = pd.read_csv("df_cmr.csv", low_memory = False)
df_filtered = df.dropna()

st.markdown("""
        <style>
            .stTabs [data-baseweb="tab-list"] {
                display: flex;
                gap: 10px;
            }

            .stTabs [data-baseweb="tab"] {
                padding: 10px 15px;
                border: 1px solid transparent;
                border-radius: 5px 5px 0 0;
                background-color: transparent;
                cursor: pointer;
                transition: all 0.3s ease;
            }

            .stTabs [data-baseweb="tab"]:hover {
                background-color: #8f8d9b;
            }

            .stTabs [aria-selected="true"] {
                background-color:  #57546a;
                border-color: #ccc;
                border-bottom-color: transparent;
            }
        </style>""", unsafe_allow_html = True)

tab1, tab2 = st.tabs(["Carte des trajectoires", "Statistiques phénologiques"])

with tab1:
    
    col1, col2 = st.columns([0.6, 0.4])
    
    with col2:
        dept = df['DEPARTEMENT'].unique()
        select_dept = st.selectbox(
            "Filtrer par département :",
            dept,
            index = None,
            placeholder = "Sélectionner un département...",
            )
        df_filtered = df[df['DEPARTEMENT'] == select_dept].dropna()

    with col1:
        show_map(df_filtered)

with tab2:
    st.markdown("text filler")