from __future__ import annotations

from sensrbio_omh.mappers.base_mapper import BaseMapper
from sensrbio_omh.schemas.types import (
    OmhHeartRate,
    OmhSchemaId,
    OmhTimeFrameDateTime,
    OmhUnitValue,
    SensrBiometric,
)
from sensrbio_omh.utils.time_utils import to_iso_string


class HeartRateMapper(BaseMapper[SensrBiometric, OmhHeartRate]):
    @property
    def schema_id(self) -> OmhSchemaId:
        return OmhSchemaId(namespace="omh", name="heart-rate", version="2.0")

    def map(self, sensr_data: SensrBiometric):
        if sensr_data.type != "heart_rate":
            return []
        raw = sensr_data.value
        if raw is None or not isinstance(raw, (int, float)):
            return []
        if raw != raw or raw in (float("inf"), float("-inf")):
            return []

        body = OmhHeartRate(
            heart_rate=OmhUnitValue(value=float(raw), unit="beats/min"),
            effective_time_frame=OmhTimeFrameDateTime(date_time=to_iso_string(sensr_data.timestamp_ms)),
        )
        return [self._create_data_point(body=body, id=sensr_data.id)]
