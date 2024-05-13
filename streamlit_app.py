import streamlit as st
import pandas as pd
from custom_functions import create_interactive_map, create_trajectories_map, gant_diagram_site, plot_trajectories_from_site, gant_diagram
import plotly.express as px

st.set_page_config(page_title = "Panneau de contrôle CMR CCPNA", layout = "wide", page_icon = "🦇")

st.markdown("<h1 style='text-align: left; color: white;'>🦇 Panneau de contrôle CCPNA</h1>", unsafe_allow_html = True)
st.markdown("D'après les données du projet Chiroptères Cavernicoles Prioritaires de Nouvelle-Aquitaine (CCPNA), porté par France Nature Environnement Nouvelle-Aquitaine (2016-2024)")
st.header("", divider = 'gray')

@st.cache_data
def load_data():
    df = pd.read_csv("df_cmr_clean.csv", engine = "pyarrow", dtype_backend = "pyarrow")
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
    return df

df = load_data()

@st.cache_data
def load_data_antenna():
    df_antenna = pd.read_csv(r'data/data_antenna_2016_2023.csv', engine = "pyarrow", dtype_backend = "pyarrow")
    df_antenna['DATE'] = df_antenna['DATE'].astype('datetime64[ns]')
    df_antenna['HEURE'] = pd.to_datetime(df_antenna['HEURE'], format='%H:%M:%S').dt.time
    df_antenna['ANNEE'] = df_antenna['ANNEE'].astype('int')
    df_antenna['COMMUNE'] = df_antenna['COMMUNE'].astype('str')
    df_antenna['LIEU_DIT'] = df_antenna['LIEU_DIT'].astype('str')
    df_antenna['PRECISION_MILIEU'] = df_antenna['PRECISION_MILIEU'].astype('str')
    df_antenna['DEPARTEMENT'] = df_antenna['DEPARTEMENT'].astype('str')
    df_antenna['CODE_ESP'] = df_antenna['CODE_ESP'].astype('str')
    df_antenna['ACTION'] = df_antenna['ACTION'].astype('str')
    df_antenna['NUM_PIT'] = df_antenna['NUM_PIT'].astype('str')
    df_antenna['LONG_L93'] = df_antenna['LONG_L93'].astype('float')
    df_antenna['LAT_L93'] = df_antenna['LAT_L93'].astype('float')
    df_antenna['LONG_WGS'] = df_antenna['LONG_WGS'].astype('float')
    df_antenna['LAT_WGS'] = df_antenna['LAT_WGS'].astype('float')
    return df_antenna

df_antenna = load_data_antenna()

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

tab1, tab2, tab3, tab4 = st.tabs(["Données de CMR", "Contrôles des antennes", "Phénologie temporelle des sites", "Statistiques analytiques"])

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
            df_filtered = df[df['NUM_PIT'] != df['NUM_PIT']]

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
            percent_recaptured = round((recaptured / total_marked) * 100, 3) if total_marked != 0 else 0
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
            create_interactive_map(df_filtered, width = 1200, height = 800)

with tab2:
    col1, col2 = st.columns([0.55, 0.45])
    
    with col2:
        st.header("Paramètres")
        on = st.toggle("Suivi par individu")

        if on:
            st.markdown("Grâce à ce module, vous pouvez suivre le déplaçement d'un ou plusieurs individus dans l'ordre chronologique.")
            individus = df_antenna['NUM_PIT'].sort_values().unique()
            select_inds = st.multiselect(
                "Suivre un individu",
                individus,
                placeholder = "Choisissez un ou plusieurs individu(s) :",
            )

            selected_years = st.slider(
                "Filtrer un intervalle d'année :",
                min_value=df['ANNEE'].min(),
                max_value=df['ANNEE'].max(),
                value=(df['ANNEE'].min(), df['ANNEE'].max()),
            )

            if select_inds:
                start_year, end_year = selected_years
                df_antenna_filtered = df_antenna[df_antenna['NUM_PIT'].isin(select_inds)]
                df_antenna_filtered = df_antenna_filtered[(df_antenna_filtered['ANNEE'] >= start_year) & (df_antenna_filtered['ANNEE'] <= end_year)]
                gant_diagram_site(df_antenna_filtered)
            else:
                df_antenna_filtered = df_antenna[df_antenna['NUM_PIT'] != df_antenna['NUM_PIT']]
        else:
            st.markdown("Grâce à ce module, vous pouvez observer l'ensemble des trajets réalisés entre les sites connectés au site sélectionné. Les trajectoires sont définies par les trajets des individus étant passés par le site sélectionné.")
            
            sites_antenna = df_antenna['LIEU_DIT'].sort_values().unique()
            selected_site_antenna = st.selectbox(
                "Filtrer par site :",
                sites_antenna,
                index = None,
                placeholder = "Choisissez un site d'antenne..."
            )

            if selected_site_antenna is None:
                df_antenna_filtered = df_antenna[df_antenna['NUM_PIT'] != df_antenna['NUM_PIT']]
            else:
                individuals = df[df['LIEU_DIT'] == selected_site_antenna]['NUM_PIT'].unique()
                df_antenna_filtered = df[df['NUM_PIT'].isin(individuals)]

            st.dataframe(df_antenna_filtered[['DEPARTEMENT', 'LIEU_DIT']].drop_duplicates().reset_index(drop = True))

        with col1:
            if on:
                create_trajectories_map(df_antenna_filtered, width = 900, height = 1000)
            else:
                plot_trajectories_from_site(df_antenna_filtered, selected_site_antenna, width = 900, height = 1000)

with tab3:
    st.header("Statistiques phénologiques")
    gant_diagram(df_antenna)
    
with tab4:
    st.markdown("Work In Progress")