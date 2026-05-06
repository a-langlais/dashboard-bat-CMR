import { useEffect, useState } from "react";
import { api } from "../api/client";
import { DistanceBoxplot, DonutChart, FrequencyChart, SpeciesYearChart, TopBarChart } from "../components/Charts";
import { KpiGrid } from "../components/KpiGrid";
import { SectionTitle } from "../components/SectionTitle";
import type { GlobalStats } from "../types/api";

export function StatsPage() {
  const [stats, setStats] = useState<GlobalStats | null>(null);
  const [transitionPage, setTransitionPage] = useState(0);
  const [tableFilters, setTableFilters] = useState({
    numPit: "",
    species: "",
    departure: "",
    arrival: "",
    distance: "",
  });

  useEffect(() => {
    api.globalStats().then(setStats);
  }, []);

  if (!stats) {
    return (
      <div className="loading">
        <span className="spinner" aria-hidden="true" />
        <span>Chargement des statistiques...</span>
      </div>
    );
  }

  const filteredTransitions = stats.transitions.filter((row) => {
    const distanceFilter = Number.parseFloat(tableFilters.distance.replace(",", "."));
    return (
      row.num_pit.toLocaleLowerCase("fr-FR").includes(tableFilters.numPit.toLocaleLowerCase("fr-FR")) &&
      (row.species ?? "").toLocaleLowerCase("fr-FR").includes(tableFilters.species.toLocaleLowerCase("fr-FR")) &&
      (row.site_depart ?? "").toLocaleLowerCase("fr-FR").includes(tableFilters.departure.toLocaleLowerCase("fr-FR")) &&
      (row.site_arrivee ?? "").toLocaleLowerCase("fr-FR").includes(tableFilters.arrival.toLocaleLowerCase("fr-FR")) &&
      (Number.isNaN(distanceFilter) || row.distance_km >= distanceFilter)
    );
  });
  const pageSize = 20;
  const pageCount = Math.max(1, Math.ceil(filteredTransitions.length / pageSize));
  const currentPage = Math.min(transitionPage, pageCount - 1);
  const transitionRows = filteredTransitions.slice(currentPage * pageSize, currentPage * pageSize + pageSize);

  function updateTableFilter(key: keyof typeof tableFilters, value: string) {
    setTransitionPage(0);
    setTableFilters((current) => ({ ...current, [key]: value }));
  }

  return (
    <section className="content-stack">
      <SectionTitle title="Statistiques analytiques" subtitle="Vue globale des métriques descriptives du projet." />
      <KpiGrid kpis={stats.kpis} />
      <div className="dashboard-grid">
        <article className="panel">
          <h3>Proportion d'espèces détectées</h3>
          <DonutChart data={stats.detected_species} />
        </article>
        <article className="panel panel-wide">
          <h3>Fréquence des détections par jour de l'année</h3>
          <FrequencyChart data={stats.daily_frequency} />
        </article>
        <article className="panel">
          <h3>Proportion d'espèces marquées</h3>
          <DonutChart data={stats.marked_species} />
        </article>
        <article className="panel">
          <h3>Individus capturés</h3>
          <SpeciesYearChart data={stats.captures_by_year} />
        </article>
        <article className="panel">
          <h3>Individus contrôlés</h3>
          <SpeciesYearChart data={stats.controls_by_year} />
        </article>
        <article className="panel">
          <h3>Détections enregistrées</h3>
          <SpeciesYearChart data={stats.detections_by_year} />
        </article>
        <article className="panel">
          <h3>Top individus détectés</h3>
          <TopBarChart data={stats.top_detections} />
        </article>
        <article className="panel">
          <h3>Distances par espèce</h3>
          <DistanceBoxplot data={stats.distances} />
        </article>
      </div>
      <article className="panel">
        <div className="table-header">
          <h3>Table des trajectoires</h3>
          <div className="table-controls">
            <button
              type="button"
              onClick={() => setTransitionPage(Math.max(0, currentPage - 1))}
              disabled={currentPage === 0}
            >
              Précédent
            </button>
            <span>
              {currentPage + 1} / {pageCount}
            </span>
            <button
              type="button"
              onClick={() => setTransitionPage(Math.min(pageCount - 1, currentPage + 1))}
              disabled={currentPage >= pageCount - 1}
            >
              Suivant
            </button>
          </div>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>
                  PIT
                  <input value={tableFilters.numPit} onChange={(event) => updateTableFilter("numPit", event.target.value)} placeholder="Filtrer" />
                </th>
                <th>
                  Espèce
                  <input value={tableFilters.species} onChange={(event) => updateTableFilter("species", event.target.value)} placeholder="Code" />
                </th>
                <th>
                  Départ
                  <input value={tableFilters.departure} onChange={(event) => updateTableFilter("departure", event.target.value)} placeholder="Site" />
                </th>
                <th>
                  Arrivée
                  <input value={tableFilters.arrival} onChange={(event) => updateTableFilter("arrival", event.target.value)} placeholder="Site" />
                </th>
                <th>
                  Distance min.
                  <input value={tableFilters.distance} onChange={(event) => updateTableFilter("distance", event.target.value)} placeholder="km" inputMode="decimal" />
                </th>
              </tr>
            </thead>
            <tbody>
              {transitionRows.map((row) => (
                <tr key={`${row.num_pit}-${row.site_depart}-${row.site_arrivee}`}>
                  <td>{row.num_pit}</td>
                  <td>{row.species}</td>
                  <td>{row.site_depart}</td>
                  <td>{row.site_arrivee}</td>
                  <td>{row.distance_km.toFixed(1)} km</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </article>
    </section>
  );
}
