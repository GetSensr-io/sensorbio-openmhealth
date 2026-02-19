import type { SensrBiometric } from '../client/sensr-client.js';
import type { OmhBloodPressure, OmhDataPoint, OmhSchemaId } from '../schemas/types.js';
import { toIsoString } from '../utils/time.js';
import { BaseMapper } from './base-mapper.js';

export class BloodPressureMapper extends BaseMapper<SensrBiometric, OmhBloodPressure> {
  schemaId: OmhSchemaId = { namespace: 'omh', name: 'blood-pressure', version: '2.0' };

  map(b: SensrBiometric): OmhDataPoint<OmhBloodPressure>[] {
    if (b.type !== 'blood_pressure') return [];

    const sys = b.blood_pressure?.systolic_mmhg;
    const dia = b.blood_pressure?.diastolic_mmhg;
    if (typeof sys !== 'number' || typeof dia !== 'number') return [];
    if (!Number.isFinite(sys) || !Number.isFinite(dia)) return [];

    return [
      this.createDataPoint(
        {
          systolic_blood_pressure: { value: sys, unit: 'mmHg' },
          diastolic_blood_pressure: { value: dia, unit: 'mmHg' },
          effective_time_frame: { date_time: toIsoString(b.timestamp_ms) }
        },
        b.id
      )
    ];
  }
}
