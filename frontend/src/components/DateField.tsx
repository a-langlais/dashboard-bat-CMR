import { useEffect, useState } from "react";

type DateFieldProps = {
  label: string;
  value: string | null;
  onChange: (value: string | null) => void;
};

export function DateField({ label, value, onChange }: DateFieldProps) {
  const [draft, setDraft] = useState(formatDateForDisplay(value));

  useEffect(() => {
    setDraft(formatDateForDisplay(value));
  }, [value]);

  function handleChange(nextValue: string) {
    const nextDraft = nextValue.replace(/[^\d/-]/g, "").slice(0, 10);
    setDraft(nextDraft);

    if (!nextDraft.trim()) {
      onChange(null);
      return;
    }

    const parsedDate = parseDisplayDate(nextDraft);
    if (parsedDate) onChange(parsedDate);
  }

  function handleBlur() {
    setDraft(formatDateForDisplay(value));
  }

  const input = (
    <input
      className="date-input"
      type="text"
      inputMode="numeric"
      placeholder="AAAA/MM/DD"
      value={draft}
      onBlur={handleBlur}
      onChange={(event) => handleChange(event.target.value)}
    />
  );

  if (!label) return input;

  return (
    <label className="date-field">
      <span>{label}</span>
      {input}
    </label>
  );
}

function formatDateForDisplay(value: string | null) {
  return value ? value.replaceAll("-", "/") : "";
}

function parseDisplayDate(value: string) {
  const match = value.match(/^(\d{4})[/-](\d{2})[/-](\d{2})$/);
  if (!match) return null;

  const [, year, month, day] = match;
  const date = new Date(`${year}-${month}-${day}T00:00:00`);
  if (
    Number.isNaN(date.getTime()) ||
    date.getFullYear() !== Number(year) ||
    date.getMonth() + 1 !== Number(month) ||
    date.getDate() !== Number(day)
  ) {
    return null;
  }

  return `${year}-${month}-${day}`;
}
