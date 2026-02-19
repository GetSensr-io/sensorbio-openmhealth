from __future__ import annotations

from sensrbio_omh.mappers.base_mapper import BaseMapper
from sensrbio_omh.schemas.types import (
    OmhDurationUnitValue,
    OmhSchemaId,
    OmhTimeFrameInterval,
    OmhTimeInterval,
    OmhTotalSleepTime,
    SensrSleepSummary,
)
from sensrbio_omh.utils.time_utils import to_iso_string


class TotalSleepTimeMapper(BaseMapper[SensrSleepSummary, OmhTotalSleepTime]):
    @property
    def schema_id(self) -> OmhSchemaId:
        return OmhSchemaId(namespace="omh", name="total-sleep-time", version="2.0")

    def map(self, sensr_data: SensrSleepSummary):
        minutes = sensr_data.total_sleep_minutes
        if not isinstance(minutes, (int, float)) or minutes != minutes or minutes in (float("inf"), float("-inf")):
            return []

        if not sensr_data.start_time_ms or not sensr_data.end_time_ms or sensr_data.end_time_ms <= sensr_data.start_time_ms:
            # TS mapper uses date_time for biometrics; for sleep summary we can still provide an interval if present.
            # If missing, emit a date_time at midnight for the day.
            interval = None
        else:
            interval = OmhTimeInterval(
                start_date_time=to_iso_string(sensr_data.start_time_ms),
                end_date_time=to_iso_string(sensr_data.end_time_ms),
            )

        effective = (
            OmhTimeFrameInterval(time_interval=interval)
            if interval
            else OmhTimeFrameInterval(time_interval=OmhTimeInterval(start_date_time=f"{sensr_data.date}T00:00:00Z", end_date_time=f"{sensr_data.date}T23:59:59Z"))
        )

        body = OmhTotalSleepTime(
            total_sleep_time=OmhDurationUnitValue(value=float(minutes), unit="min"),
            effective_time_frame=effective,
        )
        return [self._create_data_point(body=body, id=f"{sensr_data.user_id}:{sensr_data.date}:total_sleep_time")]
