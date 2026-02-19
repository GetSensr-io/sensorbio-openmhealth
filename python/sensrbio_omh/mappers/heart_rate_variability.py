from __future__ import annotations

from sensrbio_omh.mappers.base_mapper import BaseMapper
from sensrbio_omh.schemas.types import (
    OmhHeartRateVariability,
    OmhSchemaId,
    OmhTimeFrameDateTime,
    OmhUnitValue,
    SensrBiometric,
)
from sensrbio_omh.utils.time_utils import to_iso_string


class HeartRateVariabilityMapper(BaseMapper[SensrBiometric, OmhHeartRateVariability]):
    @property
    def schema_id(self) -> OmhSchemaId:
        return OmhSchemaId(namespace="omh", name="heart-rate-variability", version="1.0")

    def map(self, sensr_data: SensrBiometric):
        if sensr_data.type != "hrv":
            return []

        rmssd = sensr_data.hrv.rmssd_ms if sensr_data.hrv else None
        sdnn = sensr_data.hrv.sdnn_ms if sensr_data.hrv else None

        value = None
        measure: str = "unknown"

        if isinstance(rmssd, (int, float)) and rmssd == rmssd and rmssd not in (float("inf"), float("-inf")):
            value = float(rmssd)
            measure = "RMSSD"
        elif isinstance(sdnn, (int, float)) and sdnn == sdnn and sdnn not in (float("inf"), float("-inf")):
            value = float(sdnn)
            measure = "SDNN"
        else:
            raw = sensr_data.value
            if isinstance(raw, (int, float)) and raw == raw and raw not in (float("inf"), float("-inf")):
                value = float(raw)
                measure = "unknown"

        if value is None:
            return []

        body = OmhHeartRateVariability(
            heart_rate_variability=OmhUnitValue(value=value, unit="ms"),
            measure=measure,  # type: ignore[arg-type]
            effective_time_frame=OmhTimeFrameDateTime(date_time=to_iso_string(sensr_data.timestamp_ms)),
        )
        return [self._create_data_point(body=body, id=sensr_data.id)]
