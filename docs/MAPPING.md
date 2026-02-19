# Sensr → OMH mapping

This document describes how Sensr API payloads are mapped into Open mHealth (OMH) data points.

## General

All OMH data points use the standard envelope:

- `header.id`: Sensr record id when available; otherwise a deterministic synthetic id
- `header.creation_date_time`: time of conversion (ISO-8601)
- `header.acquisition_provenance.source_name`: `Sensr Bio`
- `header.acquisition_provenance.modality`: `sensed`

`effective_time_frame`:
- point-in-time records use `{ date_time: <timestamp> }`
- interval records use `{ time_interval: { start_date_time, end_date_time } }`

## Biometrics (`GET /v1/biometrics`)

### Heart rate
- Sensr: biometric `type = heart_rate`, `value` bpm
- OMH: `omh:heart-rate` v2.0
  - `body.heart_rate.value` = `value`
  - `body.heart_rate.unit` = `beats/min`
  - `body.effective_time_frame.date_time` = `timestamp_ms`

### HRV
- Sensr: biometric `type = hrv`
  - prefer `hrv.rmssd_ms` (measure `RMSSD`)
  - else `hrv.sdnn_ms` (measure `SDNN`)
  - else fallback to `value`
- OMH: `omh:heart-rate-variability` v1.0
  - `body.heart_rate_variability.unit` = `ms`

### Blood pressure
- Sensr: biometric `type = blood_pressure`, `blood_pressure.systolic_mmhg`, `blood_pressure.diastolic_mmhg`
- OMH: `omh:blood-pressure` v2.0
  - `systolic_blood_pressure.unit` = `mmHg`
  - `diastolic_blood_pressure.unit` = `mmHg`

### Oxygen saturation
- Sensr: biometric `type = spo2`, `value` is either fraction 0–1 or percent 0–100
- OMH: `omh:oxygen-saturation` v2.0
  - normalized to percent

### Respiratory rate
- Sensr: biometric `type = respiration_rate`, `value` breaths/min
- OMH: `omh:respiratory-rate` v2.0

### Body temperature
- Sensr: biometric `type = temperature`, `value` in °C (default) or °F if `unit` indicates
- OMH: `omh:body-temperature` v2.0 with `degC`

## Sleep (`GET /v1/sleep` and `GET /v1/sleep/details/day`)

### Total sleep time
- Sensr: sleep summary `total_sleep_minutes`
- OMH: `omh:total-sleep-time` v2.0

### Sleep episodes
- Sensr: sleep details `segments[]` with `stage`, `start_time_ms`, `end_time_ms`
- OMH: `omh:sleep-episode` v2.0
  - stages are mapped:
    - `awake` → `awake`
    - `light` → `light_sleep`
    - `deep` → `deep_sleep`
    - `rem` → `rem_sleep`
    - `in_bed` → `in_bed`
    - unknown → `unknown`

## Activities (`GET /v1/activities`)

### Physical activity
- Sensr: `type` and optional `name`, `start_time_ms`, `end_time_ms`, `distance_m`, `calories_kcal`
- OMH: `omh:physical-activity` v2.0
  - activity type is inferred by substring match (walk/run/cycle/etc.)

### Step count
- Sensr: `steps` on an activity
- OMH: `omh:step-count` v2.0

## Calories (`GET /v1/calorie/details`)

### kcal burned
- Sensr: buckets with `calories_kcal`, `start_time_ms`, `end_time_ms`
- OMH: `omh:kcal-burned` v2.0
