import { Antenna, CheckCheck, Hash, MapPinned, Percent, Tag } from "lucide-react";
import type { Kpis } from "../types/api";

type KpiGridProps = {
  kpis: Kpis;
};

export function KpiGrid({ kpis }: KpiGridProps) {
  const localControlRate = kpis.local_control_rate;
  const followUpYears = kpis.follow_up_years;
  const items = [
    { label: "Individus marqués", value: kpis.total_marked, icon: Tag },
    { label: "Individus contrôlés", value: kpis.total_recaptured, icon: CheckCheck },
    localControlRate === undefined || localControlRate === null
      ? { label: "Sites capturés", value: kpis.capture_sites.toLocaleString("fr-FR"), icon: MapPinned }
      : { label: "% contrôle local", value: `${localControlRate.toLocaleString("fr-FR")} %`, icon: Percent },
    followUpYears === undefined || followUpYears === null
      ? { label: "Sites contrôlés positifs", value: kpis.antenna_sites, icon: Antenna }
      : { label: "Années de suivi", value: followUpYears, icon: Hash },
  ];

  return (
    <div className="kpi-grid">
      {items.map((item) => (
        <article className="kpi-card" key={item.label}>
          <item.icon size={20} aria-hidden="true" />
          <span>{item.label}</span>
          <strong>{typeof item.value === "number" ? item.value.toLocaleString("fr-FR") : item.value}</strong>
        </article>
      ))}
    </div>
  );
}
