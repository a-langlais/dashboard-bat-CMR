**Patch Note - Version 0.1**
**Date de publication** : 05/08/2024

**Fonctionnalités ajoutées :**

- Ajout de la possibilité de switcher du thème sombre au thème clair selon les préférences.
- Ajout d'une page de présentation du programme avec une ébauche de texte.
- Ajout du sexe des individus.
- Ajout de filtres synergiques pour naviguer plus facilement entre les sites concernant la phénologie temporelle.
- Ajout de deux graphiques en barre :
    * "Individus capturés par année et par espèce"
    * "Individus contrôlé par année et par espèce".
- Ajout d'un tableau résumé du nombre de trajets comptabilisés entre les sites.

**Améliorations et modifications :**

- Gain de performances significatif sur le traitement de l'algorithme avec des chargements jusqu'à 75% moins long.
- Modification de l'aspect global suite au changement de framework.
- Plusieurs modifications concernant la visualisation des trajectoires :
    * Les données des antennes et des captures/contrôles à la main ont été fusionnées donnant lieu un seul onglet global de visualisation des trajectoires.
    * Améliorations visuelles de la carte pour améliorer la lecture et les performances :
        * affichage seulement des trajectoires significatives (trajet entre deux sites ayant été réalisé au moins 10 fois sur les 7 dernières années tout individu confondu).
        * fond cartographique en N&B
        * code couleur des trajectoires proportionnel à l'intensité d'utilisation sur un gradient de couleur de gris à rouge.

- Modifications du fonctionnement de certains filtres :
    * "Département" : permet de sélectionner le ou les départements d'origine des individus.
    * "Site" : permet de sélectionner le ou les sites d'origine des individus.
- Correction de la signification des codes des données (C, M, R, T notamment).
- Meilleure disposition du tableau de bord des statistiques analytiques et amélioration de la lecture des graphiques.
- Les figures sont toujours interactives et vous pouvez interagir avec la légende pour afficher/masquer des catégories.

**Problèmes connus :**

- Nombreux NA concernant les données de sexe des individus -> nécessite une concaténation avec les données individuelles
- Seuil des trajectoires significatives déterminé arbitrairement selon la moyenne des trajectoires par pair de sites (mu ~ 10) -> à discuter
- Différence statistique notable entre les sites suivis 24/7 et les sites suivis ponctuellement -> pas touché pour le moment

**Lien vers l'application en développement (build 0.1)** : https://huggingface.co/spaces/a-langlais/ccpna-taipy-dashboard

> **Rappel** : Lien vers l'application précédente (build 0 - prototype) : https://huggingface.co/spaces/a-langlais/ccpna_dashboard