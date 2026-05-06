import type {
  FilterOptions,
  GlobalStats,
  SitePhenology,
  SiteSummary,
  TrajectoryFilters,
  TrajectoryMapResponse,
} from "../types/api";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!response.ok) {
    throw new Error(`API ${response.status}: ${response.statusText}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  filters: () => request<FilterOptions>("/filters"),
  trajectories: (filters: TrajectoryFilters) =>
    request<TrajectoryMapResponse>("/map/trajectories", {
      method: "POST",
      body: JSON.stringify(filters),
    }),
  globalStats: () => request<GlobalStats>("/stats/global"),
  phenology: (params: URLSearchParams) =>
    request<SitePhenology[]>(`/phenology?${params.toString()}`),
  siteSummary: (site: string) => request<SiteSummary>(`/sites/${encodeURIComponent(site)}/summary`),
};
