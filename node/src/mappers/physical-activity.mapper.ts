import type { SensrActivity } from '../client/sensr-client.js';
import type { OmhDataPoint, OmhPhysicalActivity, OmhPhysicalActivityType, OmhSchemaId } from '../schemas/types.js';
import { BaseMapper } from './base-mapper.js';

function mapActivityType(type: string): OmhPhysicalActivityType {
  const t = type.toLowerCase();
  if (t.includes('walk')) return 'walking';
  if (t.includes('run') || t.includes('jog')) return 'running';
  if (t.includes('bike') || t.includes('cycle')) return 'cycling';
  if (t.includes('swim')) return 'swimming';
  if (t.includes('strength') || t.includes('weight')) return 'strength_training';
  if (t.includes('yoga')) return 'yoga';
  if (t.length > 0) return 'workout';
  return 'unknown';
}

export class PhysicalActivityMapper extends BaseMapper<SensrActivity, OmhPhysicalActivity> {
  schemaId: OmhSchemaId = { namespace: 'omh', name: 'physical-activity', version: '2.0' };

  map(a: SensrActivity): OmhDataPoint<OmhPhysicalActivity>[] {
    if (!a.start_time_ms || !a.end_time_ms || a.end_time_ms <= a.start_time_ms) return [];

    const body: OmhPhysicalActivity = {
      ...(a.name ? { activity_name: a.name } : {}),
      physical_activity: mapActivityType(a.type),
      effective_time_frame: {
        time_interval: {
          start_date_time: new Date(a.start_time_ms).toISOString(),
          end_date_time: new Date(a.end_time_ms).toISOString()
        }
      }
    };

    const durationS = (a.end_time_ms - a.start_time_ms) / 1000;
    if (Number.isFinite(durationS) && durationS > 0) body.duration = { value: durationS, unit: 's' };

    if (typeof a.distance_m === 'number' && Number.isFinite(a.distance_m)) {
      body.distance = { value: a.distance_m, unit: 'm' };
    }

    if (typeof a.calories_kcal === 'number' && Number.isFinite(a.calories_kcal)) {
      body.calories_burned = { value: a.calories_kcal, unit: 'kcal' };
    }

    return [this.createDataPoint(body, a.id)];
  }
}
