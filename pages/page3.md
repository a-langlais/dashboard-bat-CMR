## Phénologie temporelle des sites

<|layout|columns=1 1|
<|selector|label=Département|value={selected_dpt_gant}|lov={departements}|dropdown|multiple|on_change=update_gant|>

<|date_range|dates={dates_gant}|on_change=update_gant|>
|>

<|chart|figure={gant_global}|>