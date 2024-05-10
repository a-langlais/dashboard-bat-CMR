import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from custom_functions import create_interactive_map, show_map

st.set_page_config(page_title = "Panneau de contrôle CMR CCPNA", layout = "wide", page_icon = "")

st.markdown("<h1 style='text-align: left; color: white;'>🦇 Panneau de contrôle CCPNA</h1>", unsafe_allow_html = True)
st.markdown("Projet Chiroptères Cavernicoles Prioritaires de Nouvelle-Aquitaine, porté par France Nature Environnement Nouvelle-Aquitaine (2016-2024)")
st.header("", divider = 'gray')

df = pd.read_csv("df_cmr_clean.csv")
df['DATE'] = df['DATE'].astype('datetime64[ns]')
df['ANNEE'] = df['ANNEE'].astype('int')
df['COMMUNE'] = df['COMMUNE'].astype('str')
df['LIEU_DIT'] = df['LIEU_DIT'].astype('str')
df['DEPARTEMENT'] = df['DEPARTEMENT'].astype('str')
df['CODE_ESP'] = df['CODE_ESP'].astype('str')
df['SEXE'] = df['SEXE'].astype('str')
df['ACTION'] = df['ACTION'].astype('str')
df['NUM_PIT'] = df['NUM_PIT'].astype('str')
df['LONG_L93'] = df['LONG_L93'].astype('float')
df['LAT_L93'] = df['LAT_L93'].astype('float')
df['LONG_WGS'] = df['LONG_WGS'].astype('float')
df['LAT_WGS'] = df['LAT_WGS'].astype('float')

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
    
    col1, col2 = st.columns([0.7, 0.3])
    
    with col2:
        st.header("Paramètres")
        dept = df['DEPARTEMENT'].sort_values().unique()
        select_dept = st.multiselect(
            "Filtrer par département :",
            dept,
            placeholder = "Sélectionner un ou plusieurs département(s)...",
        )

        if select_dept:
            df_filtered = df[df['DEPARTEMENT'].isin(select_dept)]
        else:
            df_filtered = df

        sites = df_filtered['LIEU_DIT'].sort_values().unique()
        selected_site = st.selectbox(
            "Filtrer par site de première capture :",
            sites,
            index = None,
            placeholder = "Choisissez un site..."
        )

        if selected_site is not None:
            df_filtered = df_filtered[df_filtered['LIEU_DIT'] == selected_site]
            df_filtered = df_filtered[df_filtered['ACTION'] == 'T']
            pit_with_action_c = df_filtered['NUM_PIT'].unique()
            df_filtered = df[df['NUM_PIT'].isin(pit_with_action_c)]

        selected_dates = st.slider(
            "Filtrer un intervalle de dates :",
            min_value=df['DATE'].min().to_pydatetime().date(),
            max_value=df['DATE'].max().to_pydatetime().date(),
            value=(df['DATE'].min().to_pydatetime().date(), df['DATE'].max().to_pydatetime().date()),
            format="YYYY-MM-DD"
                )

        start_date, end_date = selected_dates
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        df_filtered = df_filtered[(df_filtered['DATE'] >= start_date) & (df_filtered['DATE'] <= end_date)]

        cola, colb, colc = st.columns([1, 1, 1])
        st.write(
            """
            <style>
            [data-testid="stMetricDelta"] svg {
                display: none;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        with cola:
            st.metric(label="Individus capturés", value= len(df_filtered[df_filtered['ACTION'].isin(['T', 'C', 'R'])]))
        with colb:
            total_marked = df_filtered[df_filtered['ACTION'] == 'T']['NUM_PIT'].nunique()
            st.metric(label = "Individus marqués", value = total_marked)
        with colc:
            recaptured = round(df_filtered[df_filtered['ACTION'] == 'R']['NUM_PIT'].nunique(), 3)
            percent_recaptured = round((recaptured / total_marked) * 100, 3)
            st.metric(label = "Individus recapturés", 
                      value = recaptured, 
                      delta = f"{percent_recaptured} %",
            )
        cold, cole = st.columns([1, 2])
        with cold:
            st.metric(label = "Nombre de sites", value = df_filtered['LIEU_DIT'].nunique())
            st.metric(label = "Nombre d'espèces", value = df_filtered['CODE_ESP'].nunique())
        with cole:
            st.dataframe(df_filtered[['DEPARTEMENT', 'LIEU_DIT']].drop_duplicates().reset_index(drop = True))

        with col1:
            show_map(df_filtered, width = 1200, height = 800)

with tab2:
    st.markdown("text ok")