classDiagram
    %% Table df_controls
    class df_controls {
        + DATE
        + ANNEE
        + HEURE
        + COMMUNE
        + LIEU_DIT
        + DEPARTEMENT
        + LONG_L93
        + LAT_L93
        + CODE_ESP
        + SEXE
        + AGE
        + ACTION
        + NUM_PIT
        + ETUDE
    }

    %% Table df_individus
    class df_individus {
        + DATE
        + ANNEE
        + DEPARTEMENT
        + COMMUNE
        + LIEU_DIT
        + CODE_ESP
        + SEXE
        + AGE
        + NUM_PIT
        + ETUDE
        + AGE_CLASS (calculé)
    }

    %% Table df_mapping_regions
    class df_mapping_regions {
        + Département
        + Ancienne Région
        + Nouvelle Région
        + DPT_str
    }

    %% Table df_sites
    class df_sites {
        + COMMUNE
        + LIEU_DIT
        + DEPARTEMENT
        + LONG_L93
        + LAT_L93
        + LONG_WGS (calculé)
        + LAT_WGS (calculé)
        + NOUVELLE_REGION (jointure)
        + ANCIENNE_REGION (jointure)
    }

    %% Table df_distances
    class df_distances {
        + NUM_PIT
        + CODE_ESP
        + DATE_DEPART
        + SITE_DEPART
        + DATE_ARRIVEE
        + SITE_ARRIVEE
        + DIST_KM
        + DPT_DEPART
        + LAT_DEPART
        + LONG_DEPART
        + DPT_ARRIVEE
        + LAT_ARRIVEE
        + LONG_ARRIVEE
    }

    %% Relation : df_sites récupère les colonnes NOUVELLE_REGION et ANCIENNE_REGION depuis df_mapping_regions (jointure par DEPARTEMENT)
    df_sites --> df_mapping_regions : jointure (par DEPARTEMENT)
