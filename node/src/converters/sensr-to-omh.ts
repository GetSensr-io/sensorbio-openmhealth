import type {
  SensrActivity,
  SensrBiometric,
  SensrCalorieDetailsResponse,
  SensrSleepDetailsDay,
  SensrSleepSummary
} from '../client/sensr-client.js';
import { SensrClient } from '../client/sensr-client.js';
import type { OmhBody, OmhDataPoint } from '../schemas/types.js';
import { createDefaultMappers, type MapperType } from '../mappers/index.js';

export interface DateRange {
  startDate: string; // YYYY-MM-DD
  endDate: string; // YYYY-MM-DD
}

export interface ConvertParams {
  userId: string;
  dateRange: DateRange;
}

function isoDateList(startDate: string, endDate: string): string[] {
  const start = new Date(`${startDate}T00:00:00.000Z`);
  const end = new Date(`${endDate}T00:00:00.000Z`);
  if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) {
    throw new Error('Invalid dateRange; expected YYYY-MM-DD');
  }
  const days: string[] = [];
  for (let d = start; d.getTime() <= end.getTime(); d = new Date(d.getTime() + 86400000)) {
    days.push(d.toISOString().slice(0, 10));
  }
  return days;
}

export class SensrToOmhConverter {
  private readonly client: SensrClient;
  private readonly mappers = createDefaultMappers();

  constructor(client: SensrClient) {
    this.client = client;
  }

  async convertAll(params: ConvertParams): Promise<OmhDataPoint<OmhBody>[]> {
    const types: MapperType[] = [
      'heart-rate',
      'heart-rate-variability',
      'blood-pressure',
      'oxygen-saturation',
      'respiratory-rate',
      'body-temperature',
      'total-sleep-time',
      'sleep-episode',
      'physical-activity',
      'step-count',
      'kcal-burned'
    ];

    const results: OmhDataPoint<OmhBody>[] = [];
    for (const t of types) {
      const pts = await this.convertByType(params, t);
      results.push(...pts);
    }
    return results;
  }

  async convertByType(params: ConvertParams, type: MapperType): Promise<OmhDataPoint<OmhBody>[]> {
    const { userId, dateRange } = params;

    switch (type) {
      case 'heart-rate':
      case 'heart-rate-variability':
      case 'blood-pressure':
      case 'oxygen-saturation':
      case 'respiratory-rate':
      case 'body-temperature': {
        const biometrics: SensrBiometric[] = await this.client.getBiometrics({
          userId,
          startTimeMs: Date.parse(`${dateRange.startDate}T00:00:00.000Z`),
          endTimeMs: Date.parse(`${dateRange.endDate}T23:59:59.999Z`)
        });

        const mapper = this.mappers[type] as any;
        return biometrics.flatMap((b) => mapper.map(b));
      }

      case 'physical-activity':
      case 'step-count': {
        const activities: SensrActivity[] = await this.client.getActivities({
          userId,
          startTimeMs: Date.parse(`${dateRange.startDate}T00:00:00.000Z`),
          endTimeMs: Date.parse(`${dateRange.endDate}T23:59:59.999Z`)
        });
        const mapper = this.mappers[type] as any;
        return activities.flatMap((a) => mapper.map(a));
      }

      case 'total-sleep-time': {
        const days = isoDateList(dateRange.startDate, dateRange.endDate);
        const mapper = this.mappers[type];
        const out: OmhDataPoint<OmhBody>[] = [];
        for (const day of days) {
          let summary: SensrSleepSummary;
          try {
            summary = await this.client.getSleep({ userId, date: day });
          } catch {
            continue; // no sleep data for day
          }
          out.push(...(mapper.map(summary) as unknown as OmhDataPoint<OmhBody>[]));
        }
        return out;
      }

      case 'sleep-episode': {
        const days = isoDateList(dateRange.startDate, dateRange.endDate);
        const mapper = this.mappers[type];
        const out: OmhDataPoint<OmhBody>[] = [];
        for (const day of days) {
          let details: SensrSleepDetailsDay;
          try {
            details = await this.client.getSleepDetailsDay({ userId, date: day });
          } catch {
            continue;
          }
          out.push(...(mapper.map(details) as unknown as OmhDataPoint<OmhBody>[]));
        }
        return out;
      }

      case 'kcal-burned': {
        const mapper = this.mappers[type];
        let details: SensrCalorieDetailsResponse;
        try {
          details = await this.client.getCalorieDetails({
            userId,
            granularity: 'day',
            startDate: dateRange.startDate,
            endDate: dateRange.endDate
          });
        } catch {
          return [];
        }
        return mapper.map(details) as unknown as OmhDataPoint<OmhBody>[];
      }

      default:
        return [];
    }
  }
}
