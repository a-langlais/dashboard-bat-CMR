## Statistiques analytiques

<|layout|columns=1 2 3|
<|part|class_name=card|

<|text|value=Individus marqués|class_name=title|>
<|text|value={total_marked}|class_name=values|>

<|text|value=Individus contrôlés|class_name=title|>
<|text|value={total_recaptured}|class_name=values|>

<|text|value=Nombre de sites de capture|class_name=title|>
<|text|value={sites_capture}|class_name=values|>

<|text|value=Nombre de sites contrôlés positifs|class_name=title|>
<|text|value={sites_antennes}|class_name=values|>
|>

<|part|class_name=card|
<|text|value=Proportion d'espèces détectées|class_name=title|>
<|chart|figure={plot_pie_controled}|>
|>
<|part|class_name=card|
<|text|value=Proportion d'espèces détectées|class_name=title|>

<|chart|figure={plot_frequencies}|>
|>
|>

<|layout|columns=2 4|
<|part|class_name=card|
<|text|value=Proportion d'espèces marquées|class_name=title|>

<|chart|figure={plot_pie_marked}|>
|>
<|part|class_name=card|
<|layout|columns=1 1 1|
<|part|
<|text|value=Individus capturés par année et par espèce|class_name=title|>
<|chart|figure={plot_capture_year}|>
|>
<|part|
<|text|value=Individus contrôlés par année et par espèce|class_name=title|>
<|chart|figure={plot_control_year}|>
|>
<|part|
<|text|value=Détections par année et par espèce|class_name=title|>
<|chart|figure={plot_detection_year}|>
|>
|>
|>
|>

<|layout|columns=2 4|
<|part|class_name=card|
<|text|value=Répartition des distances par espèce|class_name=title|>
<|chart|figure={plot_box_distances}|>

|>
<|part|class_name=card|
<|text|value=Table des trajectoires|class_name=title|>
<|table|data={transition_table_plot}|height=400px|>
|>
|>