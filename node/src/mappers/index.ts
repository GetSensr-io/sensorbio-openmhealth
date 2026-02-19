import { BloodPressureMapper } from './blood-pressure.mapper.js';
import { BodyTemperatureMapper } from './body-temperature.mapper.js';
import { CaloriesBurnedMapper } from './calories-burned.mapper.js';
import { HeartRateMapper } from './heart-rate.mapper.js';
import { HeartRateVariabilityMapper } from './heart-rate-variability.mapper.js';
import { OxygenSaturationMapper } from './oxygen-saturation.mapper.js';
import { PhysicalActivityMapper } from './physical-activity.mapper.js';
import { RespiratoryRateMapper } from './respiratory-rate.mapper.js';
import { SleepEpisodeMapper } from './sleep-episode.mapper.js';
import { StepCountMapper } from './step-count.mapper.js';
import { TotalSleepTimeMapper } from './total-sleep-time.mapper.js';

export {
  BloodPressureMapper,
  BodyTemperatureMapper,
  CaloriesBurnedMapper,
  HeartRateMapper,
  HeartRateVariabilityMapper,
  OxygenSaturationMapper,
  PhysicalActivityMapper,
  RespiratoryRateMapper,
  SleepEpisodeMapper,
  StepCountMapper,
  TotalSleepTimeMapper
};

export type MapperType =
  | 'heart-rate'
  | 'heart-rate-variability'
  | 'blood-pressure'
  | 'oxygen-saturation'
  | 'respiratory-rate'
  | 'body-temperature'
  | 'total-sleep-time'
  | 'sleep-episode'
  | 'physical-activity'
  | 'step-count'
  | 'kcal-burned';

export function createDefaultMappers() {
  return {
    'heart-rate': new HeartRateMapper(),
    'heart-rate-variability': new HeartRateVariabilityMapper(),
    'blood-pressure': new BloodPressureMapper(),
    'oxygen-saturation': new OxygenSaturationMapper(),
    'respiratory-rate': new RespiratoryRateMapper(),
    'body-temperature': new BodyTemperatureMapper(),
    'total-sleep-time': new TotalSleepTimeMapper(),
    'sleep-episode': new SleepEpisodeMapper(),
    'physical-activity': new PhysicalActivityMapper(),
    'step-count': new StepCountMapper(),
    'kcal-burned': new CaloriesBurnedMapper()
  } as const;
}
