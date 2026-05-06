import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";
import { MultiSelect } from "../components/MultiSelect";
import { SectionTitle } from "../components/SectionTitle";
import type { FilterOptions, SitePhenology } from "../types/api";

export function PhenologyPage({ filters }: { filters: FilterOptions }) {
  const [departements, setDepartements] = useState<string[]>([]);
  const [dateStart, setDateStart] = useState(filters.date_min ?? "");
  const [dateEnd, setDateEnd] = useState(filters.date_max ?? "");
  const [sites, setSites] = useState<SitePhenology[]>([]);

  async function refresh() {
    const params = new URLSearchParams();
    departements.forEach((departement) => params.append("departements", departement));
    if (dateStart) params.set("date_start", dateStart);
    if (dateEnd) params.set("date_end", dateEnd);
    setSites(await api.phenology(params));
  }

  useEffect(() => {
    refresh();
  }, []);

  const timeline = useMemo(() => {
    const allVisits = sites.flatMap((site) => site.visits);
    if (!allVisits.length) return { rows: [], years: [] };
    const min = Math.min(...allVisits.map((visit) => new Date(visit.start).getTime()));
    const max = Math.max(...allVisits.map((visit) => new Date(visit.finish).getTime()));
    const span = Math.max(max - min, 1);
    const firstYear = new Date(min).getFullYear();
    const lastYear = new Date(max).getFullYear();
    const years = Array.from({ length: lastYear - firstYear + 1 }, (_, index) => {
      const year = firstYear + index;
      const date = new Date(`${year}-01-01T00:00:00`);
      return {
        year,
        left: ((date.getTime() - min) / span) * 100,
      };
    }).filter((marker) => marker.left >= 0 && marker.left <= 100);
    const rows = sites.slice(0, 140).map((site) => ({
      ...site,
      segments: site.visits.map((visit) => ({
        ...visit,
        left: ((new Date(visit.start).getTime() - min) / span) * 100,
        width: Math.max(((new Date(visit.finish).getTime() - new Date(visit.start).getTime()) / span) * 100, 0.8),
      })),
    }));
    return { rows, years };
  }, [sites]);

  return (
    <section className="content-stack">
      <SectionTitle title="Phénologie temporelle des sites" subtitle="Présence par site équipé, filtrable par département et plage de dates." />
      <div className="phenology-controls">
        <MultiSelect label="Département" values={departements} options={filters.departements_antennes} onChange={setDepartements} compact />
        <label>
          <span>Début</span>
          <input type="date" value={dateStart} onChange={(event) => setDateStart(event.target.value)} />
        </label>
        <label>
          <span>Fin</span>
          <input type="date" value={dateEnd} onChange={(event) => setDateEnd(event.target.value)} />
        </label>
        <button className="primary-action" onClick={refresh}>Mettre à jour</button>
      </div>
      <article className="panel">
        <h3>Présence sur chaque site</h3>
        <div className="timeline-year-header">
          <span />
          <div>
            {timeline.years.map((marker) => (
              <i key={marker.year} style={{ left: `${marker.left}%` }}>
                {marker.year}
              </i>
            ))}
          </div>
        </div>
        <div className="timeline">
          {timeline.rows.map((site) => (
            <div className="timeline-row" key={site.site}>
              <span title={site.site}>{site.site}</span>
              <div>
                {timeline.years.map((marker) => (
                  <b key={marker.year} style={{ left: `${marker.left}%` }} />
                ))}
                {site.segments.map((segment, index) => (
                  <i
                    key={`${segment.start}-${segment.finish}-${index}`}
                    style={{ left: `${segment.left}%`, width: `${segment.width}%` }}
                    title={`${segment.start} - ${segment.finish}`}
                  />
                ))}
              </div>
            </div>
          ))}
        </div>
      </article>
    </section>
  );
}
