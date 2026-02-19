import type { SensrBiometric } from '../client/sensr-client.js';
import type { OmhDataPoint, OmhHeartRate, OmhSchemaId } from '../schemas/types.js';
import { toIsoString } from '../utils/time.js';
import { BaseMapper } from './base-mapper.js';

export class HeartRateMapper extends BaseMapper<SensrBiometric, OmhHeartRate> {
  schemaId: OmhSchemaId = { namespace: 'omh', name: 'heart-rate', version: '2.0' };

  map(b: SensrBiometric): OmhDataPoint<OmhHeartRate>[] {
    if (b.type !== 'heart_rate') return [];
    const value = b.value;
    if (typeof value !== 'number' || !Number.isFinite(value)) return [];

    return [
      this.createDataPoint(
        {
          heart_rate: { value, unit: 'beats/min' },
          effective_time_frame: { date_time: toIsoString(b.timestamp_ms) }
        },
        b.id
      )
    ];
  }
}
