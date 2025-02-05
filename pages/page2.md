## Visualisation des données d'antennes

<|layout|columns=1 2|
<|
<|Sélectionner un ou plusieurs département(s) pour limiter les trajectoires sur la carte.|>
<|selector|label=Département|value={selected_dpt}|lov={departements}|dropdown|multiple|>

<|Sélectionner la ou les espèces voulue(s).|>
<|selector|label=Espèce|value={selected_sp}|lov={species}|dropdown|multiple|>
<|selector|label=Sexe|value={selected_gender}|lov={genders}|dropdown|multiple|>

<|Séléctionner un site (possibilité de filtrer les sites par commune)|>
<|selector|label=Commune|value={selected_communes}|lov={communes}|dropdown|multiple|on_change=refresh_sites|>
<|selector|label=Site|value={selected_sites}|lov={sites}|dropdown|multiple|>

<|Sélectionner l'amplitude des dates voulues.|>
<|date_range|dates={selected_dates}|>

<|Actualisation|button|class_name=plain|on_action=refresh_map_button|>
|>

<|part|content={m}|height=800px|>
|>
