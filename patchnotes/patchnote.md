**Patch Note - Version 0.2**
**Date de publication** : 24/11/2024

**Fonctionnalités ajoutées :**

- Ajout d'un onglet "Fiche_site" permettant d'afficher quelques informations pour le moment sur un site particulier, dont une carte des sites connectés, d'un graph de présence annuelle et de quelques autres informations.
- Mise à jour de la base de données jusqu'au 18-11-2024

**Améliorations et modifications :**

- Nettoyage des données terminée
- Split des données en plusieurs tables pour faciliter les importation en attendant l'intégration d'une BDD dédiée
- Gain de performance significative par vectorisation des calculs
- Refonte du backend pour éviter la sur-solicitation du cache
- Refonte de la visualisation des cartes pour plus de clarté et facilité l'interprétabilité
- Retrait des "seuils de trajectoires" pour ne perdre aucune information

**Problèmes connus :**

- Quelques soucis d'affichage sur les petits écrans
- Exportation des cartes plus disponible pour le moment (mais possible via une simple capture d'écran)

> **Lien vers l'application en développement (build 0.2)** : https://huggingface.co/spaces/a-langlais/ccpna-taipy-dashboard

La version MVP via Streamlit (build 0.0) n'est plus hebergée.
_________________________________________________________________________________
_________________________________________________________________________________

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