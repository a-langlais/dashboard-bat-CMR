import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  LabelList,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ReferenceDot,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { CategoryCount, DailyFrequency, DistanceValue, YearCount } from "../types/api";

export const speciesColors: Record<string, string> = {
  MINSCH: "#1f77b4",
  RHIFER: "#2ca02c",
  MYOEMA: "#d62728",
  RHIEUR: "#9467bd",
  MYONAT: "#ff7f0e",
  MYODAU: "#8c564b",
};

const palette = ["#16697a", "#db6400", "#489fb5", "#82c0cc", "#ffa62b", "#6a994e", "#9b5de5"];
const colorFor = (label: string, index: number) => speciesColors[label] ?? palette[index % palette.length];
const visibleCountLabel = (value: unknown) => {
  const count = Number(value ?? 0);
  return count > 0 ? count.toLocaleString("fr-FR") : "";
};

export function SpeciesYearChart({ data }: { data: YearCount[] }) {
  const years = Array.from(new Set(data.map((item) => item.year))).sort();
  const species = Array.from(new Set(data.map((item) => item.species))).sort();
  const rows = years.map((year) => {
    const row: Record<string, number | string> = { year };
    species.forEach((code) => {
      row[code] = data.find((item) => item.year === year && item.species === code)?.count ?? 0;
    });
    return row;
  });

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={rows} margin={{ top: 18, right: 18, bottom: 8, left: 0 }}>
        <CartesianGrid strokeDasharray="3 3" vertical={false} />
        <XAxis dataKey="year" tickLine={false} />
        <YAxis tickLine={false} width={68} />
        <Tooltip />
        <Legend />
        {species.map((code, index) => (
          <Bar key={code} dataKey={code} stackId="species" fill={colorFor(code, index)}>
            <LabelList dataKey={code} position="insideTop" fill="#fff" fontSize={10} formatter={visibleCountLabel} />
          </Bar>
        ))}
      </BarChart>
    </ResponsiveContainer>
  );
}

export function DonutChart({ data }: { data: CategoryCount[] }) {
  return (
    <ResponsiveContainer width="100%" height={310}>
      <PieChart margin={{ top: 18, right: 24, bottom: 18, left: 24 }}>
        <Pie
          data={data}
          dataKey="count"
          nameKey="label"
          innerRadius={62}
          outerRadius={98}
          paddingAngle={2}
          labelLine={false}
          label={(entry) => Number(entry.value ?? 0).toLocaleString("fr-FR")}
        >
          {data.map((entry, index) => (
            <Cell key={entry.label} fill={colorFor(entry.label, index)} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}

export function FrequencyChart({ data }: { data: DailyFrequency[] }) {
  const maxPoint = data.reduce<DailyFrequency | null>(
    (best, item) => (!best || item.count > best.count ? item : best),
    null,
  );

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data} margin={{ top: 22, right: 18, bottom: 8, left: 0 }}>
        <CartesianGrid strokeDasharray="3 3" vertical={false} />
        <XAxis dataKey="month_day" tickLine={false} interval={35} />
        <YAxis tickLine={false} width={68} />
        <Tooltip />
        <Line type="monotone" dataKey="count" name="Détections" stroke="#16697a" strokeWidth={2} dot={false} />
        {maxPoint ? (
          <ReferenceDot
            x={maxPoint.month_day}
            y={maxPoint.count}
            r={4}
            fill="#db6400"
            stroke="#fff"
            label={{ value: maxPoint.count.toLocaleString("fr-FR"), position: "top", fill: "#33474d", fontSize: 12 }}
          />
        ) : null}
      </LineChart>
    </ResponsiveContainer>
  );
}

export function TopBarChart({ data }: { data: CategoryCount[] }) {
  return (
    <ResponsiveContainer width="100%" height={390}>
      <BarChart data={data} layout="vertical" margin={{ left: 16, right: 36, top: 8, bottom: 8 }}>
        <CartesianGrid strokeDasharray="3 3" horizontal={false} />
        <XAxis type="number" tickLine={false} />
        <YAxis type="category" dataKey="label" tickLine={false} width={142} />
        <Tooltip />
        <Bar dataKey="count" name="Occurrences" fill="#db6400" radius={[0, 4, 4, 0]}>
          <LabelList dataKey="count" position="right" formatter={visibleCountLabel} />
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}

export function DistanceBoxplot({ data }: { data: DistanceValue[] }) {
  const grouped = buildDistanceGroups(data);
  const formatKm = (value: number) => value.toLocaleString("fr-FR", { maximumFractionDigits: 1 });

  return (
    <div className="distance-table" aria-label="Distances par espèce">
      <div className="distance-distribution-head">
        <span>Espèce</span>
        <span>Min</span>
        <span>Q1</span>
        <span>Méd.</span>
        <span>Q3</span>
        <span>Max</span>
        <span>n</span>
      </div>
      {grouped.map((item) => (
        <div className="distance-distribution-row" key={item.species}>
          <strong style={{ borderColor: item.color }}>{item.species}</strong>
          <span>{formatKm(item.min)}</span>
          <span>{formatKm(item.q1)}</span>
          <span className="distance-emphasis">{formatKm(item.median)}</span>
          <span>{formatKm(item.q3)}</span>
          <span>{formatKm(item.max)}</span>
          <span>{item.count.toLocaleString("fr-FR")}</span>
        </div>
      ))}
    </div>
  );
}

function buildDistanceGroups(data: DistanceValue[]) {
  return Array.from(
    data.reduce((acc, row) => {
      const values = acc.get(row.species) ?? [];
      values.push(row.distance_km);
      acc.set(row.species, values);
      return acc;
    }, new Map<string, number[]>()),
  )
    .map(([species, values], index) => {
      const sorted = [...values].sort((a, b) => a - b);
      return {
        species,
        color: colorFor(species, index),
        min: sorted[0],
        q1: quantile(sorted, 0.25),
        median: quantile(sorted, 0.5),
        q3: quantile(sorted, 0.75),
        max: sorted[sorted.length - 1],
        count: sorted.length,
      };
    })
    .sort((a, b) => b.median - a.median);
}

function quantile(sorted: number[], q: number) {
  if (!sorted.length) return 0;
  const pos = (sorted.length - 1) * q;
  const base = Math.floor(pos);
  const rest = pos - base;
  return sorted[base + 1] !== undefined ? sorted[base] + rest * (sorted[base + 1] - sorted[base]) : sorted[base];
}
