from __future__ import annotations

from sensrbio_omh.mappers.base_mapper import BaseMapper
from sensrbio_omh.schemas.types import (
    OmhDurationUnitValue,
    OmhPhysicalActivity,
    OmhPhysicalActivityType,
    OmhSchemaId,
    OmhTimeFrameInterval,
    OmhTimeInterval,
    OmhUnitValue,
    SensrActivity,
)
from sensrbio_omh.utils.time_utils import to_iso_string


def map_activity_type(t: str) -> OmhPhysicalActivityType:
    s = (t or "").lower()
    if "walk" in s:
        return "walking"
    if "run" in s or "jog" in s:
        return "running"
    if "bike" in s or "cycle" in s:
        return "cycling"
    if "swim" in s:
        return "swimming"
    if "strength" in s or "weight" in s:
        return "strength_training"
    if "yoga" in s:
        return "yoga"
    if len(s) > 0:
        return "workout"
    return "unknown"


class PhysicalActivityMapper(BaseMapper[SensrActivity, OmhPhysicalActivity]):
    @property
    def schema_id(self) -> OmhSchemaId:
        return OmhSchemaId(namespace="omh", name="physical-activity", version="2.0")

    def map(self, sensr_data: SensrActivity):
        if not sensr_data.start_time_ms or not sensr_data.end_time_ms or sensr_data.end_time_ms <= sensr_data.start_time_ms:
            return []

        interval = OmhTimeInterval(
            start_date_time=to_iso_string(sensr_data.start_time_ms),
            end_date_time=to_iso_string(sensr_data.end_time_ms),
        )

        body = OmhPhysicalActivity(
            activity_name=sensr_data.name,
            physical_activity=map_activity_type(sensr_data.type),
            effective_time_frame=OmhTimeFrameInterval(time_interval=interval),
        )

        duration_s = (sensr_data.end_time_ms - sensr_data.start_time_ms) / 1000.0
        if duration_s > 0 and duration_s == duration_s:
            body.duration = OmhDurationUnitValue(value=float(duration_s), unit="s")

        if isinstance(sensr_data.distance_m, (int, float)):
            body.distance = OmhUnitValue(value=float(sensr_data.distance_m), unit="m")

        if isinstance(sensr_data.calories_kcal, (int, float)):
            body.calories_burned = OmhUnitValue(value=float(sensr_data.calories_kcal), unit="kcal")

        return [self._create_data_point(body=body, id=sensr_data.id)]
