import { Activity, BarChart3, Home, Map, Radar } from "lucide-react";
import { useEffect, useState } from "react";
import { api } from "./api/client";
import { HomePage } from "./pages/HomePage";
import { MapPage } from "./pages/MapPage";
import { PhenologyPage } from "./pages/PhenologyPage";
import { SitePage } from "./pages/SitePage";
import { StatsPage } from "./pages/StatsPage";
import type { FilterOptions } from "./types/api";
import biocenaLogo from "../images/biocena.svg";

type Tab = "home" | "map" | "phenology" | "stats" | "site";

const tabs: { id: Tab; label: string; icon: typeof Home }[] = [
  { id: "home", label: "Présentation", icon: Home },
  { id: "map", label: "Antennes", icon: Map },
  { id: "phenology", label: "Phénologie", icon: Activity },
  { id: "stats", label: "Statistiques", icon: BarChart3 },
  { id: "site", label: "Fiche site", icon: Radar },
];

export function App() {
  const [activeTab, setActiveTab] = useState<Tab>("home");
  const [filters, setFilters] = useState<FilterOptions | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.filters().then(setFilters).catch((err: Error) => setError(err.message));
  }, []);

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <span className="brand-mark">🦇</span>
          <div>
            <strong>Tableau de bord</strong>
            <small>Chiroptères Cavernicoles Prioritaires de Nouvelle-Aquitaine</small>
          </div>
        </div>
        <nav aria-label="Navigation principale">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              className={activeTab === tab.id ? "active" : ""}
              onClick={() => setActiveTab(tab.id)}
            >
              <tab.icon size={24} />
              <span>{tab.label}</span>
            </button>
          ))}
        </nav>
      </header>

      <main>
        {error ? <div className="error">API indisponible : {error}</div> : null}
        {!filters && !error ? <div className="loading">Chargement des filtres...</div> : null}
        {filters ? (
          <>
            {activeTab === "home" && <HomePage />}
            {activeTab === "map" && <MapPage filters={filters} />}
            {activeTab === "phenology" && <PhenologyPage filters={filters} />}
            {activeTab === "stats" && <StatsPage />}
            {activeTab === "site" && <SitePage filters={filters} />}
          </>
        ) : null}
      </main>
      <footer className="app-footer">
        <img src={biocenaLogo} alt="Biocena" />
        <span>© 2026 - Biocena (Alexandre LANGLAIS) - v0.6</span>
      </footer>
    </div>
  );
}
