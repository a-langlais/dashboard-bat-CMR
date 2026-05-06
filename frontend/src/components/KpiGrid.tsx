import { Antenna, MapPinned, MousePointerClick, Tag } from "lucide-react";
import type { Kpis } from "../types/api";

type KpiGridProps = {
  kpis: Kpis;
};

export function KpiGrid({ kpis }: KpiGridProps) {
  const items = [
    { label: "Individus marqués", value: kpis.total_marked, icon: Tag },
    { label: "Individus contrôlés", value: kpis.total_recaptured, icon: MousePointerClick },
    { label: "Sites capturés", value: kpis.capture_sites, icon: MapPinned },
    { label: "Sites contrôlés positifs", value: kpis.antenna_sites, icon: Antenna },
  ];

  return (
    <div className="kpi-grid">
      {items.map((item) => (
        <article className="kpi-card" key={item.label}>
          <item.icon size={20} aria-hidden="true" />
          <span>{item.label}</span>
          <strong>{item.value.toLocaleString("fr-FR")}</strong>
        </article>
      ))}
    </div>
  );
}
