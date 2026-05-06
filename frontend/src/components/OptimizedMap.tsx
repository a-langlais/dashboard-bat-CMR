import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { ChevronDown, ChevronUp } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import type { TrajectoryMapResponse } from "../types/api";
import {
  formatDepartment as formatDepartmentLabel,
  getDepartmentColor as getDepartmentColorForCode,
  normalizeDepartmentCode,
} from "../utils/departments";

type OptimizedMapProps = {
  data: TrajectoryMapResponse | null;
  showSiteLabels?: boolean;
};

type MapLegendProps = OptimizedMapProps & {
  onToggleSiteLabels?: (visible: boolean) => void;
};

const UNKNOWN_DEPARTMENT = "Non renseigné";

export function OptimizedMap({ data, showSiteLabels = false }: OptimizedMapProps) {
  const mapNode = useRef<HTMLDivElement | null>(null);
  const map = useRef<L.Map | null>(null);
  const layer = useRef<L.LayerGroup | null>(null);

  useEffect(() => {
    if (!mapNode.current || map.current) return;

    map.current = L.map(mapNode.current, {
      renderer: L.canvas({ padding: 0.5 }),
      preferCanvas: true,
      zoomControl: false,
    }).setView([46.493889, 2.602778], 6);

    L.control.zoom({ position: "bottomright" }).addTo(map.current);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "&copy; OpenStreetMap",
      crossOrigin: "anonymous",
      maxZoom: 18,
    }).addTo(map.current);
    layer.current = L.layerGroup().addTo(map.current);
  }, []);

  useEffect(() => {
    if (!mapNode.current) return;

    const observer = new ResizeObserver(() => {
      map.current?.invalidateSize();
    });
    observer.observe(mapNode.current);

    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (!map.current || !layer.current || !data) return;

    layer.current.clearLayers();
    map.current.setView([data.center.lat, data.center.lon], data.center.zoom);

    const routeCounts = data.trajectories.reduce<Record<string, Set<string>>>((acc, trajectory) => {
      const species = trajectory.species ?? "Non renseigné";
      const routeKey = `${species}|${trajectory.departure.site ?? ""}|${trajectory.arrival.site ?? ""}`;
      if (!acc[routeKey]) acc[routeKey] = new Set();
      acc[routeKey].add(trajectory.num_pit);
      return acc;
    }, {});

    data.trajectories.forEach((trajectory) => {
      const species = trajectory.species ?? "Non renseigné";
      const routeKey = `${species}|${trajectory.departure.site ?? ""}|${trajectory.arrival.site ?? ""}`;
      const individualCount = trajectory.individual_count ?? routeCounts[routeKey]?.size;
      const individualText =
        individualCount === undefined
          ? "Nombre d'individus indisponible avec la réponse API courante"
          : `${individualCount.toLocaleString("fr-FR")} individu${individualCount > 1 ? "s" : ""} ayant réalisé cette trajectoire au moins une fois`;
      const line = L.polyline(
        [
          [trajectory.departure.lat, trajectory.departure.lon],
          [trajectory.arrival.lat, trajectory.arrival.lon],
        ],
        {
          color: trajectory.color,
          weight: individualCount ? Math.min(5.5, 1.1 + Math.log10(individualCount + 1) * 1.7) : 1.45,
          opacity: individualCount && individualCount > 20 ? 0.7 : 0.54,
          interactive: true,
        },
      );
      line.bindTooltip(
        `<strong>${species}</strong><br>${individualText}<br>${trajectory.departure.site ?? "Site départ inconnu"} -> ${trajectory.arrival.site ?? "Site arrivée inconnu"}<br>${trajectory.distance_km.toLocaleString("fr-FR")} km`,
        { sticky: true },
      );
      line.addTo(layer.current!);
    });

    data.sites.forEach((site) => {
      const marker = L.circleMarker([site.lat, site.lon], {
        radius: 4,
        color: "#1f2937",
        fillColor: getDepartmentColorForCode(site.departement),
        fillOpacity: 0.95,
        weight: 1,
      });
      marker.bindTooltip(
        `<strong>${site.site}</strong><br>${site.commune ?? ""}${site.departement ? ` (${formatDepartment(site.departement)})` : ""}`,
        { sticky: true },
      );
      marker.addTo(layer.current!);

      if (showSiteLabels) {
        L.marker([site.lat, site.lon], {
          interactive: false,
          icon: L.divIcon({
            className: "site-name-label",
            html: `<span>${escapeHtml(site.site)}</span>`,
            iconAnchor: [-8, 13],
          }),
        }).addTo(layer.current!);
      }
    });

    if (data.bounds) {
      map.current.fitBounds(
        [
          [data.bounds.south, data.bounds.west],
          [data.bounds.north, data.bounds.east],
        ],
        { padding: [28, 28], maxZoom: 9 },
      );
    }

    setTimeout(() => map.current?.invalidateSize(), 0);
  }, [data, showSiteLabels]);

  return <div className="map-canvas" ref={mapNode} />;
}

function escapeHtml(value: string) {
  return value.replace(/[&<>"']/g, (char) => {
    const entities: Record<string, string> = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;",
    };
    return entities[char];
  });
}

function getVisibleDepartements(data: TrajectoryMapResponse) {
  return Array.from(new Set(data.sites.map((site) => normalizeDepartmentCode(site.departement) ?? UNKNOWN_DEPARTMENT))).sort((a, b) =>
    formatDepartment(a).localeCompare(formatDepartment(b), "fr-FR", { numeric: true }),
  );
}

function getDepartmentCounts(data: TrajectoryMapResponse) {
  return data.sites.reduce<Record<string, number>>((counts, site) => {
    const departement = normalizeDepartmentCode(site.departement) ?? UNKNOWN_DEPARTMENT;
    counts[departement] = (counts[departement] ?? 0) + 1;
    return counts;
  }, {});
}

function formatDepartment(departement: string) {
  return formatDepartmentLabel(departement);
}

export function MapLegend({ data, showSiteLabels = false, onToggleSiteLabels }: MapLegendProps) {
  const [collapsed, setCollapsed] = useState(false);

  if (!data || !Object.keys(data.species_colors).length) return null;

  const counts = data.trajectories.reduce<Record<string, number>>((acc, trajectory) => {
    const species = trajectory.species ?? "Non renseigné";
    acc[species] = (acc[species] ?? 0) + 1;
    return acc;
  }, {});
  const departements = getVisibleDepartements(data);
  const departmentCounts = getDepartmentCounts(data);

  return (
    <div className={`map-legend${collapsed ? " map-legend-collapsed" : ""}`} aria-label="Légende de la carte">
      <div className="map-legend-header">
        <strong>Légende</strong>
        <button
          type="button"
          onClick={() => setCollapsed((current) => !current)}
          title={collapsed ? "Afficher la légende" : "Réduire la légende"}
          aria-expanded={!collapsed}
        >
          {collapsed ? <ChevronDown size={16} /> : <ChevronUp size={16} />}
        </button>
      </div>
      {!collapsed ? (
        <>
          <label className="map-label-toggle">
            <input
              type="checkbox"
              checked={showSiteLabels}
              onChange={(event) => onToggleSiteLabels?.(event.target.checked)}
            />
            <span>Nom des sites</span>
          </label>
          <div className={legendSectionClass(Object.keys(counts).length)}>
            <strong>Espèces</strong>
            {Object.entries(data.species_colors)
              .filter(([species]) => counts[species])
              .map(([species, color]) => (
                <div className="map-legend-row" key={species}>
                  <i style={{ backgroundColor: color }} />
                  <span>{species}</span>
                  <em>{counts[species].toLocaleString("fr-FR")}</em>
                </div>
              ))}
          </div>
          <div className={legendSectionClass(departements.length)}>
            <strong>Départements</strong>
            {departements.map((departement) => (
              <div className="map-legend-row" key={departement}>
                <i style={{ backgroundColor: getDepartmentColorForCode(departement) }} />
                <span>{formatDepartment(departement)}</span>
                <em>{departmentCounts[departement].toLocaleString("fr-FR")}</em>
              </div>
            ))}
          </div>
        </>
      ) : null}
    </div>
  );
}

function legendSectionClass(itemCount: number) {
  return itemCount > 6 ? "map-legend-section map-legend-section-wide" : "map-legend-section";
}
