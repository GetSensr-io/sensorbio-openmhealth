import { describe, expect, it } from 'vitest';
import { PhysicalActivityMapper } from '../../src/mappers/physical-activity.mapper.js';
import { StepCountMapper } from '../../src/mappers/step-count.mapper.js';
import activitiesFixture from '../fixtures/sensr-activities.json';

// eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
const activities = (activitiesFixture as any).data;

describe('activity mappers', () => {
  it('maps physical activity', () => {
    const mapper = new PhysicalActivityMapper();
    const points = mapper.map(activities[0]);
    expect(points).toHaveLength(1);
    expect(points[0].header.schema_id.name).toBe('physical-activity');
    expect(points[0].body.duration?.unit).toBe('s');
    expect(points[0].body.distance?.unit).toBe('m');
    expect(points[0].body.calories_burned?.unit).toBe('kcal');
  });

  it('maps step count from activity', () => {
    const mapper = new StepCountMapper();
    const points = mapper.map(activities[0]);
    expect(points).toHaveLength(1);
    expect(points[0].header.schema_id.name).toBe('step-count');
    expect(points[0].body.step_count).toBe(3200);
  });
});
