import { Activity, BarChart3, Map, Radar } from "lucide-react";
import federLogo from "../../images/FEDER-NA.png";
import franceNationVerteLogo from "../../images/FranceNationVerte.jpg";
import prefetLogo from "../../images/Prefet_NA.jpg";

const funders = [
  { src: prefetLogo, alt: "Prefet Nouvelle-Aquitaine" },
  { src: franceNationVerteLogo, alt: "France Nation Verte" },
  { src: federLogo, alt: "FEDER Nouvelle-Aquitaine" },
];

export function HomePage() {
  return (
    <section className="home-page">
      <div className="home-layout">
        <div className="home-copy">
          <p className="eyebrow">Outil de visualisation</p>
          <h1>Exploration des données de CMR</h1>
          <p>
            Exploration interactive des trajectoires, phénologies de presence et statistiques
            descriptives issues des données actuelles.
          </p>
        </div>
        <div className="home-panels" aria-label="Modules disponibles">
          {[
            { icon: Map, title: "Cartographie", text: "Trajectoires filtrees et carte canvas." },
            { icon: Activity, title: "Phenologie", text: "Presences par site et par periode." },
            { icon: BarChart3, title: "Statistiques", text: "KPI, especes, frequences, distances." },
            { icon: Radar, title: "Fiche site", text: "Vue detaillee par site equipe." },
          ].map((item) => (
            <article key={item.title}>
              <item.icon size={22} />
              <strong>{item.title}</strong>
              <span>{item.text}</span>
            </article>
          ))}
        </div>
      </div>
      <div className="funder-strip" aria-label="Financeurs">
        {funders.map((funder) => (
          <img key={funder.alt} src={funder.src} alt={funder.alt} />
        ))}
      </div>
    </section>
  );
}
