## Fiche site

<|selector|label=Site antenne|value={selection_fiche}|lov={liste_sites_antennes}|dropdown|on_change=update_fiche|>

<|layout|columns=1 5|
<|part|class_name=kpi-container|
<|raw|
<div class="titre-container">
    <h1 class="titre-modern">Individus marqués</h1>
    <div class="ligne-soulignement"></div>
</div>
|>
<|text|value={total_marked_fiche}|class_name=kpi-value|>

<|raw|
<div class="titre-container">
    <h1 class="titre-modern">Individus contrôlés</h1>
    <div class="ligne-soulignement"></div>
</div>
|>
<|text|value={total_recaptured_fiche}|class_name=kpi-value|>
|>

<|part|class_name=card|
<|layout|columns=1 1 1|
<|part|
<|raw|
<div class="titre-container">
    <h1 class="titre-modern">Individus capturés</h1>
    <div class="ligne-soulignement"></div>
</div>
|>
<|chart|figure={plot_capture_year_fiche}|>
|>
<|part|
<|raw|
<div class="titre-container">
    <h1 class="titre-modern">Individus contrôlés</h1>
    <div class="ligne-soulignement"></div>
</div>
|>
<|chart|figure={plot_control_year_fiche}|>
|>
<|part|
<|raw|
<div class="titre-container">
    <h1 class="titre-modern">Individus détectés</h1>
    <div class="ligne-soulignement"></div>
</div>
|>
<|chart|figure={plot_detection_year_fiche}|>
|>
|>
|>
|>

<|layout|columns=2 3|
<|part|class_name=card|
<|raw|
<div class="titre-container">
    <h1 class="titre-modern">Durée de présence</h1>
    <div class="ligne-soulignement"></div>
</div>
|><|chart|figure={gant_diagram_fiche}|>
<|raw|
<div class="titre-container">
    <h1 class="titre-modern">Fréquences de détection</h1>
    <div class="ligne-soulignement"></div>
</div>
|>
<|chart|figure={plot_frequencies_fiche}|>
|>

<|part|content={map_fiche}|height=100%|width=100%|>
|>
