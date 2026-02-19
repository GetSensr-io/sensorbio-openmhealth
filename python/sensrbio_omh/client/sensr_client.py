from __future__ import annotations

from dataclasses import dataclass
from typing import Any, AsyncGenerator, Optional

import httpx

from sensrbio_omh.schemas.types import (
    SensrActivity,
    SensrBiometric,
    SensrCalorieDetailsResponse,
    SensrPaginatedResponse,
    SensrSleepDetailsDay,
    SensrSleepSummary,
    SensrVitals,
)


@dataclass
class SensrClientOptions:
    api_key: str
    base_url: str = "https://api.getsensr.io"
    headers: Optional[dict[str, str]] = None


class SensrApiError(RuntimeError):
    pass


class SensrClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.getsensr.io",
        headers: Optional[dict[str, str]] = None,
        timeout_s: float = 30.0,
    ):
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._headers = headers or {}
        self._client = httpx.AsyncClient(timeout=timeout_s)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "SensrClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

    async def _request(self, path: str, query: Optional[dict[str, Any]] = None) -> Any:
        url = f"{self._base_url}{path}"
        params = {k: v for (k, v) in (query or {}).items() if v is not None}
        resp = await self._client.get(
            url,
            params=params,
            headers={
                "Accept": "application/json",
                "X-API-KEY": self._api_key,
                **self._headers,
            },
        )
        if resp.status_code >= 400:
            text = ""
            try:
                text = resp.text
            except Exception:
                pass
            raise SensrApiError(f"Sensr API error {resp.status_code} for {url}: {text}")
        return resp.json()

    async def _paginate(self, path: str, query: dict[str, Any]) -> AsyncGenerator[dict[str, Any], None]:
        cursor: Optional[str] = None
        while True:
            page = await self._request(path, {**query, "cursor": cursor})
            parsed = SensrPaginatedResponse.model_validate(page)
            for item in parsed.data:
                yield item
            nxt = parsed.pagination.next_cursor if parsed.pagination else None
            if not nxt:
                break
            cursor = nxt

    async def get_biometrics(
        self,
        *,
        user_id: str,
        start_time_ms: Optional[int] = None,
        end_time_ms: Optional[int] = None,
        limit: int = 200,
    ) -> list[SensrBiometric]:
        out: list[SensrBiometric] = []
        async for item in self._paginate(
            "/v1/biometrics",
            {"user_id": user_id, "start_time_ms": start_time_ms, "end_time_ms": end_time_ms, "limit": limit},
        ):
            out.append(SensrBiometric.model_validate(item))
        return out

    async def get_activities(
        self,
        *,
        user_id: str,
        start_time_ms: Optional[int] = None,
        end_time_ms: Optional[int] = None,
        limit: int = 200,
    ) -> list[SensrActivity]:
        out: list[SensrActivity] = []
        async for item in self._paginate(
            "/v1/activities",
            {"user_id": user_id, "start_time_ms": start_time_ms, "end_time_ms": end_time_ms, "limit": limit},
        ):
            out.append(SensrActivity.model_validate(item))
        return out

    async def get_sleep(self, *, user_id: str, date: str) -> SensrSleepSummary:
        data = await self._request("/v1/sleep", {"user_id": user_id, "date": date})
        return SensrSleepSummary.model_validate(data)

    async def get_sleep_details_day(self, *, user_id: str, date: str) -> SensrSleepDetailsDay:
        data = await self._request("/v1/sleep/details/day", {"user_id": user_id, "date": date})
        return SensrSleepDetailsDay.model_validate(data)

    async def get_sleep_details_granular(
        self,
        *,
        user_id: str,
        granularity: str,
        start_date: str,
        end_date: str,
    ) -> Any:
        return await self._request(
            "/v1/sleep/details/granular",
            {"user_id": user_id, "granularity": granularity, "start_date": start_date, "end_date": end_date},
        )

    async def get_calorie_details(
        self,
        *,
        user_id: str,
        granularity: str,
        start_date: str,
        end_date: str,
    ) -> SensrCalorieDetailsResponse:
        data = await self._request(
            "/v1/calorie/details",
            {"user_id": user_id, "granularity": granularity, "start_date": start_date, "end_date": end_date},
        )
        return SensrCalorieDetailsResponse.model_validate(data)

    async def get_scores(self, *, user_id: str, date: str) -> Any:
        return await self._request("/v1/scores", {"user_id": user_id, "date": date})

    async def get_recovery_score_details(
        self,
        *,
        user_id: str,
        granularity: str,
        start_date: str,
        end_date: str,
    ) -> Any:
        return await self._request(
            "/v1/scores/recovery/details",
            {"user_id": user_id, "granularity": granularity, "start_date": start_date, "end_date": end_date},
        )

    async def get_insights(self, *, user_id: str, date: str) -> Any:
        return await self._request("/v1/insights", {"user_id": user_id, "date": date})

    async def get_vitals(
        self,
        *,
        user_id: str,
        start_time_ms: Optional[int] = None,
        end_time_ms: Optional[int] = None,
        limit: int = 200,
    ) -> list[SensrVitals]:
        out: list[SensrVitals] = []
        async for item in self._paginate(
            "/v1/vitals",
            {"user_id": user_id, "start_time_ms": start_time_ms, "end_time_ms": end_time_ms, "limit": limit},
        ):
            out.append(SensrVitals.model_validate(item))
        return out

    async def get_vitals_details_granular(
        self,
        *,
        user_id: str,
        granularity: str,
        start_date: str,
        end_date: str,
    ) -> Any:
        return await self._request(
            "/v1/vitals/details/granular",
            {"user_id": user_id, "granularity": granularity, "start_date": start_date, "end_date": end_date},
        )

