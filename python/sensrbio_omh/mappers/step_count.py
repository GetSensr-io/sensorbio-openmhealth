from __future__ import annotations

from sensrbio_omh.mappers.base_mapper import BaseMapper
from sensrbio_omh.schemas.types import (
    OmhSchemaId,
    OmhStepCount,
    OmhTimeFrameInterval,
    OmhTimeInterval,
    SensrActivity,
)
from sensrbio_omh.utils.time_utils import to_iso_string


class StepCountMapper(BaseMapper[SensrActivity, OmhStepCount]):
    @property
    def schema_id(self) -> OmhSchemaId:
        return OmhSchemaId(namespace="omh", name="step-count", version="2.0")

    def map(self, sensr_data: SensrActivity):
        if sensr_data.steps is None:
            return []
        if not isinstance(sensr_data.steps, int):
            return []
        if not sensr_data.start_time_ms or not sensr_data.end_time_ms or sensr_data.end_time_ms <= sensr_data.start_time_ms:
            return []

        interval = OmhTimeInterval(
            start_date_time=to_iso_string(sensr_data.start_time_ms),
            end_date_time=to_iso_string(sensr_data.end_time_ms),
        )

        body = OmhStepCount(step_count=int(sensr_data.steps), effective_time_frame=OmhTimeFrameInterval(time_interval=interval))
        return [self._create_data_point(body=body, id=f"{sensr_data.id}:steps")]
