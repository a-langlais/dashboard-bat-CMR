export type FilterOptions = {
  departements: string[];
  departements_antennes: string[];
  communes: string[];
  species: string[];
  genders: string[];
  ages: string[];
  sites: string[];
  sites_by_commune: Record<string, string[]>;
  antenna_sites: string[];
  periods: string[];
  date_min: string | null;
  date_max: string | null;
};

export type TrajectoryFilters = {
  departements: string[];
  species: string[];
  genders: string[];
  ages: string[];
  communes: string[];
  sites: string[];
  date_start: string | null;
  date_end: string | null;
  periods: string[];
};

export type MapPoint = {
  site: string | null;
  departement: string | null;
  date: string | null;
  lat: number;
  lon: number;
};

export type Trajectory = {
  id: string;
  num_pit: string;
  species: string | null;
  gender: string | null;
  age: string | null;
  individual_count: number;
  departure: MapPoint;
  arrival: MapPoint;
  distance_km: number;
  color: string;
};

export type SiteMarker = {
  site: string;
  commune: string | null;
  departement: string | null;
  lat: number;
  lon: number;
  role: "departure" | "arrival" | "both";
};

export type TrajectoryMapResponse = {
  count: number;
  center: { lat: number; lon: number; zoom: number };
  bounds: { south: number; west: number; north: number; east: number } | null;
  species_colors: Record<string, string>;
  trajectories: Trajectory[];
  sites: SiteMarker[];
};

export type Kpis = {
  total_marked: number;
  total_recaptured: number;
  capture_sites: number;
  antenna_sites: number;
  local_control_rate?: number | null;
  follow_up_years?: number | null;
};

export type YearCount = { year: number; species: string; count: number };
export type CategoryCount = { label: string; count: number };
export type DailyFrequency = { month_day: string; count: number };
export type DistanceValue = { species: string; distance_km: number };

export type TransitionRow = {
  num_pit: string;
  species: string | null;
  date_depart: string | null;
  site_depart: string | null;
  date_arrivee: string | null;
  site_arrivee: string | null;
  distance_km: number;
};

export type GlobalStats = {
  kpis: Kpis;
  detections_by_year: YearCount[];
  captures_by_year: YearCount[];
  controls_by_year: YearCount[];
  detected_species: CategoryCount[];
  marked_species: CategoryCount[];
  daily_frequency: DailyFrequency[];
  top_detections: CategoryCount[];
  distances: DistanceValue[];
  transitions: TransitionRow[];
};

export type PhenologySegment = {
  start: string;
  finish: string;
};

export type SitePhenology = {
  site: string;
  departement: string | null;
  visits: PhenologySegment[];
};

export type SiteSummary = {
  site: string;
  kpis: Kpis;
  detections_by_year: YearCount[];
  captures_by_year: YearCount[];
  controls_by_year: YearCount[];
  detected_species: CategoryCount[];
  marked_species: CategoryCount[];
  daily_frequency: DailyFrequency[];
  phenology: SitePhenology[];
};
