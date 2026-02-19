import type { SensrBiometric } from '../client/sensr-client.js';
import type { OmhBodyTemperature, OmhDataPoint, OmhSchemaId } from '../schemas/types.js';
import { toIsoString } from '../utils/time.js';
import { BaseMapper } from './base-mapper.js';

function fToC(f: number): number {
  return (f - 32) * (5 / 9);
}

export class BodyTemperatureMapper extends BaseMapper<SensrBiometric, OmhBodyTemperature> {
  schemaId: OmhSchemaId = { namespace: 'omh', name: 'body-temperature', version: '2.0' };

  map(b: SensrBiometric): OmhDataPoint<OmhBodyTemperature>[] {
    if (b.type !== 'temperature') return [];
    const raw = b.value;
    if (typeof raw !== 'number' || !Number.isFinite(raw)) return [];

    // Sensr might send in C or F. Prefer explicit unit if present.
    const unit = (b.unit ?? '').toLowerCase();
    const valueC = unit.includes('f') ? fToC(raw) : raw;

    return [
      this.createDataPoint(
        {
          body_temperature: { value: valueC, unit: 'degC' },
          effective_time_frame: { date_time: toIsoString(b.timestamp_ms) }
        },
        b.id
      )
    ];
  }
}
