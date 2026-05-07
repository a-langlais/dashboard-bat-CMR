import type {
  FilterOptions,
  GlobalStats,
  SitePhenology,
  SiteSummary,
  TrajectoryFilters,
  TrajectoryMapResponse,
} from "../types/api";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api";
const responseCache = new Map<string, Promise<unknown>>();

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

function cachedRequest<T>(key: string, loader: () => Promise<T>): Promise<T> {
  const cached = responseCache.get(key) as Promise<T> | undefined;
  if (cached) return cached;

  const promise = loader().catch((error) => {
    responseCache.delete(key);
    throw error;
  });
  responseCache.set(key, promise);
  return promise;
}

export const api = {
  filters: () => cachedRequest("filters", () => request<FilterOptions>("/filters")),
  trajectories: (filters: TrajectoryFilters) =>
    cachedRequest(`trajectories:${JSON.stringify(filters)}`, () =>
      request<TrajectoryMapResponse>("/map/trajectories", {
        method: "POST",
        body: JSON.stringify(filters),
      }),
    ),
  globalStats: () => cachedRequest("global-stats", () => request<GlobalStats>("/stats/global")),
  phenology: (params: URLSearchParams) =>
    cachedRequest(`phenology:${params.toString()}`, () =>
      request<SitePhenology[]>(`/phenology?${params.toString()}`),
    ),
  siteSummary: (site: string) =>
    cachedRequest(`site-summary:${site}`, () =>
      request<SiteSummary>(`/sites/${encodeURIComponent(site)}/summary`),
    ),
};
