## Visualisation des données d'antennes

<|layout|columns=1 2|
<|
<|selector|label=Département|value={selected_dpt}|lov={departements}|dropdown|multiple|>
<|selector|label=Espèce|value={selected_sp}|lov={species}|dropdown|multiple|>
<|selector|label=Sexe|value={selected_gender}|lov={genders}|dropdown|multiple|>
<|selector|label=Site|value={selected_sites}|lov={sites}|dropdown|multiple|>
<|date_range|dates={selected_dates}|>

<|Actualisation|button|class_name=plain|on_action=refresh_button|>
|>

<|chart|figure={map_section}|>
|>
