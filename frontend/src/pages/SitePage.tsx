import { useEffect, useState } from "react";
import { api } from "../api/client";
import { DonutChart, FrequencyChart, SpeciesYearChart } from "../components/Charts";
import { KpiGrid } from "../components/KpiGrid";
import { SectionTitle } from "../components/SectionTitle";
import type { FilterOptions, SiteSummary } from "../types/api";

export function SitePage({ filters }: { filters: FilterOptions }) {
  const [site, setSite] = useState(filters.antenna_sites[0] ?? "");
  const [summary, setSummary] = useState<SiteSummary | null>(null);

  useEffect(() => {
    setSummary(null);
    if (site) api.siteSummary(site).then(setSummary);
  }, [site]);

  return (
    <section className="content-stack">
      <SectionTitle title="Fiche site" subtitle="Synthèse ciblée sur un site équipé d'antenne." />
      <label className="site-selector">
        <span>Site antenne</span>
        <select value={site} onChange={(event) => setSite(event.target.value)}>
          {filters.antenna_sites.map((option) => (
            <option key={option} value={option}>{option}</option>
          ))}
        </select>
      </label>
      {!summary ? (
        <div className="loading">
          <span className="spinner" aria-hidden="true" />
          <span>Chargement de la fiche site...</span>
        </div>
      ) : (
        <>
          <KpiGrid kpis={summary.kpis} />
          <div className="dashboard-grid">
            <article className="panel">
              <h3>Individus capturés</h3>
              <SpeciesYearChart data={summary.captures_by_year} />
            </article>
            <article className="panel">
              <h3>Individus contrôlés</h3>
              <SpeciesYearChart data={summary.controls_by_year} />
            </article>
            <article className="panel">
              <h3>Individus détectés</h3>
              <SpeciesYearChart data={summary.detections_by_year} />
            </article>
            <article className="panel">
              <h3>Espèces détectées</h3>
              <DonutChart data={summary.detected_species} />
            </article>
            <article className="panel panel-wide">
              <h3>Fréquences de détection</h3>
              <FrequencyChart data={summary.daily_frequency} />
            </article>
          </div>
        </>
      )}
    </section>
  );
}
