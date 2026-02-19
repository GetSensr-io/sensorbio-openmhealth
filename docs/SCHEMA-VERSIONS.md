# OMH schema versions targeted

This repo produces OMH data points with the following schema ids:

- `omh:heart-rate` v2.0
- `omh:heart-rate-variability` v1.0
- `omh:blood-pressure` v2.0
- `omh:oxygen-saturation` v2.0
- `omh:respiratory-rate` v2.0
- `omh:body-temperature` v2.0
- `omh:total-sleep-time` v2.0
- `omh:sleep-episode` v2.0
- `omh:physical-activity` v2.0
- `omh:step-count` v2.0
- `omh:kcal-burned` v2.0

Notes:
- OMH schema versions are sourced from the Open mHealth schemas repository (main branch).
- Some OMH deployments vary; if you need different versions, update `src/mappers/*.ts` schema ids.
