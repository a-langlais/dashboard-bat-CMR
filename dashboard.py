import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

COULEURS_ESPECES = {
    'MINSCH': '#1f77b4',  # Bleu
    'RHIFER': '#2ca02c',  # Vert
    'MYOEMA': '#d62728',  # Rouge
    'RHIEUR': '#9467bd',  # Violet
    'MYONAT': '#ff7f0e',  # Orange
    'MYODAU': '#8c564b'   # Brun
}

def detection_by_year(df_controls):
    df_controls['DATE'] = pd.to_datetime(df_controls['DATE'], errors='coerce')
    df_controls['YEAR'] = df_controls['DATE'].dt.year
    grouped_data = df_controls.groupby(['YEAR', 'CODE_ESP']).size().reset_index(name = 'Detections').sort_values('YEAR')
    
    fig = px.bar(grouped_data, x = 'YEAR', y = 'Detections', color = 'CODE_ESP', color_discrete_map = COULEURS_ESPECES,
                 labels = {'Detections': 'Nombre de détections', 'CODE_ESP': 'Espèce'},
                 )

    fig.update_layout(
        height = 400,
        width = 400,
        yaxis_title = 'Nombre de détections',
        xaxis_title = None,
        xaxis = {'type': 'linear', 'tickmode': 'linear', 'dtick': 1},
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

def capture_by_year(df_captures):
    df_filtre = df_captures.copy()
    df_filtre['YEAR'] = df_filtre['DATE'].dt.year
    df_grouped = df_filtre.groupby(['YEAR', 'CODE_ESP'])['NUM_PIT'].nunique().reset_index().sort_values('YEAR')
    df_grouped.rename(columns = {'NUM_PIT': 'Nombre d\'individus uniques'}, inplace = True)
    
    fig = px.bar(df_grouped, x = 'YEAR', y = 'Nombre d\'individus uniques', color = 'CODE_ESP', color_discrete_map = COULEURS_ESPECES,
                 labels = {'Nombre d\'individus uniques': 'Nombre d\'individus uniques', 'CODE_ESP': 'Espèce'}
                 )

    fig.update_layout(
        height = 400,
        width = 400,
        yaxis_title = 'Nombre d\'individus uniques',
        xaxis_title = None,
        xaxis = {'type': 'linear', 'tickmode': 'linear', 'dtick': 1},
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

def control_by_year(df_controls):
    df_filtre = df_controls.copy()
    df_filtre['DATE'] = pd.to_datetime(df_filtre['DATE'], errors='coerce')
    df_filtre['YEAR'] = df_filtre['DATE'].dt.year
    df_grouped = df_filtre.groupby(['YEAR', 'CODE_ESP'])['NUM_PIT'].nunique().reset_index().sort_values('YEAR')
    df_grouped.rename(columns = {'NUM_PIT': 'Nombre d\'individus'}, inplace = True)
    
    fig = px.bar(df_grouped, x = 'YEAR', y = 'Nombre d\'individus', color = 'CODE_ESP', color_discrete_map = COULEURS_ESPECES,
                 labels = {'Nombre d\'individus': 'Nombre d\'individus', 'CODE_ESP': 'Espèce'},
                 )

    fig.update_layout(
        height = 400,
        width = 400,
        yaxis_title = 'Nombre d\'individus',
        xaxis_title = None,
        xaxis = {'type': 'linear', 'tickmode': 'linear', 'dtick': 1},
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

def detection_frequencies(df_controls):
    df_controls['DATE'] = pd.to_datetime(df_controls['DATE'], errors='coerce')
    df_controls['MONTH_DAY'] = df_controls['DATE'].dt.strftime('%m-%d')
    global_freq = df_controls.groupby('MONTH_DAY').size().reset_index(name = 'Global Detections')

    # Calculer les fréquences par site
    site_freq = df_controls.groupby(['MONTH_DAY', 'LIEU_DIT']).size().reset_index(name = 'Detections')
    sites = site_freq['LIEU_DIT'].unique()

    # Préparer l'ordre chronologique
    months_days = pd.date_range('2021-01-01', '2021-12-31').strftime('%m-%d')
    global_freq['MONTH_DAY'] = pd.Categorical(global_freq['MONTH_DAY'], categories = months_days, ordered = True)
    global_freq = global_freq.sort_values('MONTH_DAY')

    # Création du graphique
    fig = go.Figure()

    if len(site_freq['LIEU_DIT'].unique()) > 1:
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

def detection_frequencies_global(df_controls):
    df_controls['DATE'] = pd.to_datetime(df_controls['DATE'], errors='coerce')
    df_controls['MONTH_DAY'] = df_controls['DATE'].dt.strftime('%m-%d')
    global_freq = df_controls.groupby('MONTH_DAY').size().reset_index(name = 'Global Detections')

    # Calculer les fréquences par site
    site_freq = df_controls.groupby(['MONTH_DAY', 'LIEU_DIT']).size().reset_index(name = 'Detections')
    sites = site_freq['LIEU_DIT'].unique()

    # Préparer l'ordre chronologique
    months_days = pd.date_range('2021-01-01', '2021-12-31').strftime('%m-%d')
    global_freq['MONTH_DAY'] = pd.Categorical(global_freq['MONTH_DAY'], categories = months_days, ordered = True)
    global_freq = global_freq.sort_values('MONTH_DAY')

    # Création du graphique
    fig = go.Figure()

    # Ajouter la courbe globale
    fig.add_trace(go.Scatter(x = global_freq['MONTH_DAY'], y = global_freq['Global Detections'], mode = 'lines', name = 'Global'))

    # Mise à jour du layout
    fig.update_layout(
        xaxis_title = 'Jour de l\'année',
        yaxis_title = 'Nombre de détections',
        xaxis = dict(type = 'category', categoryorder = 'array', categoryarray = [md for md in months_days]),
        legend = dict(bgcolor = 'rgba(0, 0, 0, 0)'),
        #yaxis = dict(range = [0, global_freq['Global Detections'].max() + 10])
    )
    return fig

def pie_controled(df_controls):
    species_counts = df_controls['CODE_ESP'].value_counts().reset_index()
    species_counts.columns = ['Species', 'Count']

    # Créer un diagramme circulaire
    fig = px.pie(species_counts, 
                values = 'Count', names = 'Species', color = 'Species',
                color_discrete_map = COULEURS_ESPECES,
                hole = 0.5,)

    # Personnalisation supplémentaire
    fig.update_layout(legend_title_text = 'Espèce',
                    showlegend = True,
                    legend = dict(bgcolor = 'rgba(0, 0, 0, 0)')
                        )
    return fig

def pie_marked(df_individus):
    marked_species = df_individus.copy()
    species_counts = marked_species['CODE_ESP'].value_counts().reset_index()
    species_counts.columns = ['Species', 'Count']

    # Créer un diagramme circulaire
    fig = px.pie(species_counts, 
                values = 'Count', names = 'Species', color = 'Species',
                color_discrete_map = COULEURS_ESPECES,
                hole = 0.5)

    # Personnalisation supplémentaire
    fig.update_layout(legend_title_text = 'Espèce',
                    showlegend = True,
                    legend = dict(bgcolor = 'rgba(0, 0, 0, 0)')
                        )
    return fig

def top_detection(df_controls):
    df_controls['NUM_PIT'] = "n° " + df_controls['NUM_PIT'].astype(str)

    # Obtenir les dix catégories les plus fréquentes avec leurs occurrences
    top_categories = df_controls['NUM_PIT'].value_counts().head(10)

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

def distance_boxplot(df_distances):
    fig = px.box(
        df_distances,
        x = 'CODE_ESP',
        y = 'DIST_KM',
        color = 'CODE_ESP',  # Utilisation des couleurs basées sur les espèces
        color_discrete_map = COULEURS_ESPECES,
        title = ''
    )

    fig.update_layout(
        xaxis_title = '',
        yaxis_title = 'Distance entre deux sites (km)',
        showlegend = False
    )

    return fig