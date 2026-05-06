import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { ChevronDown, ChevronUp } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import type { TrajectoryMapResponse } from "../types/api";
import { formatDepartment as formatDepartmentLabel, normalizeDepartmentCode } from "../utils/departments";

type OptimizedMapProps = {
  data: TrajectoryMapResponse | null;
  showSiteLabels?: boolean;
};

type MapLegendProps = OptimizedMapProps & {
  onToggleSiteLabels?: (visible: boolean) => void;
};

const DEPARTMENT_COLORS = [
  "#2563eb",
  "#16a34a",
  "#dc2626",
  "#9333ea",
  "#ea580c",
  "#0891b2",
  "#65a30d",
  "#be123c",
  "#7c3aed",
  "#0f766e",
];

const UNKNOWN_DEPARTMENT = "Non renseigné";

const DEPARTMENT_LABELS: Record<string, string> = {
  "01": "Ain",
  "02": "Aisne",
  "03": "Allier",
  "04": "Alpes-de-Haute-Provence",
  "05": "Hautes-Alpes",
  "06": "Alpes-Maritimes",
  "07": "Ardèche",
  "08": "Ardennes",
  "09": "Ariège",
  "10": "Aube",
  "11": "Aude",
  "12": "Aveyron",
  "13": "Bouches-du-Rhône",
  "14": "Calvados",
  "15": "Cantal",
  "16": "Charente",
  "17": "Charente-Maritime",
  "18": "Cher",
  "19": "Correze",
  "20": "Corse",
  "21": "Côte-d'Or",
  "22": "Côtes-d'Armor",
  "23": "Creuse",
  "24": "Dordogne",
  "25": "Doubs",
  "26": "Drôme",
  "27": "Eure",
  "28": "Eure-et-Loir",
  "29": "Finistère",
  "30": "Gard",
  "32": "Gers",
  "65": "Hautes-Pyrénées",
  "33": "Gironde",
  "34": "Hérault",
  "35": "Ille-et-Vilaine",
  "36": "Indre",
  "37": "Indre-et-Loire",
  "38": "Isère",
  "39": "Jura",
  "40": "Landes",
  "41": "Loir-et-Cher",
  "42": "Loire",
  "43": "Haute-Loire",
  "44": "Loire-Atlantique",
  "45": "Loiret",
  "46": "Lot",
  "47": "Lot-et-Garonne",
  "48": "Lozère",
  "49": "Maine-et-Loire",
  "50": "Manche",
  "51": "Marne",
  "52": "Haute-Marne",
  "53": "Mayenne",
  "54": "Meurthe-et-Moselle",
  "55": "Meuse",
  "56": "Morbihan",
  "57": "Moselle",
  "58": "Nièvre",
  "59": "Nord",
  "60": "Oise",
  "61": "Orne",
  "62": "Pas-de-Calais",
  "63": "Puy-de-Dôme",
  "64": "Pyrénées-Atlantiques",
  "66": "Pyrénées-Orientales",
  "67": "Bas-Rhin",
  "68": "Haut-Rhin",
  "69": "Rhône",
  "71": "Saône-et-Loire",
  "72": "Sarthe",
  "73": "Savoie",
  "74": "Haute-Savoie",
  "75": "Paris",
  "76": "Seine-Maritime",
  "93": "Seine-Saint-Denis",
  "78": "Yvelines",
  "81": "Tarn",
  "82": "Tarn-et-Garonne",
  "83": "Var",
  "84": "Vaucluse",
  "85": "Vendée",
  "86": "Vienne",
  "87": "Haute-Vienne",
  "89": "Yonne",
  "91": "Essonne",
  "94": "Val-de-Marne",
  "95": "Val-d'Oise",
  "971": "Guadeloupe",
  "972": "Martinique",
  "973": "Guyane",
  "974": "La Réunion",
  "Alava/Araba": "Espagne",
  "Araba": "Espagne",
  "Aragon": "Espagne",
  "Bizkaia": "Espagne",
  "Catalunya": "Espagne",
  "Gipuzkoa": "Espagne",
  "Navarra": "Espagne",
};

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
        fillColor: getDepartmentColor(site.departement, data),
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

function getDepartmentColor(departement: string | null, data: TrajectoryMapResponse) {
  const departements = getVisibleDepartements(data);
  const key = normalizeDepartmentCode(departement) ?? UNKNOWN_DEPARTMENT;
  const index = Math.max(0, departements.indexOf(key));
  return DEPARTMENT_COLORS[index % DEPARTMENT_COLORS.length];
}

function getVisibleDepartements(data: TrajectoryMapResponse) {
  return Array.from(new Set(data.sites.map((site) => normalizeDepartmentCode(site.departement) ?? UNKNOWN_DEPARTMENT))).sort((a, b) =>
    formatDepartment(a).localeCompare(formatDepartment(b), "fr-FR", { numeric: true }),
  );
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
            {departements.map((departement, index) => (
              <div className="map-legend-row" key={departement}>
                <i style={{ backgroundColor: DEPARTMENT_COLORS[index % DEPARTMENT_COLORS.length] }} />
                <span>{formatDepartment(departement)}</span>
                <em>{data.sites.filter((site) => (normalizeDepartmentCode(site.departement) ?? UNKNOWN_DEPARTMENT) === departement).length}</em>
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
