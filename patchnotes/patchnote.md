**Patch Note - Version 0.4**
**Date de publication** : 21/04/2025

**Fonctionnalités ajoutées :**

- Ajout de filtres pour les cartes : notamment âge à la capture et période du cycle de vie

**Améliorations et modifications :**

- Refonte graphique du design de l'application en vue de l'intégration future à l'appli de BDD du projet
- Changement sémantique de titres pour plus de clarté
- Retrait de la page "PRESENTATION" qui n'apportait pas de plus-value
- Sur l'onglet "CARTO_CMR" (anciennement "ANTENNES") : ajout de courtes descriptions des filtres
- sur l'onglet "PHENOLOGIE" : ne concerne maintenant que les données d'antenne fixe
- Sur l'onglet "STATISTIQUES" : changement du graphique en courbe pour une lecture simplifiée avec la fréquence de détection globale. Les courbes des sites individuels est toujours consultable sur l'onglet "FICHE_SITE"

**Problèmes connus :**

- En raison d'une BASE_SITES non définitive, il peut y avoir quelques erreurs concernant l'intitulé de certains sites, leur localisation ou le nombre de sites de captures et de sites contrôlés affichés dans l'onglet STATISTIQUES, merci de me le faire remonter si vous constatez quelque chose qui empêche l'utilisation de l'appli (ex : "La Brumaudière" <-> "Ancienne citerne à eau" <-> "Citerne de Sainte-Ouenne")
- La prochaine mise-à-jour portera sur l'ajout de nouveaux indicateurs stats et l'amélioration des cartes, je me base en priorité sur vos remarques et observations centralisée sur le fichier du drive

> **Lien vers l'application en développement (build 0.4)** : https://huggingface.co/spaces/a-langlais/ccpna-taipy-dashboard

_________________________________________________________________________________
_________________________________________________________________________________

**Patch Note - Version 0.3**
**Date de publication** : 05/02/2025

**Fonctionnalités ajoutées :**

- Ajout d'un pré-filtre COMMUNE avant de sélectionner un site sur l'onglet ANTENNES
- Mise-à-jour de la base de données avec les données disponibles jusqu'au 03-02-2025

**Améliorations et modifications :**

- L'onglet PHENOLOGIE ne concerne maintenant que les sites antennes
- Affichage du nom des sites par ordre alphabétique sur l'onglet FICHE_SITE
- L'onglet STATISTIQUES ne concerne maintenant que les données produites lors des études suivantes : ["Diag CEN", "Diag NATURA 2000", "Diag FDS_Oléron", "ECOFECT (GR/CCPNA)", "ECOFECT (Hors GR)", "TRANSPY ESPAGNE", "TRANSPY FRANCE"], ajout d'un sélecteur de programme pour afficher les statistiques prochainement
- Suppression du graphique "Individus les plus détectés" dans l'onglet STATISTIQUES
- Ajout du graphique intéractif "Répartition des distances par espèce" dans l'onglet STATISTIQUES
- Modification de la largeur de la table des distances pour une meilleure lecture
- Correction d'un bug qui empêchait certaines trajectoires de s'afficher pour certaines espèces (ex : MINSCH)
- Correction d'un bug qui affichait "0" à toutes les statistiques sur la Fiche_site de certains sites (ex : Grottes de Loubeau)

**Problèmes connus :**

- En raison d'une BASE_SITES non définitive, il peut y avoir quelques erreurs concernant l'intitulé de certains sites, leur localisation ou le nombre de sites de captures et de sites contrôlés affichés dans l'onglet STATISTIQUES, merci de me le faire remonter si vous constatez quelque chose qui empêche l'utilisation de l'appli (ex : "La Brumaudière" <-> "Ancienne citerne à eau" <-> "Citerne de Sainte-Ouenne")
- La prochaine mise-à-jour portera probablement sur l'interface : améliorer l'esthétique et le rendu dynamique de l'application

> **Lien vers l'application en développement (build 0.3)** : https://huggingface.co/spaces/a-langlais/ccpna-taipy-dashboard

La version MVP via Streamlit (build 0.0) n'est définitivement plus déployée mais le code source reste disponible.
_________________________________________________________________________________
_________________________________________________________________________________

**Patch Note - Version 0.2**
**Date de publication** : 24/11/2024

**Fonctionnalités ajoutées :**

- Ajout d'un onglet "Fiche_site" permettant d'afficher quelques informations pour le moment sur un site particulier, dont une carte des sites connectés, d'un graph de présence annuelle et de quelques autres informations.
- Mise-à-jour de la base de données jusqu'au 18-11-2024

**Améliorations et modifications :**

- Nettoyage des données terminée
- Split des données en plusieurs tables pour faciliter les importation en attendant l'intégration d'une BDD dédiée
- Gain de performance significative par vectorisation des calculs
- Refonte du backend pour éviter la sur-sollicitation du cache
- Refonte de la visualisation des cartes pour plus de clarté et facilité l'interprétabilité
- Retrait des "seuils de trajectoires" pour ne perdre aucune information

**Problèmes connus :**

- Quelques soucis d'affichage sur les petits écrans
- Exportation des cartes plus disponible pour le moment (mais possible via une simple capture d'écran)
- Retrait des étiquettes sur les marqueurs des cartes pour la visibilité en attendant une meilleure solution, bien sûr les noms restent disponible via l'interactivité

> **Lien vers l'application en développement (build 0.2)** : https://huggingface.co/spaces/a-langlais/ccpna-taipy-dashboard

La version MVP via Streamlit (build 0.0) ne sera bientôt plus hebergée.
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