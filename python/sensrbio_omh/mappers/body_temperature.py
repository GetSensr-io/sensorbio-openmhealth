from __future__ import annotations

from sensrbio_omh.mappers.base_mapper import BaseMapper
from sensrbio_omh.schemas.types import (
    OmhBodyTemperature,
    OmhSchemaId,
    OmhTimeFrameDateTime,
    OmhUnitValue,
    SensrBiometric,
)
from sensrbio_omh.utils.time_utils import to_iso_string


def f_to_c(f: float) -> float:
    return (f - 32.0) * (5.0 / 9.0)


class BodyTemperatureMapper(BaseMapper[SensrBiometric, OmhBodyTemperature]):
    @property
    def schema_id(self) -> OmhSchemaId:
        return OmhSchemaId(namespace="omh", name="body-temperature", version="2.0")

    def map(self, sensr_data: SensrBiometric):
        if sensr_data.type != "temperature":
            return []
        raw = sensr_data.value
        if not isinstance(raw, (int, float)) or raw != raw or raw in (float("inf"), float("-inf")):
            return []

        unit = (sensr_data.unit or "").lower()
        value_c = f_to_c(float(raw)) if "f" in unit else float(raw)

        body = OmhBodyTemperature(
            body_temperature=OmhUnitValue(value=value_c, unit="degC"),
            effective_time_frame=OmhTimeFrameDateTime(date_time=to_iso_string(sensr_data.timestamp_ms)),
        )
        return [self._create_data_point(body=body, id=sensr_data.id)]
