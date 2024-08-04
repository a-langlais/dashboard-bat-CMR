## Statistiques analytiques

<|layout|columns=1 1 1|
<|
<|part|class_name=card|
<|text|value=Individus capturés|class_name=title|>

<|text|value={total_captured}|class_name=values|>
|>
<|part|class_name=card|
<|text|value=Individus marqués|class_name=title|>

<|text|value={total_marked}|class_name=values|>
|>
|>

<|
<|part|class_name=card|
<|text|value=Individus recapturés|class_name=title|>

<|text|value={total_recaptured}|class_name=values|>
|>
|>

<|
<|part|class_name=card|
<|text|value=Nombre de sites de capture|class_name=title|>

<|text|value={sites_capture}|class_name=values|>
|>
<|part|class_name=card|
<|text|value=Nombre de sites contrôlés|class_name=title|>

<|text|value={sites_antennes}|class_name=values|>
|>
|>
|>

<|layout|columns=1 1 1|
<|chart|figure={plot_capture_year}|>

<|chart|figure={plot_control_year}|>

<|chart|figure={plot_detection_year}|>
|>

<|layout|columns=1 1|
<|chart|figure={plot_frequencies}|>
|>

<|layout|columns=1 1|
<|chart|figure={plot_pie_controled}|>

<|chart|figure={plot_pie_marked}|>
|>

<|layout|columns=1 1|
<|chart|figure={plot_top_detection}|>

<|part|content={plot_chord_diagram}|>
|>
