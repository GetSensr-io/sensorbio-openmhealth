from __future__ import annotations

from sensrbio_omh.mappers.base_mapper import BaseMapper
from sensrbio_omh.schemas.types import (
    OmhSchemaId,
    OmhSleepEpisode,
    OmhSleepEpisodeBody,
    OmhSleepEpisodeType,
    OmhTimeFrameInterval,
    OmhTimeInterval,
    SensrSleepDetailsDay,
)
from sensrbio_omh.utils.time_utils import to_iso_string


def map_stage(stage: str) -> OmhSleepEpisodeType:
    s = (stage or "").lower()
    if s == "awake":
        return "awake"
    if s == "light":
        return "light_sleep"
    if s == "deep":
        return "deep_sleep"
    if s == "rem":
        return "rem_sleep"
    if s in {"in_bed", "inbed", "bed"}:
        return "in_bed"
    return "unknown"


def seg_id(user_id: str, date: str, start_ms: int, end_ms: int, idx: int) -> str:
    return f"{user_id}:{date}:{start_ms}:{end_ms}:{idx}"


class SleepEpisodeMapper(BaseMapper[SensrSleepDetailsDay, OmhSleepEpisode]):
    @property
    def schema_id(self) -> OmhSchemaId:
        return OmhSchemaId(namespace="omh", name="sleep-episode", version="2.0")

    def map(self, sensr_data: SensrSleepDetailsDay):
        if not sensr_data.segments:
            return []

        overall_interval = OmhTimeInterval(
            start_date_time=to_iso_string(sensr_data.start_time_ms),
            end_date_time=to_iso_string(sensr_data.end_time_ms),
        )

        out: list = []
        for idx, seg in enumerate(sensr_data.segments):
            if not isinstance(seg.start_time_ms, int) or not isinstance(seg.end_time_ms, int):
                continue
            if seg.end_time_ms <= seg.start_time_ms:
                continue

            body = OmhSleepEpisode(
                sleep_episode=OmhSleepEpisodeBody(
                    sleep_episode_type=map_stage(seg.stage),
                    time_interval=OmhTimeInterval(
                        start_date_time=to_iso_string(seg.start_time_ms),
                        end_date_time=to_iso_string(seg.end_time_ms),
                    ),
                ),
                effective_time_frame=OmhTimeFrameInterval(time_interval=overall_interval),
            )
            out.append(self._create_data_point(body=body, id=seg_id(sensr_data.user_id, sensr_data.date, seg.start_time_ms, seg.end_time_ms, idx)))

        return out
