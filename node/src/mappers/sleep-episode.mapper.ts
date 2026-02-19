import type { SensrSleepDetailsDay, SensrSleepEpisodeSegment } from '../client/sensr-client.js';
import type { OmhDataPoint, OmhSchemaId, OmhSleepEpisode, OmhSleepEpisodeType } from '../schemas/types.js';
import { BaseMapper } from './base-mapper.js';

function mapStage(stage: string): OmhSleepEpisodeType {
  const s = stage.toLowerCase();
  if (s === 'awake') return 'awake';
  if (s === 'light') return 'light_sleep';
  if (s === 'deep') return 'deep_sleep';
  if (s === 'rem') return 'rem_sleep';
  if (s === 'in_bed' || s === 'inbed' || s === 'bed') return 'in_bed';
  return 'unknown';
}

function segId(userId: string, date: string, seg: SensrSleepEpisodeSegment, idx: number): string {
  return `${userId}:${date}:${seg.start_time_ms}:${seg.end_time_ms}:${idx}`;
}

export class SleepEpisodeMapper extends BaseMapper<SensrSleepDetailsDay, OmhSleepEpisode> {
  schemaId: OmhSchemaId = { namespace: 'omh', name: 'sleep-episode', version: '2.0' };

  map(d: SensrSleepDetailsDay): OmhDataPoint<OmhSleepEpisode>[] {
    if (!Array.isArray(d.segments) || d.segments.length === 0) return [];

    const interval = {
      start_date_time: new Date(d.start_time_ms).toISOString(),
      end_date_time: new Date(d.end_time_ms).toISOString()
    };

    return d.segments
      .filter((s) => typeof s.start_time_ms === 'number' && typeof s.end_time_ms === 'number' && s.end_time_ms > s.start_time_ms)
      .map((s, idx) =>
        this.createDataPoint(
          {
            sleep_episode: {
              sleep_episode_type: mapStage(s.stage),
              time_interval: {
                start_date_time: new Date(s.start_time_ms).toISOString(),
                end_date_time: new Date(s.end_time_ms).toISOString()
              }
            },
            effective_time_frame: { time_interval: interval }
          },
          segId(d.user_id, d.date, s, idx)
        )
      );
  }
}
