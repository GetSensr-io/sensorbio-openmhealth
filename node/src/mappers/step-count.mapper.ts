import type { SensrActivity } from '../client/sensr-client.js';
import type { OmhDataPoint, OmhSchemaId, OmhStepCount } from '../schemas/types.js';
import { BaseMapper } from './base-mapper.js';

export class StepCountMapper extends BaseMapper<SensrActivity, OmhStepCount> {
  schemaId: OmhSchemaId = { namespace: 'omh', name: 'step-count', version: '2.0' };

  map(a: SensrActivity): OmhDataPoint<OmhStepCount>[] {
    const steps = a.steps;
    if (typeof steps !== 'number' || !Number.isFinite(steps)) return [];
    if (!a.start_time_ms || !a.end_time_ms || a.end_time_ms <= a.start_time_ms) return [];

    return [
      this.createDataPoint(
        {
          step_count: Math.round(steps),
          effective_time_frame: {
            time_interval: {
              start_date_time: new Date(a.start_time_ms).toISOString(),
              end_date_time: new Date(a.end_time_ms).toISOString()
            }
          }
        },
        `${a.id}:steps`
      )
    ];
  }
}
