from __future__ import annotations

from sensrbio_omh.mappers.base_mapper import BaseMapper
from sensrbio_omh.schemas.types import (
    OmhOxygenSaturation,
    OmhSchemaId,
    OmhTimeFrameDateTime,
    OmhUnitValue,
    SensrBiometric,
)
from sensrbio_omh.utils.time_utils import clamp01, to_iso_string


class OxygenSaturationMapper(BaseMapper[SensrBiometric, OmhOxygenSaturation]):
    @property
    def schema_id(self) -> OmhSchemaId:
        return OmhSchemaId(namespace="omh", name="oxygen-saturation", version="2.0")

    def map(self, sensr_data: SensrBiometric):
        if sensr_data.type != "spo2":
            return []
        raw = sensr_data.value
        if not isinstance(raw, (int, float)) or raw != raw or raw in (float("inf"), float("-inf")):
            return []

        pct = clamp01(float(raw)) * 100.0 if raw <= 1 else float(raw)

        body = OmhOxygenSaturation(
            oxygen_saturation=OmhUnitValue(value=pct, unit="%"),
            effective_time_frame=OmhTimeFrameDateTime(date_time=to_iso_string(sensr_data.timestamp_ms)),
        )
        return [self._create_data_point(body=body, id=sensr_data.id)]
