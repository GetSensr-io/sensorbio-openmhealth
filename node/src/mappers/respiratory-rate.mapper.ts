import type { SensrBiometric } from '../client/sensr-client.js';
import type { OmhDataPoint, OmhRespiratoryRate, OmhSchemaId } from '../schemas/types.js';
import { toIsoString } from '../utils/time.js';
import { BaseMapper } from './base-mapper.js';

export class RespiratoryRateMapper extends BaseMapper<SensrBiometric, OmhRespiratoryRate> {
  schemaId: OmhSchemaId = { namespace: 'omh', name: 'respiratory-rate', version: '2.0' };

  map(b: SensrBiometric): OmhDataPoint<OmhRespiratoryRate>[] {
    if (b.type !== 'respiration_rate') return [];
    const value = b.value;
    if (typeof value !== 'number' || !Number.isFinite(value)) return [];

    return [
      this.createDataPoint(
        {
          respiratory_rate: { value, unit: 'breaths/min' },
          effective_time_frame: { date_time: toIsoString(b.timestamp_ms) }
        },
        b.id
      )
    ];
  }
}
