type DepartmentMetadata = {
  label: string;
  color: string;
};

const DEPARTMENTS: Record<string, DepartmentMetadata> = {
  "10": { label: "Aube", color: "#65a30d" },
  "11": { label: "Aude", color: "#9333ea" },
  "12": { label: "Aveyron", color: "#ea580c" },
  "13": { label: "Bouches-du-Rhône", color: "#0f766e" },
  "14": { label: "Calvados", color: "#c2410c" },
  "15": { label: "Cantal", color: "#4f46e5" },
  "16": { label: "Charente", color: "#0d9488" },
  "17": { label: "Charente-Maritime", color: "#b91c1c" },
  "18": { label: "Cher", color: "#7e22ce" },
  "19": { label: "Correze", color: "#15803d" },
  "20": { label: "Corse", color: "#b45309" },
  "21": { label: "Côte-d'Or", color: "#0284c7" },
  "22": { label: "Côtes-d'Armor", color: "#db2777" },
  "23": { label: "Creuse", color: "#4d7c0f" },
  "24": { label: "Dordogne", color: "#6d28d9" },
  "25": { label: "Doubs", color: "#f97316" },
  "26": { label: "Drôme", color: "#047857" },
  "27": { label: "Eure", color: "#be123c" },
  "28": { label: "Eure-et-Loir", color: "#1d4ed8" },
  "29": { label: "Finistère", color: "#a16207" },
  "30": { label: "Gard", color: "#7c2d12" },
  "31": { label: "Haute-Garonne", color: "#0369a1" },
  "32": { label: "Gers", color: "#84cc16" },
  "33": { label: "Gironde", color: "#e11d48" },
  "34": { label: "Hérault", color: "#4338ca" },
  "35": { label: "Ille-et-Vilaine", color: "#059669" },
  "36": { label: "Indre", color: "#c026d3" },
  "37": { label: "Indre-et-Loire", color: "#ca8a04" },
  "38": { label: "Isère", color: "#dc2626" },
  "39": { label: "Jura", color: "#0e7490" },
  "40": { label: "Landes", color: "#9333ea" },
  "41": { label: "Loir-et-Cher", color: "#16a34a" },
  "42": { label: "Loire", color: "#2563eb" },
  "43": { label: "Haute-Loire", color: "#ea580c" },
  "44": { label: "Loire-Atlantique", color: "#be185d" },
  "45": { label: "Loiret", color: "#0f766e" },
  "46": { label: "Lot", color: "#7c3aed" },
  "47": { label: "Lot-et-Garonne", color: "#0891b2" },
  "48": { label: "Lozère", color: "#b91c1c" },
  "49": { label: "Maine-et-Loire", color: "#65a30d" },
  "50": { label: "Manche", color: "#d97706" },
  "51": { label: "Marne", color: "#4f46e5" },
  "52": { label: "Haute-Marne", color: "#15803d" },
  "53": { label: "Mayenne", color: "#c2410c" },
  "54": { label: "Meurthe-et-Moselle", color: "#0284c7" },
  "55": { label: "Meuse", color: "#a21caf" },
  "56": { label: "Morbihan", color: "#047857" },
  "57": { label: "Moselle", color: "#e11d48" },
  "58": { label: "Nièvre", color: "#84cc16" },
  "59": { label: "Nord", color: "#7c2d12" },
  "60": { label: "Oise", color: "#0369a1" },
  "61": { label: "Orne", color: "#9333ea" },
  "62": { label: "Pas-de-Calais", color: "#ca8a04" },
  "63": { label: "Puy-de-Dôme", color: "#be123c" },
  "64": { label: "Pyrénées-Atlantiques", color: "#16a34a" },
  "65": { label: "Hautes-Pyrénées", color: "#dc2626" },
  "66": { label: "Pyrénées-Orientales", color: "#0f766e" },
  "67": { label: "Bas-Rhin", color: "#7c3aed" },
  "68": { label: "Haut-Rhin", color: "#ea580c" },
  "69": { label: "Rhône", color: "#0891b2" },
  "70": { label: "Haute-Saône", color: "#b91c1c" },
  "71": { label: "Saône-et-Loire", color: "#65a30d" },
  "72": { label: "Sarthe", color: "#1d4ed8" },
  "73": { label: "Savoie", color: "#d97706" },
  "74": { label: "Haute-Savoie", color: "#be185d" },
  "75": { label: "Paris", color: "#64748b" },
  "76": { label: "Seine-Maritime", color: "#059669" },
  "77": { label: "Seine-et-Marne", color: "#c026d3" },
  "78": { label: "Yvelines", color: "#a16207" },
  "79": { label: "Deux-Sèvres", color: "#2563eb" },
  "80": { label: "Somme", color: "#7e22ce" },
  "81": { label: "Tarn", color: "#047857" },
  "82": { label: "Tarn-et-Garonne", color: "#b45309" },
  "83": { label: "Var", color: "#4338ca" },
  "84": { label: "Vaucluse", color: "#15803d" },
  "85": { label: "Vendée", color: "#dc2626" },
  "86": { label: "Vienne", color: "#0e7490" },
  "87": { label: "Haute-Vienne", color: "#9333ea" },
  "88": { label: "Vosges", color: "#ca8a04" },
  "89": { label: "Yonne", color: "#16a34a" },
  "90": { label: "Territoire de Belfort", color: "#be123c" },
  "91": { label: "Essonne", color: "#0284c7" },
  "92": { label: "Hauts-de-Seine", color: "#65a30d" },
  "93": { label: "Seine-Saint-Denis", color: "#ea580c" },
  "94": { label: "Val-de-Marne", color: "#7c3aed" },
  "95": { label: "Val-d'Oise", color: "#0f766e" },
  "971": { label: "Guadeloupe", color: "#0369a1" },
  "972": { label: "Martinique", color: "#be185d" },
  "973": { label: "Guyane", color: "#15803d" },
  "974": { label: "La Réunion", color: "#d97706" },
  "976": { label: "Mayotte", color: "#7c3aed" },
  "01": { label: "Ain", color: "#2b6cb0" },
  "02": { label: "Aisne", color: "#d97706" },
  "03": { label: "Allier", color: "#16a34a" },
  "04": { label: "Alpes-de-Haute-Provence", color: "#7c3aed" },
  "05": { label: "Hautes-Alpes", color: "#dc2626" },
  "06": { label: "Alpes-Maritimes", color: "#0891b2" },
  "07": { label: "Ardèche", color: "#ca8a04" },
  "08": { label: "Ardennes", color: "#be185d" },
  "09": { label: "Ariège", color: "#2563eb" },
  "Alava/Araba": { label: "Alava/Araba (ES)", color: "#2563eb" },
  "Araba": { label: "Araba (ES)", color: "#0891b2" },
  "Aragon": { label: "Aragon (ES)", color: "#ea580c" },
  "Bizkaia": { label: "Bizkaia (ES)", color: "#16a34a" },
  "Catalunya": { label: "Catalunya (ES)", color: "#7c3aed" },
  "Gipuzkoa": { label: "Gipuzkoa (ES)", color: "#dc2626" },
  "Navarra": { label: "Navarra (ES)", color: "#ca8a04" },
};

const UNKNOWN_DEPARTMENT_COLOR = "#78909c";

export function normalizeDepartmentCode(departement: string | null) {
  if (!departement) return null;
  const value = departement.trim();
  return /^\d{1,2}$/.test(value) ? value.padStart(2, "0") : value;
}

export function formatDepartment(departement: string | null) {
  const normalized = normalizeDepartmentCode(departement);
  if (!normalized) return "Non renseigné";
  return DEPARTMENTS[normalized]?.label ?? normalized;
}

export function compareDepartmentLabels(a: string, b: string) {
  return formatDepartment(a).localeCompare(formatDepartment(b), "fr-FR", { numeric: true });
}

export function sortDepartmentsByLabel(departements: string[]) {
  return [...departements].sort(compareDepartmentLabels);
}

export function getDepartmentColor(departement: string | null) {
  const normalized = normalizeDepartmentCode(departement);
  if (!normalized) return UNKNOWN_DEPARTMENT_COLOR;
  return DEPARTMENTS[normalized]?.color ?? UNKNOWN_DEPARTMENT_COLOR;
}
