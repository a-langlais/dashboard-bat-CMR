## Statistiques analytiques

<|layout|columns=1 2 3|
<|part|class_name=kpi-container|

<|raw|
<div class="titre-container">
    <h1 class="titre-modern">Individus marqués</h1>
    <div class="ligne-soulignement"></div>
</div>
|>
<|text|value={total_marked}|class_name=kpi-value|>

<|raw|
<div class="titre-container">
    <h1 class="titre-modern">Individus contrôlés</h1>
    <div class="ligne-soulignement"></div>
</div>
|>
<|text|value={total_recaptured}|class_name=kpi-value|>

<|raw|
<div class="titre-container">
    <h1 class="titre-modern">Sites capturés</h1>
    <div class="ligne-soulignement"></div>
</div>
|>
<|text|value={sites_capture}|class_name=kpi-value|>

<|raw|
<div class="titre-container">
    <h1 class="titre-modern">Sites contrôlés positifs</h1>
    <div class="ligne-soulignement"></div>
</div>
|>
<|text|value={sites_antennes}|class_name=kpi-value|>
|>

<|part|class_name=kpi-container|
<|raw|
<div class="titre-container">
    <h1 class="titre-modern">Proportion d'espèces détectées</h1>
    <div class="ligne-soulignement"></div>
</div>
|>
<|chart|figure={plot_pie_controled}|>
|>

<|part|class_name=kpi-container|
<|raw|
<div class="titre-container">
    <h1 class="titre-modern">Fréquence des détections par jour de l'année</h1>
    <div class="ligne-soulignement"></div>
</div>
|>
<|chart|figure={plot_frequencies}|>
|>
|>

<|layout|columns=2 4|
<|part|class_name=kpi-container|
<|raw|
<div class="titre-container">
    <h1 class="titre-modern">Proportion d'espèces marquées</h1>
    <div class="ligne-soulignement"></div>
</div>
|>
<|chart|figure={plot_pie_marked}|>
|>
<|part|class_name=kpi-container|
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
<|part|class_name=kpi-container|
<|raw|
<div class="titre-container">
    <h1 class="titre-modern">Répartition des distances par espèce</h1>
    <div class="ligne-soulignement"></div>
</div>
|>
<|chart|figure={plot_box_distances}|>
|>
<|part|class_name=kpi-container|
<|raw|
<div class="titre-container">
    <h1 class="titre-modern">Table des trajectoires</h1>
    <div class="ligne-soulignement"></div>
</div>
|>
<|table|data={transition_table_plot}|height=400px|>
|>
|>
