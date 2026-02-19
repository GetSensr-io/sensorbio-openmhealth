from __future__ import annotations

from typing import Any, Literal

from sensrbio_omh.client.sensr_client import SensrApiError, SensrClient
from sensrbio_omh.mappers import MapperType, create_default_mappers
from sensrbio_omh.schemas.types import (
    OmhBody,
    OmhDataPoint,
    SensrActivity,
    SensrBiometric,
    SensrCalorieDetailsResponse,
    SensrSleepDetailsDay,
    SensrSleepSummary,
)
from sensrbio_omh.utils.time_utils import ensure_ms_range, iso_date_list


class SensrToOmhConverter:
    def __init__(self, client: SensrClient):
        self._client = client
        self._mappers = create_default_mappers()

    async def convert_all(self, *, user_id: str, start_date: str, end_date: str) -> list[OmhDataPoint[OmhBody]]:
        types: list[MapperType] = [
            "heart-rate",
            "heart-rate-variability",
            "blood-pressure",
            "oxygen-saturation",
            "respiratory-rate",
            "body-temperature",
            "total-sleep-time",
            "sleep-episode",
            "physical-activity",
            "step-count",
            "kcal-burned",
        ]
        out: list[OmhDataPoint[OmhBody]] = []
        for t in types:
            out.extend(await self.convert_by_type(user_id=user_id, start_date=start_date, end_date=end_date, type=t))
        return out

    async def convert_by_type(
        self,
        *,
        user_id: str,
        start_date: str,
        end_date: str,
        type: MapperType,
    ) -> list[OmhDataPoint[OmhBody]]:
        start_ms, end_ms = ensure_ms_range(start_date, end_date)

        if type in {
            "heart-rate",
            "heart-rate-variability",
            "blood-pressure",
            "oxygen-saturation",
            "respiratory-rate",
            "body-temperature",
        }:
            biometrics: list[SensrBiometric] = await self._client.get_biometrics(
                user_id=user_id, start_time_ms=start_ms, end_time_ms=end_ms
            )
            mapper = self._mappers[type]
            return [pt for b in biometrics for pt in mapper.map(b)]  # type: ignore[arg-type]

        if type in {"physical-activity", "step-count"}:
            activities: list[SensrActivity] = await self._client.get_activities(
                user_id=user_id, start_time_ms=start_ms, end_time_ms=end_ms
            )
            mapper = self._mappers[type]
            return [pt for a in activities for pt in mapper.map(a)]  # type: ignore[arg-type]

        if type == "total-sleep-time":
            days = iso_date_list(start_date, end_date)
            mapper = self._mappers[type]
            out: list[OmhDataPoint[OmhBody]] = []
            for day in days:
                try:
                    summary: SensrSleepSummary = await self._client.get_sleep(user_id=user_id, date=day)
                except SensrApiError:
                    continue
                out.extend(mapper.map(summary))  # type: ignore[arg-type]
            return out

        if type == "sleep-episode":
            days = iso_date_list(start_date, end_date)
            mapper = self._mappers[type]
            out: list[OmhDataPoint[OmhBody]] = []
            for day in days:
                try:
                    details: SensrSleepDetailsDay = await self._client.get_sleep_details_day(user_id=user_id, date=day)
                except SensrApiError:
                    continue
                out.extend(mapper.map(details))  # type: ignore[arg-type]
            return out

        if type == "kcal-burned":
            mapper = self._mappers[type]
            try:
                details: SensrCalorieDetailsResponse = await self._client.get_calorie_details(
                    user_id=user_id, granularity="day", start_date=start_date, end_date=end_date
                )
            except SensrApiError:
                return []
            return mapper.map(details)  # type: ignore[arg-type]

        return []
