import { Download, FileJson, RefreshCw } from "lucide-react";
import { toPng } from "html-to-image";
import { useEffect, useMemo, useRef, useState } from "react";
import { api } from "../api/client";
import { FilterChecklist } from "../components/FilterChecklist";
import { MapLegend, OptimizedMap } from "../components/OptimizedMap";
import { SectionTitle } from "../components/SectionTitle";
import type { FilterOptions, TrajectoryFilters, TrajectoryMapResponse } from "../types/api";

type MapPageProps = {
  filters: FilterOptions;
};

export function MapPage({ filters }: MapPageProps) {
  const mapStageRef = useRef<HTMLDivElement | null>(null);
  const defaultForm: TrajectoryFilters = {
    departements: [],
    species: [],
    genders: [],
    ages: [],
    communes: [],
    sites: [],
    date_start: filters.date_min,
    date_end: filters.date_max,
    periods: filters.periods,
  };
  const [form, setForm] = useState<TrajectoryFilters>({
    ...defaultForm,
  });
  const [mapData, setMapData] = useState<TrajectoryMapResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [exportingPng, setExportingPng] = useState(false);
  const [exportError, setExportError] = useState<string | null>(null);
  const [showSiteLabels, setShowSiteLabels] = useState(false);

  const activeFilterCount =
    form.departements.length +
    form.species.length +
    form.genders.length +
    form.ages.length +
    form.communes.length +
    form.sites.length +
    (form.periods.length === filters.periods.length ? 0 : form.periods.length) +
    (form.date_start !== filters.date_min ? 1 : 0) +
    (form.date_end !== filters.date_max ? 1 : 0);

  const sites = useMemo(() => {
    if (!form.communes.length) return filters.sites;
    const siteSet = new Set<string>();
    form.communes.forEach((commune) => {
      filters.sites_by_commune[commune]?.forEach((site) => siteSet.add(site));
    });
    return Array.from(siteSet).sort();
  }, [filters.sites, filters.sites_by_commune, form.communes]);

  async function refresh() {
    setLoading(true);
    try {
      setMapData(await api.trajectories(form));
    } finally {
      setLoading(false);
    }
  }

  async function exportMapPng() {
    if (!mapStageRef.current) return;

    setExportError(null);
    setExportingPng(true);
    try {
      const dataUrl = await toPng(mapStageRef.current, {
        backgroundColor: "#f6faf9",
        cacheBust: true,
        pixelRatio: 2,
      });
      downloadUrl(dataUrl, `carte-trajectoires-${getExportDate()}.png`);
    } catch {
      setExportError("L'export PNG a echoue. Certaines tuiles cartographiques peuvent bloquer la capture du navigateur.");
    } finally {
      setExportingPng(false);
    }
  }

  function exportTrajectoriesGeoJson() {
    if (!mapData?.trajectories.length) return;

    setExportError(null);
    const featureCollection = {
      type: "FeatureCollection",
      name: `trajectoires-${getExportDate()}`,
      crs: {
        type: "name",
        properties: {
          name: "urn:ogc:def:crs:OGC:1.3:CRS84",
        },
      },
      features: mapData.trajectories.map((trajectory) => ({
        type: "Feature",
        properties: {
          id: trajectory.id,
          num_pit: trajectory.num_pit,
          species: trajectory.species,
          gender: trajectory.gender,
          age: trajectory.age,
          individual_count: trajectory.individual_count,
          departure_site: trajectory.departure.site,
          departure_departement: trajectory.departure.departement,
          departure_date: trajectory.departure.date,
          arrival_site: trajectory.arrival.site,
          arrival_departement: trajectory.arrival.departement,
          arrival_date: trajectory.arrival.date,
          distance_km: trajectory.distance_km,
          color: trajectory.color,
        },
        geometry: {
          type: "LineString",
          coordinates: [
            [trajectory.departure.lon, trajectory.departure.lat],
            [trajectory.arrival.lon, trajectory.arrival.lat],
          ],
        },
      })),
    };

    downloadBlob(
      JSON.stringify(featureCollection, null, 2),
      `trajectoires-affichees-${getExportDate()}.geojson`,
      "application/geo+json",
    );
  }

  useEffect(() => {
    refresh();
  }, []);

  return (
    <section className="map-layout">
      <aside className="filter-panel">
        <div className="filter-header">
          <SectionTitle
            title="Filtres cartographiques"
            subtitle="Affinez les liaisons par localisation, individus, sites et temporalité."
          />
          <div className="filter-summary">
            <strong>{activeFilterCount}</strong>
            <span>filtres actifs</span>
          </div>
        </div>
        <div className="filter-group">
          <h3>Limites administratives</h3>
          <FilterChecklist
            label="Département"
            values={form.departements}
            options={filters.departements}
            onChange={(departements) => setForm({ ...form, departements })}
            maxHeight={150}
          />
        </div>
        <div className="filter-group">
          <h3>Individus</h3>
          <FilterChecklist label="Espèce" values={form.species} options={filters.species} onChange={(species) => setForm({ ...form, species })} maxHeight={120} />
          <div className="inline-filter-grid">
            <FilterChecklist label="Sexe" values={form.genders} options={filters.genders} onChange={(genders) => setForm({ ...form, genders })} maxHeight={92} />
            <FilterChecklist label="Âge" values={form.ages} options={filters.ages} onChange={(ages) => setForm({ ...form, ages })} maxHeight={120} />
          </div>
        </div>
        <div className="filter-group">
          <h3>Sites</h3>
          <FilterChecklist label="Commune" values={form.communes} options={filters.communes} onChange={(communes) => setForm({ ...form, communes, sites: [] })} />
          <FilterChecklist label="Site" values={form.sites} options={sites} onChange={(selectedSites) => setForm({ ...form, sites: selectedSites })} maxHeight={220} />
        </div>
        <div className="filter-group">
          <h3>Temporalité</h3>
          <div className="date-row">
            <label>
              <span>Début</span>
              <input type="date" value={form.date_start ?? ""} onChange={(event) => setForm({ ...form, date_start: event.target.value || null })} />
            </label>
            <label>
              <span>Fin</span>
              <input type="date" value={form.date_end ?? ""} onChange={(event) => setForm({ ...form, date_end: event.target.value || null })} />
            </label>
          </div>
          <FilterChecklist label="Périodes" values={form.periods} options={filters.periods} onChange={(periods) => setForm({ ...form, periods })} maxHeight={120} />
        </div>
        <div className="filter-actions">
          <button className="secondary-action" onClick={() => setForm({ ...defaultForm })}>
            Réinitialiser
          </button>
          <button className="primary-action" onClick={refresh} disabled={loading}>
            <RefreshCw size={18} />
            {loading ? "Mise à jour..." : "Mettre à jour"}
          </button>
        </div>
      </aside>
      <div className="map-column">
        <div className="map-stage" ref={mapStageRef}>
          <div className="map-toolbar">
            <strong>{mapData?.count.toLocaleString("fr-FR") ?? "..."}</strong>
          <span>liaisons agrégées affichées</span>
        </div>
          <MapLegend data={mapData} showSiteLabels={showSiteLabels} onToggleSiteLabels={setShowSiteLabels} />
          <OptimizedMap data={mapData} showSiteLabels={showSiteLabels} />
        </div>
        <div className="map-export-actions">
          <button className="secondary-action" onClick={exportMapPng} disabled={!mapData || loading || exportingPng}>
            <Download size={18} />
            {exportingPng ? "Export PNG..." : "Exporter la carte PNG"}
          </button>
          <button className="secondary-action" onClick={exportTrajectoriesGeoJson} disabled={!mapData?.trajectories.length || loading}>
            <FileJson size={18} />
            Exporter les trajectoires GeoJSON
          </button>
        </div>
        {exportError ? <p className="map-export-error">{exportError}</p> : null}
      </div>
    </section>
  );
}

function getExportDate() {
  return new Date().toISOString().slice(0, 10);
}

function downloadUrl(url: string, filename: string) {
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
}

function downloadBlob(content: string, filename: string, type: string) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  downloadUrl(url, filename);
  URL.revokeObjectURL(url);
}
