import type { SensrCalorieDetailsResponse } from '../client/sensr-client.js';
import type { OmhDataPoint, OmhKcalBurned, OmhSchemaId } from '../schemas/types.js';
import { BaseMapper } from './base-mapper.js';

export class CaloriesBurnedMapper extends BaseMapper<SensrCalorieDetailsResponse, OmhKcalBurned> {
  schemaId: OmhSchemaId = { namespace: 'omh', name: 'kcal-burned', version: '2.0' };

  map(r: SensrCalorieDetailsResponse): OmhDataPoint<OmhKcalBurned>[] {
    if (!Array.isArray(r.buckets) || r.buckets.length === 0) return [];

    return r.buckets
      .filter((b) => typeof b.calories_kcal === 'number' && Number.isFinite(b.calories_kcal))
      .map((b) =>
        this.createDataPoint(
          {
            kcal_burned: { value: b.calories_kcal, unit: 'kcal' },
            effective_time_frame: {
              time_interval: {
                start_date_time: new Date(b.start_time_ms).toISOString(),
                end_date_time: new Date(b.end_time_ms).toISOString()
              }
            }
          },
          `${r.user_id}:${b.start_time_ms}:${b.end_time_ms}:kcal`
        )
      );
  }
}
