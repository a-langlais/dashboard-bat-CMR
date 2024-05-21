import streamlit as st
import pandas as pd
from custom_functions import create_interactive_map, create_trajectories_map, gant_diagram_site, plot_trajectories_from_site, gant_diagram, distance_parcourue_par_individu, haversine_distance
import plotly.express as px
import plotly.graph_objects as go


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

        if select_dept is not None:
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
                create_interactive_map(df_filtered, height = 1000)
        else:
            with col1:
                create_interactive_map(df_filtered, height = 1000)
            with col2:    
                st.warning("Veuillez sélectionner au moins un département", icon="⚠️")

with tab2:
    col1, col2 = st.columns([0.55, 0.45])
    
    with col2:
        st.header("Paramètres")
        on = st.radio("Choix de visualisation par :",
                      ["Site", "Individu"],
                      captions = ["Sites interconnectés", "Trajectoires des individus"],
                      horizontal = True)

        if on == "Individu":
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

            def get_infos(individu, df):
                table = []
                for ind in individu:
                    table_ind = {
                        'NUM_PIT': ind,
                        'ORIGINE': df[df['NUM_PIT'] == ind]['LIEU_DIT'].iloc[0],
                        'VISITED_SITES': df[df['NUM_PIT'] == ind]['LIEU_DIT'].nunique(),
                        'YEAR_MARKED': pd.to_datetime(df[df['NUM_PIT'] == ind]['ANNEE'], format='%Y').min(),  # Convertir en datetime
                        'DISTANCE_TRAVELED': round(distance_parcourue_par_individu(df[df['NUM_PIT'] == ind]), 2),
                        'DISTANCE_BY_YEAR': round(distance_parcourue_par_individu(df[df['NUM_PIT'] == ind]) / (df[df['NUM_PIT'] == ind]['ANNEE'].max() - df[df['NUM_PIT'] == ind]['ANNEE'].min()), 2)
                    }
                    table.append(table_ind)
                df_result = pd.DataFrame(table)
                df_result['YEAR_MARKED'] = df_result['YEAR_MARKED'].dt.strftime('%Y')  
                return st.dataframe(df_result)

            if select_inds:
                start_year, end_year = selected_years
                df_antenna_filtered = df_antenna[df_antenna['NUM_PIT'].isin(select_inds)]
                df_antenna_filtered = df_antenna_filtered[(df_antenna_filtered['ANNEE'] >= start_year) & (df_antenna_filtered['ANNEE'] <= end_year)]
                get_infos(select_inds, df_antenna_filtered)
                gant_diagram_site(df_antenna_filtered)
            else:
                df_antenna_filtered = df_antenna[df_antenna['NUM_PIT'] != df_antenna['NUM_PIT']]
                st.warning("Veuillez sélectionner au moins un individu", icon="⚠️")
        elif on == "Site":
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
                st.warning("Veuillez sélectionner un site", icon="⚠️")
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

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        total_captured = len(df[(df['ACTION'] == 'T') | (df['ACTION'] == 'C')])
        st.metric(label="Individus capturés", value = total_captured)

        recaptured = round(df[df['ACTION'] == 'R']['NUM_PIT'].nunique(), 3)
        percent_recaptured = round((recaptured / total_captured) * 100, 3) if total_captured != 0 else 0
        st.metric(label = "Individus recapturés", 
                value = recaptured, 
                delta = f"{percent_recaptured} %",
                )

    with col2:
        total_marked = df[df['ACTION'] == 'T']['NUM_PIT'].nunique()
        st.metric(label = "Individus marqués", value = total_marked)
       
        controled = df_antenna['NUM_PIT'].nunique()
        percent_controled = round((controled / total_marked) * 100, 3) if total_marked != 0 else 0
        st.metric(label = "Individus contrôlés", value = controled, delta = f"{percent_controled} %")

    with col3:
        sites_capture = df['LIEU_DIT'].nunique()
        st.metric(label = "Sites capturés", value = sites_capture)

        sites_antennes = df_antenna['LIEU_DIT'].nunique()
        st.metric(label = "Sites contrôlés", value = sites_antennes)   

    col1, col2 = st.columns([1, 2])

    with col1:
        ## BARRE EMPILEE PAR ANNEE
        df_antenna['YEAR'] = df_antenna['DATE'].dt.year
        grouped_data = df_antenna.groupby(['YEAR', 'CODE_ESP']).size().reset_index(name='Detections')

        fig = px.bar(grouped_data, x='YEAR', y='Detections', color='CODE_ESP',
                    title="Nombre de détections par année et par espèce",
                    labels={'Detections': 'Nombre de détections', 'YEAR': 'Année', 'CODE_ESP': 'Espèce'},
                    )

        fig.update_layout(xaxis_title='Année',
                        yaxis_title='Nombre de détections',
                        xaxis={'type': 'category'},  # Assurez-vous que l'axe des x est traité comme des catégories
                        barmode='stack',
                        width = 400) 

        # Afficher le graphique
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        ## COURBES FREQUENCES DETECTIONS
        df_antenna['MONTH_DAY'] = df_antenna['DATE'].dt.strftime('%m-%d')  # Cela crée une chaîne de caractères 'MM-DD'
        global_freq = df_antenna.groupby('MONTH_DAY').size().reset_index(name='Global Detections')

        # Calculer les fréquences par site
        site_freq = df_antenna.groupby(['MONTH_DAY', 'LIEU_DIT']).size().reset_index(name='Detections')
        sites = site_freq['LIEU_DIT'].unique()

        # Préparer l'ordre chronologique
        months_days = pd.date_range('2021-01-01', '2021-12-31').strftime('%m-%d')
        global_freq['MONTH_DAY'] = pd.Categorical(global_freq['MONTH_DAY'], categories=months_days, ordered=True)
        global_freq = global_freq.sort_values('MONTH_DAY')

        # Création du graphique
        fig2 = go.Figure()

        # Ajouter la courbe globale
        fig2.add_trace(go.Scatter(x=global_freq['MONTH_DAY'], y=global_freq['Global Detections'],
                                mode='lines', name='Global'))

        # Ajouter une courbe pour chaque site
        for site in sites:
            site_data = site_freq[site_freq['LIEU_DIT'] == site]
            site_data['MONTH_DAY'] = pd.Categorical(site_data['MONTH_DAY'], categories=months_days, ordered=True)
            site_data = site_data.sort_values('MONTH_DAY')
            fig2.add_trace(go.Scatter(x=site_data['MONTH_DAY'], y=site_data['Detections'],
                                    mode='lines', name=site))

        # Mise à jour du layout
        fig2.update_layout(
            title='Fréquence de détection en fonction du jour de l\'année par site',
            xaxis_title='Jour de l\'année',
            yaxis_title='Nombre de détections',
            xaxis=dict(type='category', categoryorder='array', categoryarray=[md for md in months_days]),
            #yaxis=dict(range=[0, global_freq['Global Detections'].max() + 10])
        )
        st.plotly_chart(fig2, use_container_width=True)

    col1, col2 = st.columns([1, 1])
    
    with col1:
        ## PIEPLOT PROPORTION DESPECES CONTROLEES
        species_counts = df_antenna['CODE_ESP'].value_counts().reset_index()
        species_counts.columns = ['Species', 'Count']

        # Créer un diagramme circulaire
        fig3 = px.pie(species_counts, 
                    values='Count', names='Species', 
                    title="Proportion d'espèces détectées",
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    hole = 0.5,)

        # Personnalisation supplémentaire
        fig3.update_traces(textposition='outside', textinfo='percent+label', insidetextorientation='radial')
        fig3.update_layout(legend_title_text='Espèce',
                        margin=dict(t=150, b=150, l=0, r=0),
                        showlegend = False
                            )
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        ##PIEPLOT PROPORTION DESPECES MARQUEES
        marked_species = df[df['ACTION'] == 'T']
        species_counts = marked_species['CODE_ESP'].value_counts().reset_index()
        species_counts.columns = ['Species', 'Count']

        # Créer un diagramme circulaire
        fig4 = px.pie(species_counts, 
                    values='Count', names='Species', 
                    title="Proportion d'espèces marquées",
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    hole = 0.5)

        # Personnalisation supplémentaire
        fig4.update_traces(textposition='outside', textinfo='percent+label', insidetextorientation='radial')
        fig4.update_layout(legend_title_text='Espèce',
                        margin=dict(t=150, b=150, l=0, r=0),
                        showlegend = False
                            )
        st.plotly_chart(fig4, use_container_width=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        ## DIAGRAMME TOP 5 LES PLUS DETECTEES
        df_antenna['NUM_PIT'] = "n° " + df_antenna['NUM_PIT'].astype(str)

        # Obtenir les cinq catégories les plus fréquentes avec leurs occurrences
        top_categories = df_antenna['NUM_PIT'].value_counts().head(10)

        # Créer un DataFrame à partir des cinq premières catégories
        df_top_categories = pd.DataFrame({'NUM_PIT': top_categories.index, 'Occurrences': top_categories.values})
        df_top_categories = df_top_categories.sort_values(by='Occurrences', ascending=False)

        # Créer le diagramme en barres horizontales avec Plotly Express
        fig5 = px.bar(df_top_categories, x='Occurrences', y='NUM_PIT', orientation='h',
                    title='TOP 10 des individus les plus contrôlés',
                    labels={'Occurrences': 'Nombre d\'occurrences', 'NUM_PIT': 'Catégories'},
                    color='NUM_PIT', color_discrete_sequence = px.colors.qualitative.Pastel,)

        fig5.update_layout(showlegend=False)

        st.plotly_chart(fig5, use_container_width=True)

    with col2:
        ## TABLEAU DETAILLES DES 10 INDIVIDUS
        num_pit_counts = df_antenna['NUM_PIT'].value_counts()

        # Liste pour stocker les informations sur les 10 NUM_PIT les plus détectés
        num_pit_info = []

        # Pour chaque NUM_PIT, calculer les informations requises
        for num_pit in num_pit_counts.head(10).index:  
            num_pit_data = df_antenna[df_antenna['NUM_PIT'] == num_pit]
            origin_site = num_pit_data['LIEU_DIT'].iloc[0]  # Site d'origine
            visited_sites = num_pit_data['LIEU_DIT'].nunique()  # Nombre de sites différents visités
            year_marked = num_pit_data['YEAR'].min(),
            years_monitored = num_pit_data['YEAR'].max() - num_pit_data['YEAR'].min()
            
            # Calculer la distance parcourue par l'individu
            distance_traveled = distance_parcourue_par_individu(num_pit_data)
            
            # Calculer la distance moyenne par an
            if year_marked != 0:
                distance_by_year = distance_traveled / years_monitored
            else:
                distance_by_year = 0
            
            # Ajouter les informations au dictionnaire
            num_pit_info.append({'NUM_PIT': num_pit, 'Origin_Site': origin_site, 
                                'Visited_Sites': visited_sites, 'Year_Marked': year_marked, 'Years_Monitored' : years_monitored,
                                'Distance_Traveled': round(distance_traveled, 2),
                                'Distance_by_year': round(distance_by_year, 2)})

        # Créer un DataFrame avec ces informations
        df_top_num_pit_info = pd.DataFrame(num_pit_info)

        # Afficher le DataFrame
        st.dataframe(df_top_num_pit_info, use_container_width=True)

    
    
    