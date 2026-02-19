import type { SensrBiometric } from '../client/sensr-client.js';
import type { OmhDataPoint, OmhOxygenSaturation, OmhSchemaId } from '../schemas/types.js';
import { clamp01, toIsoString } from '../utils/time.js';
import { BaseMapper } from './base-mapper.js';

export class OxygenSaturationMapper extends BaseMapper<SensrBiometric, OmhOxygenSaturation> {
  schemaId: OmhSchemaId = { namespace: 'omh', name: 'oxygen-saturation', version: '2.0' };

  map(b: SensrBiometric): OmhDataPoint<OmhOxygenSaturation>[] {
    if (b.type !== 'spo2') return [];
    const raw = b.value;
    if (typeof raw !== 'number' || !Number.isFinite(raw)) return [];

    // Sensr might return either percent (0-100) or fraction (0-1). Normalize to percent.
    const pct = raw <= 1 ? clamp01(raw) * 100 : raw;

    return [
      this.createDataPoint(
        {
          oxygen_saturation: { value: pct, unit: '%' },
          effective_time_frame: { date_time: toIsoString(b.timestamp_ms) }
        },
        b.id
      )
    ];
  }
}
