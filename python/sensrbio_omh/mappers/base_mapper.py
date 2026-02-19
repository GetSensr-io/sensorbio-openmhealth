from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Generic, TypeVar
from uuid import uuid4

from sensrbio_omh.schemas.types import (
    OmhAcquisitionProvenance,
    OmhDataPoint,
    OmhHeader,
    OmhSchemaId,
)


TSensr = TypeVar("TSensr")
TOmh = TypeVar("TOmh")


class BaseMapper(ABC, Generic[TSensr, TOmh]):
    @property
    @abstractmethod
    def schema_id(self) -> OmhSchemaId:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def map(self, sensr_data: TSensr) -> list[OmhDataPoint[TOmh]]:  # pragma: no cover
        raise NotImplementedError

    def _create_header(self, id: str | None = None) -> OmhHeader:
        return OmhHeader(
            id=id or str(uuid4()),
            creation_date_time=datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z"),
            schema_id=self.schema_id,
            acquisition_provenance=OmhAcquisitionProvenance(source_name="Sensr Bio", modality="sensed"),
        )

    def _create_data_point(self, body: TOmh, id: str | None = None) -> OmhDataPoint[TOmh]:
        return OmhDataPoint(header=self._create_header(id), body=body)
