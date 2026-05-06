import { Search, X } from "lucide-react";
import { useMemo, useState } from "react";

type FilterChecklistProps = {
  label: string;
  values: string[];
  options: string[];
  onChange: (values: string[]) => void;
  placeholder?: string;
  maxHeight?: number;
  optionLabel?: (option: string) => string;
};

export function FilterChecklist({
  label,
  values,
  options,
  onChange,
  placeholder = "Rechercher",
  maxHeight = 180,
  optionLabel = (option) => option,
}: FilterChecklistProps) {
  const [query, setQuery] = useState("");
  const selected = new Set(values);
  const normalizedQuery = query.trim().toLocaleLowerCase("fr-FR");

  const visibleOptions = useMemo(() => {
    if (!normalizedQuery) return options.slice(0, 140);
    return options
      .filter((option) => optionLabel(option).toLocaleLowerCase("fr-FR").includes(normalizedQuery))
      .slice(0, 180);
  }, [normalizedQuery, optionLabel, options]);

  function toggle(option: string) {
    if (selected.has(option)) {
      onChange(values.filter((value) => value !== option));
    } else {
      onChange([...values, option]);
    }
  }

  return (
    <div className="checklist-field">
      <div className="checklist-label">
        <span>{label}</span>
        {values.length ? (
          <button type="button" onClick={() => onChange([])} title={`Vider ${label}`}>
            <X size={14} />
            {values.length}
          </button>
        ) : null}
      </div>
      <label className="filter-search">
        <Search size={15} />
        <input
          type="search"
          value={query}
          placeholder={placeholder}
          onChange={(event) => setQuery(event.target.value)}
        />
      </label>
      {values.length ? (
        <div className="selected-chips">
          {values.slice(0, 6).map((value) => (
            <button key={value} type="button" onClick={() => toggle(value)}>
              {optionLabel(value)}
              <X size={12} />
            </button>
          ))}
          {values.length > 6 ? <span>+{values.length - 6}</span> : null}
        </div>
      ) : null}
      <div className="checklist-options" style={{ maxHeight }}>
        {visibleOptions.map((option) => (
          <label key={option}>
            <input
              type="checkbox"
              checked={selected.has(option)}
              onChange={() => toggle(option)}
            />
            <span>{optionLabel(option)}</span>
          </label>
        ))}
        {!visibleOptions.length ? <em>Aucun résultat</em> : null}
      </div>
    </div>
  );
}
