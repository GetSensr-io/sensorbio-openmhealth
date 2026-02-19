from __future__ import annotations

from sensrbio_omh.mappers.base_mapper import BaseMapper
from sensrbio_omh.schemas.types import (
    OmhBloodPressure,
    OmhSchemaId,
    OmhTimeFrameDateTime,
    OmhUnitValue,
    SensrBiometric,
)
from sensrbio_omh.utils.time_utils import to_iso_string


class BloodPressureMapper(BaseMapper[SensrBiometric, OmhBloodPressure]):
    @property
    def schema_id(self) -> OmhSchemaId:
        return OmhSchemaId(namespace="omh", name="blood-pressure", version="2.0")

    def map(self, sensr_data: SensrBiometric):
        if sensr_data.type != "blood_pressure":
            return []
        bp = sensr_data.blood_pressure
        if not bp:
            return []
        sys = bp.systolic_mmhg
        dia = bp.diastolic_mmhg
        if not all(isinstance(x, (int, float)) for x in (sys, dia)):
            return []

        body = OmhBloodPressure(
            systolic_blood_pressure=OmhUnitValue(value=float(sys), unit="mmHg"),
            diastolic_blood_pressure=OmhUnitValue(value=float(dia), unit="mmHg"),
            effective_time_frame=OmhTimeFrameDateTime(date_time=to_iso_string(sensr_data.timestamp_ms)),
        )
        return [self._create_data_point(body=body, id=sensr_data.id)]
