// OMH envelope + common body types.
// These are pragmatic TypeScript types aligned with the Open mHealth schema structure.

export type OmhNamespace = 'omh';

export interface OmhSchemaId {
  namespace: OmhNamespace;
  name:
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
  version: string;
}

export interface OmhAcquisitionProvenance {
  source_name: string;
  modality: 'sensed' | 'self-reported' | 'unknown';
}

export interface OmhHeader {
  id: string;
  creation_date_time: string; // ISO-8601
  schema_id: OmhSchemaId;
  acquisition_provenance?: OmhAcquisitionProvenance;
}

export interface OmhDataPoint<TBody> {
  header: OmhHeader;
  body: TBody;
}

export interface OmhTimeInterval {
  start_date_time: string; // ISO
  end_date_time: string; // ISO
}

export type OmhTimeFrame =
  | { time_interval: OmhTimeInterval }
  | { date_time: string };

export interface OmhUnitValue<TUnit extends string = string> {
  value: number;
  unit: TUnit;
}

export interface OmhDurationUnitValue<TUnit extends string = 's' | 'min' | 'h'> {
  value: number;
  unit: TUnit;
}

// --- Schema bodies ---

export interface OmhHeartRate {
  heart_rate: OmhUnitValue<'beats/min'>;
  effective_time_frame: OmhTimeFrame;
}

export interface OmhHeartRateVariability {
  // Many OMH deployments use either RMSSD or SDNN.
  // We'll represent generic HRV as milliseconds plus an optional measure.
  heart_rate_variability: OmhUnitValue<'ms'>;
  measure?: 'RMSSD' | 'SDNN' | 'pNN50' | 'unknown';
  effective_time_frame: OmhTimeFrame;
}

export interface OmhBloodPressure {
  systolic_blood_pressure: OmhUnitValue<'mmHg'>;
  diastolic_blood_pressure: OmhUnitValue<'mmHg'>;
  effective_time_frame: OmhTimeFrame;
}

export interface OmhOxygenSaturation {
  oxygen_saturation: OmhUnitValue<'%'>;
  effective_time_frame: OmhTimeFrame;
}

export interface OmhRespiratoryRate {
  respiratory_rate: OmhUnitValue<'breaths/min'>;
  effective_time_frame: OmhTimeFrame;
}

export interface OmhBodyTemperature {
  body_temperature: OmhUnitValue<'degC'>;
  effective_time_frame: OmhTimeFrame;
}

export interface OmhTotalSleepTime {
  // total sleep time duration
  total_sleep_time: OmhDurationUnitValue<'min'>;
  effective_time_frame: OmhTimeFrame;
}

export type OmhSleepEpisodeType =
  | 'in_bed'
  | 'awake'
  | 'light_sleep'
  | 'deep_sleep'
  | 'rem_sleep'
  | 'unknown';

export interface OmhSleepEpisode {
  sleep_episode: {
    // A single contiguous episode segment.
    sleep_episode_type: OmhSleepEpisodeType;
    time_interval: OmhTimeInterval;
  };
  effective_time_frame: OmhTimeFrame;
}

export type OmhPhysicalActivityType =
  | 'walking'
  | 'running'
  | 'cycling'
  | 'swimming'
  | 'strength_training'
  | 'yoga'
  | 'workout'
  | 'unknown';

export interface OmhPhysicalActivity {
  activity_name?: string;
  physical_activity: OmhPhysicalActivityType;
  effective_time_frame: OmhTimeFrame;
  distance?: OmhUnitValue<'m'>;
  duration?: OmhDurationUnitValue<'s'>;
  calories_burned?: OmhUnitValue<'kcal'>;
}

export interface OmhStepCount {
  step_count: number;
  effective_time_frame: OmhTimeFrame;
}

export interface OmhKcalBurned {
  kcal_burned: OmhUnitValue<'kcal'>;
  effective_time_frame: OmhTimeFrame;
}

export type OmhBody =
  | OmhHeartRate
  | OmhHeartRateVariability
  | OmhBloodPressure
  | OmhOxygenSaturation
  | OmhRespiratoryRate
  | OmhBodyTemperature
  | OmhTotalSleepTime
  | OmhSleepEpisode
  | OmhPhysicalActivity
  | OmhStepCount
  | OmhKcalBurned;
