import type { SensrSleepSummary } from '../client/sensr-client.js';
import type { OmhDataPoint, OmhSchemaId, OmhTotalSleepTime } from '../schemas/types.js';
import { endOfDayIso, startOfDayIso } from '../utils/time.js';
import { BaseMapper } from './base-mapper.js';

export class TotalSleepTimeMapper extends BaseMapper<SensrSleepSummary, OmhTotalSleepTime> {
  schemaId: OmhSchemaId = { namespace: 'omh', name: 'total-sleep-time', version: '2.0' };

  map(s: SensrSleepSummary): OmhDataPoint<OmhTotalSleepTime>[] {
    const tsm = s.total_sleep_minutes;
    if (typeof tsm !== 'number' || !Number.isFinite(tsm)) return [];

    // Use the sleep day as the effective time frame. If explicit start/end exist, use those.
    const start = s.start_time_ms ? new Date(s.start_time_ms).toISOString() : startOfDayIso(s.date as any);
    const end = s.end_time_ms ? new Date(s.end_time_ms).toISOString() : endOfDayIso(s.date as any);

    return [
      this.createDataPoint(
        {
          total_sleep_time: { value: tsm, unit: 'min' },
          effective_time_frame: { time_interval: { start_date_time: start, end_date_time: end } }
        },
        `${s.user_id}:${s.date}:total_sleep_time`
      )
    ];
  }
}
