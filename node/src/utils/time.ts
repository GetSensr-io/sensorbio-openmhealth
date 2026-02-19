export type IsoDate = `${number}-${number}-${number}`;

export function toIsoString(value: string | number | Date): string {
  if (value instanceof Date) return value.toISOString();
  if (typeof value === 'number') {
    // Sensr typically uses ms timestamps
    return new Date(value).toISOString();
  }
  // assume ISO string
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) throw new Error(`Invalid date/time: ${value}`);
  return d.toISOString();
}

export function startOfDayIso(date: IsoDate, timeZone: 'UTC' = 'UTC'): string {
  if (timeZone !== 'UTC') {
    // Placeholder for future TZ support.
    // Sensr endpoints appear to operate in UTC for ISO date parameters.
  }
  return `${date}T00:00:00.000Z`;
}

export function endOfDayIso(date: IsoDate, timeZone: 'UTC' = 'UTC'): string {
  if (timeZone !== 'UTC') {
    // Placeholder for future TZ support.
  }
  return `${date}T23:59:59.999Z`;
}

export function clamp01(x: number): number {
  if (x < 0) return 0;
  if (x > 1) return 1;
  return x;
}

export function msToSeconds(ms: number): number {
  return ms / 1000;
}

export function secondsToMinutes(s: number): number {
  return s / 60;
}
