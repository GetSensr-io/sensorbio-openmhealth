import type { SensrBiometric } from '../client/sensr-client.js';
import type { OmhDataPoint, OmhHeartRateVariability, OmhSchemaId } from '../schemas/types.js';
import { toIsoString } from '../utils/time.js';
import { BaseMapper } from './base-mapper.js';

export class HeartRateVariabilityMapper extends BaseMapper<SensrBiometric, OmhHeartRateVariability> {
  schemaId: OmhSchemaId = { namespace: 'omh', name: 'heart-rate-variability', version: '1.0' };

  map(b: SensrBiometric): OmhDataPoint<OmhHeartRateVariability>[] {
    if (b.type !== 'hrv') return [];

    const rmssd = b.hrv?.rmssd_ms;
    const sdnn = b.hrv?.sdnn_ms;

    let value: number | undefined;
    let measure: OmhHeartRateVariability['measure'] = 'unknown';

    if (typeof rmssd === 'number' && Number.isFinite(rmssd)) {
      value = rmssd;
      measure = 'RMSSD';
    } else if (typeof sdnn === 'number' && Number.isFinite(sdnn)) {
      value = sdnn;
      measure = 'SDNN';
    } else if (typeof b.value === 'number' && Number.isFinite(b.value)) {
      value = b.value;
      measure = 'unknown';
    }

    if (value === undefined) return [];

    return [
      this.createDataPoint(
        {
          heart_rate_variability: { value, unit: 'ms' },
          measure,
          effective_time_frame: { date_time: toIsoString(b.timestamp_ms) }
        },
        b.id
      )
    ];
  }
}
