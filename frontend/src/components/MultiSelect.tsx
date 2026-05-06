type MultiSelectProps = {
  label: string;
  values: string[];
  options: string[];
  onChange: (values: string[]) => void;
  compact?: boolean;
};

export function MultiSelect({ label, values, options, onChange, compact }: MultiSelectProps) {
  return (
    <label className="field">
      <span>{label}</span>
      <select
        multiple
        size={compact ? 4 : 6}
        value={values}
        onChange={(event) =>
          onChange(Array.from(event.currentTarget.selectedOptions).map((option) => option.value))
        }
      >
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </label>
  );
}
