## Fiche site

<|selector|label=Site antenne|value={selection_fiche}|lov={liste_sites_antennes}|dropdown|on_change=update_fiche|>

<|layout|columns=1 3|
<|part|class_name=card|
<|text|value=Individus marqués|class_name=title|>
<|text|value={total_marked_fiche}|class_name=values|>

<|text|value=Individus contrôlés|class_name=title|>
<|text|value={total_recaptured_fiche}|class_name=values|>
|>

<|part|class_name=card|
<|layout|columns=1 1 1|
<|part|
<|text|value=Individus capturés par année et par espèce|class_name=title|>
<|chart|figure={plot_capture_year_fiche}|>
|>
<|part|
<|text|value=Individus contrôlés par année et par espèce|class_name=title|>
<|chart|figure={plot_control_year_fiche}|>
|>
<|part|
<|text|value=Détections par année et par espèce|class_name=title|>
<|chart|figure={plot_detection_year_fiche}|>
|>
|>
|>
|>

<|layout|columns=2 3|
<|part|class_name=card|
<|text|value=Durée de présence|class_name=title|>
<|chart|figure={gant_diagram_fiche}|>
<|text|value=Courbes de fréquences|class_name=title|>
<|chart|figure={plot_frequencies_fiche}|>
|>

<|part|content={map_fiche}|height=100%|width=100%|>
|>
