from __future__ import annotations

from sensrbio_omh.mappers.base_mapper import BaseMapper
from sensrbio_omh.schemas.types import (
    OmhKcalBurned,
    OmhSchemaId,
    OmhTimeFrameInterval,
    OmhTimeInterval,
    OmhUnitValue,
    SensrCalorieDetailsResponse,
)
from sensrbio_omh.utils.time_utils import to_iso_string


class CaloriesBurnedMapper(BaseMapper[SensrCalorieDetailsResponse, OmhKcalBurned]):
    @property
    def schema_id(self) -> OmhSchemaId:
        return OmhSchemaId(namespace="omh", name="kcal-burned", version="2.0")

    def map(self, sensr_data: SensrCalorieDetailsResponse):
        if not sensr_data.buckets:
            return []

        out: list = []
        for b in sensr_data.buckets:
            if not isinstance(b.calories_kcal, (int, float)):
                continue
            interval = OmhTimeInterval(start_date_time=to_iso_string(b.start_time_ms), end_date_time=to_iso_string(b.end_time_ms))
            body = OmhKcalBurned(
                kcal_burned=OmhUnitValue(value=float(b.calories_kcal), unit="kcal"),
                effective_time_frame=OmhTimeFrameInterval(time_interval=interval),
            )
            out.append(self._create_data_point(body=body, id=f"{sensr_data.user_id}:{b.start_time_ms}:{b.end_time_ms}:kcal"))
        return out
