## Visualisation des données d'antennes

<|layout|columns=1 2|gap=50px|
<|
<|raw|
<div class="titre-container">
    <h1 class="titre-modern">Limites administratives</h1>
    <div class="ligne-soulignement"></div>
</div>
|>
<|text|value=Ces paramètres permettent de filtrer les trajectoires en fonction de leur localisation administrative. Dans l'objectif de limiter l'affichage des trajectoires à celles passant dans certains départements ou régions.|class_name=citation|>
<|selector|label=Département|value={selected_dpt}|lov={departements}|dropdown|multiple|>

<|raw|
<div class="titre-container">
    <h1 class="titre-modern">Individus</h1>
    <div class="ligne-soulignement"></div>
</div>
|>
<|text|value=Ces paramètres permettent de filtrer les caractéristiques liés à l'espèce, l'âge à la capture ou le sexe des individus.|class_name=citation|>
<|selector|label=Espèce|value={selected_sp}|lov={species}|dropdown|multiple|>
<|selector|label=Sexe|value={selected_gender}|lov={genders}|dropdown|multiple|>

<|raw|
<div class="titre-container">
    <h1 class="titre-modern">Sites</h1>
    <div class="ligne-soulignement"></div>
</div>
|>
<|text|value=Ces paramètres permettent de filtrer les trajectoires en fonction du passage à un ou plusieurs sites en particulier. Si un individu est passé au moins une fois sur un des sites sélectionnés, toutes ses trajectoires seront affichées. Il est possible de sélectionner une commune afin de limiter le choix des sites.|class_name=citation|>
<|selector|label=Commune|value={selected_communes}|lov={communes}|dropdown|multiple|on_change=refresh_sites|>
<|selector|label=Site|value={selected_sites}|lov={sites}|dropdown|multiple|>

<|raw|
<div class="titre-container">
    <h1 class="titre-modern">Temporalité</h1>
    <div class="ligne-soulignement"></div>
</div>
|>
<|text|value=Ces paramètres permettent de saisir l'échelle de temps globale sur laquelle concentrer l'affichage des trajectoires (par défaut, toute la temporalité est conservée). Il est aussi possible de ne choisir l'affichage de seulement une ou plusieurs période (transit, parturition et hivernale).|class_name=citation|>
<|date_range|dates={selected_dates}|>

<|Mettre à jour la carte|button|class_name=plain|on_action=refresh_map_button|>
|>

<|part|content={m}|height=1000px|>
|>
