type MultiSelectProps = {
  label: string;
  values: string[];
  options: string[];
  onChange: (values: string[]) => void;
  compact?: boolean;
  optionLabel?: (option: string) => string;
};

export function MultiSelect({ label, values, options, onChange, compact, optionLabel = (option) => option }: MultiSelectProps) {
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
            {optionLabel(option)}
          </option>
        ))}
      </select>
    </label>
  );
}
