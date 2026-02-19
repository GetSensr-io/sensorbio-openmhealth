import { describe, expect, it } from 'vitest';
import { HeartRateMapper } from '../../src/mappers/heart-rate.mapper.js';
import { OxygenSaturationMapper } from '../../src/mappers/oxygen-saturation.mapper.js';
import { HeartRateVariabilityMapper } from '../../src/mappers/heart-rate-variability.mapper.js';
import type { SensrBiometric } from '../../src/client/sensr-client.js';
import biometricsFixture from '../fixtures/sensr-biometrics.json';

// eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
const biometrics = (biometricsFixture as any).data as SensrBiometric[];

describe('biometric mappers', () => {
  it('maps heart rate', () => {
    const mapper = new HeartRateMapper();
    const hr = biometrics.find((b) => b.type === 'heart_rate')!;
    const points = mapper.map(hr);
    expect(points).toHaveLength(1);
    expect(points[0].header.schema_id.name).toBe('heart-rate');
    expect(points[0].body.heart_rate.unit).toBe('beats/min');
    expect(points[0].body.heart_rate.value).toBe(62);
  });

  it('maps oxygen saturation and normalizes to percent', () => {
    const mapper = new OxygenSaturationMapper();
    const sp = biometrics.find((b) => b.type === 'spo2')!;
    const points = mapper.map(sp);
    expect(points).toHaveLength(1);
    expect(points[0].body.oxygen_saturation.unit).toBe('%');
    expect(points[0].body.oxygen_saturation.value).toBeCloseTo(97.5, 3);
  });

  it('maps HRV (RMSSD preferred)', () => {
    const mapper = new HeartRateVariabilityMapper();
    const hrv = biometrics.find((b) => b.type === 'hrv')!;
    const points = mapper.map(hrv);
    expect(points).toHaveLength(1);
    expect(points[0].header.schema_id.name).toBe('heart-rate-variability');
    expect(points[0].body.heart_rate_variability.unit).toBe('ms');
    expect(points[0].body.heart_rate_variability.value).toBeCloseTo(42.5, 5);
    expect(points[0].body.measure).toBe('RMSSD');
  });
});
