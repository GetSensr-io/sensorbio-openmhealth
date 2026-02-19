import { describe, expect, it } from 'vitest';
import { TotalSleepTimeMapper } from '../../src/mappers/total-sleep-time.mapper.js';
import { SleepEpisodeMapper } from '../../src/mappers/sleep-episode.mapper.js';
import sleepFixture from '../fixtures/sensr-sleep.json';

// eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
const summary = (sleepFixture as any).summary;
// eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
const details = (sleepFixture as any).details_day;

describe('sleep mappers', () => {
  it('maps total sleep time', () => {
    const mapper = new TotalSleepTimeMapper();
    const points = mapper.map(summary);
    expect(points).toHaveLength(1);
    expect(points[0].header.schema_id.name).toBe('total-sleep-time');
    expect(points[0].body.total_sleep_time.unit).toBe('min');
    expect(points[0].body.total_sleep_time.value).toBe(420);
  });

  it('maps sleep episode segments', () => {
    const mapper = new SleepEpisodeMapper();
    const points = mapper.map(details);
    expect(points.length).toBeGreaterThan(0);
    const types = new Set(points.map((p) => p.body.sleep_episode.sleep_episode_type));
    expect(types.has('in_bed')).toBe(true);
    expect(types.has('light_sleep')).toBe(true);
    expect(types.has('deep_sleep')).toBe(true);
    expect(types.has('awake')).toBe(true);
    expect(types.has('rem_sleep')).toBe(true);
  });
});
