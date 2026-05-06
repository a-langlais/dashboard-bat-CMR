import { Activity, BarChart3, Map, Radar } from "lucide-react";

type PartnerLogo = {
  file: string;
  alt: string;
};

type PartnerGroup = {
  title: string;
  logos: PartnerLogo[];
};

const topPartnerGroups: PartnerGroup[] = [
  {
    title: "Financeurs",
    logos: [
      { file: "FEDER-NA.png", alt: "FEDER Nouvelle-Aquitaine" },
      { file: "Prefet_NA.jpg", alt: "Prefet Nouvelle-Aquitaine" },
      { file: "FranceNationVerte.jpg", alt: "France Nation Verte" },
      { file: "CaisseEpargne.png", alt: "Caisse d'Epargne" },
      { file: "FRhinos.png", alt: "Fonds de dotation Rhinos" },
      { file: "FHumus.jpg", alt: "Fondation Humus" },
    ],
  },
  {
    title: "Coordination administrative & technique",
    logos: [
      { file: "FNENA.png", alt: "France Nature Environnement Nouvelle-Aquitaine" },
      { file: "PCN.jpg", alt: "Poitou-Charentes Nature" },
      { file: "NE17.jpg", alt: "Nature Environnement 17" },
    ],
  },
  {
    title: "Coordination techniques territoriales",
    logos: [
      { file: "DSNE.jpg", alt: "Deux-Sèvres Nature Environnement" },
      { file: "CN.png", alt: "Charente Nature" },
      { file: "VN.png", alt: "Vienne Nature" },
      { file: "LPOFrance.jpg", alt: "LPO France" },
      { file: "NE17.jpg", alt: "Nature Environnement 17" },
      { file: "GCA.jpg", alt: "Groupe Chiroptères Aquitaine" },
      { file: "CistudeNature.jpg", alt: "Cistude Nature" },
      { file: "CENNA.jpg", alt: "Conservatoire d'espaces naturels Nouvelle-Aquitaine" },
      { file: "SEPANLOG.jpg", alt: "SEPANLOG" },
      { file: "GMHL.png", alt: "Groupe Mammalogique et Herpétologique du Limousin" },
    ],
  },
];

const bottomPartnerGroups: PartnerGroup[] = [
  {
    title: "Partenaires scientifiques & techniques",
    logos: [
      { file: "LBBE.png", alt: "LBBE" },
      { file: "CNRS.png", alt: "CNRS" },
      { file: "InstitutPasteur.jpg", alt: "Institut Pasteur" },
      { file: "anses.jpg", alt: "Anses" },
      { file: "CESCO.png", alt: "CESCO" },
      { file: "MNHN.png", alt: "Muséum national d'Histoire naturelle" },
      { file: "UDBarcelona.png", alt: "Universitat de Barcelona" },
      { file: "UDNeuchatel.png", alt: "Université de Neuchâtel" },
      { file: "UDPaisVasco.png", alt: "Universidad del Pais Vasco" },
    ],
  },
  {
    title: "Partenaires associatifs & institutionnels",
    logos: [
      { file: "GCPDL.jpg", alt: "Groupe Chiroptères Pays de la Loire" },
      { file: "CSA.png", alt: "Conservatoire d'espaces naturels Alsace" },
      { file: "GCP.jpg", alt: "Groupe Chiroptères Provence" },
      { file: "GCMP.jpg", alt: "Groupe Chiroptères Midi-Pyrénées" },
      { file: "CENA.png", alt: "Conservatoire d'espaces naturels Auvergne" },
      { file: "LPOARA.jpg", alt: "LPO Auvergne-Rhone-Alpes" },
      { file: "LPOCVDL.jpg", alt: "LPO Centre-Val de Loire" },
      { file: "LPOTouraine.png", alt: "LPO Touraine" },
      { file: "CMNF.png", alt: "Coordination Mammalogique du Nord de la France" },
      { file: "GMN.jpg", alt: "Groupe Mammalogique Normand" },
      { file: "CDS46.png", alt: "Comite departemental de speleologie du Lot" },
      { file: "amikiro.png", alt: "Amikiro" },
      { file: "PNRMP.jpg", alt: "Parc naturel régional Millevaches en Limousin" },
      { file: "PNRPL.jpg", alt: "Parc naturel régional Périgord-Limousin" },
      { file: "PNRMVL.jpg", alt: "Parc naturel régional Marais poitevin" },
      { file: "PNRLDG.png", alt: "Parc naturel régional Landes de Gascogne" },
      { file: "PNNPyrenees.png", alt: "Parc national des Pyrénées" },
      { file: "ONF.png", alt: "Office national des forêts" },
      { file: "IndreNature.png", alt: "Indre Nature" },
      { file: "GMIEL.png", alt: "GMIEL" },
    ],
  },
];

const modules = [
  { icon: Map, title: "Cartographie", text: "Trajectoires filtrees et carte canvas." },
  { icon: Activity, title: "Phenologie", text: "Presences par site et par periode." },
  { icon: BarChart3, title: "Statistiques", text: "KPI, especes, frequences, distances." },
  { icon: Radar, title: "Fiche site", text: "Vue detaillee par site equipe." },
];

export function HomePage() {
  return (
    <section className="home-page">
      <PartnerGroups groups={topPartnerGroups} />
      <div className="home-layout">
        <div className="home-copy">
          <p className="eyebrow">Outil de visualisation</p>
          <h1>Exploration des données de CMR</h1>
          <p>
            Exploration interactive des trajectoires, phénologies de présence et statistiques
            descriptives issues des données actuelles.
          </p>
        </div>
        <div className="home-panels" aria-label="Modules disponibles">
          {modules.map((item) => (
            <article key={item.title}>
              <item.icon size={22} />
              <strong>{item.title}</strong>
              <span>{item.text}</span>
            </article>
          ))}
        </div>
      </div>
      <PartnerGroups groups={bottomPartnerGroups} />
    </section>
  );
}

function PartnerGroups({ groups }: { groups: PartnerGroup[] }) {
  return (
    <div className="partner-groups">
      {groups.map((group) => (
        <fieldset className="partner-fieldset" key={group.title}>
          <legend>{group.title}</legend>
          <div className="partner-logo-strip">
            {group.logos.map((logo) => (
              <img key={logo.file} src={logoUrl(logo.file)} alt={logo.alt} loading="lazy" />
            ))}
          </div>
        </fieldset>
      ))}
    </div>
  );
}

function logoUrl(file: string) {
  return new URL(`../../images/${file}`, import.meta.url).href;
}
