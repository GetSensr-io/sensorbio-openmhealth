from __future__ import annotations

from typing import Annotated, Generic, Literal, Optional, TypeVar, Union
from uuid import uuid4

from pydantic import BaseModel, Field


OmhNamespace = Literal["omh"]


class OmhSchemaId(BaseModel):
    namespace: OmhNamespace = "omh"
    name: Literal[
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
    version: str


class OmhAcquisitionProvenance(BaseModel):
    source_name: str
    modality: Literal["sensed", "self-reported", "unknown"]


class OmhHeader(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    creation_date_time: str
    schema_id: OmhSchemaId
    acquisition_provenance: Optional[OmhAcquisitionProvenance] = None


class OmhTimeInterval(BaseModel):
    start_date_time: str
    end_date_time: str


class OmhTimeFrameDateTime(BaseModel):
    date_time: str


class OmhTimeFrameInterval(BaseModel):
    time_interval: OmhTimeInterval


OmhTimeFrame = Annotated[Union[OmhTimeFrameInterval, OmhTimeFrameDateTime], Field(discriminator=None)]


class OmhUnitValue(BaseModel):
    value: float
    unit: str


class OmhDurationUnitValue(BaseModel):
    value: float
    unit: Literal["s", "min", "h"]


# --- OMH bodies ---


class OmhHeartRate(BaseModel):
    heart_rate: OmhUnitValue
    effective_time_frame: OmhTimeFrame


class OmhHeartRateVariability(BaseModel):
    heart_rate_variability: OmhUnitValue
    measure: Optional[Literal["RMSSD", "SDNN", "pNN50", "unknown"]] = None
    effective_time_frame: OmhTimeFrame


class OmhBloodPressure(BaseModel):
    systolic_blood_pressure: OmhUnitValue
    diastolic_blood_pressure: OmhUnitValue
    effective_time_frame: OmhTimeFrame


class OmhOxygenSaturation(BaseModel):
    oxygen_saturation: OmhUnitValue
    effective_time_frame: OmhTimeFrame


class OmhRespiratoryRate(BaseModel):
    respiratory_rate: OmhUnitValue
    effective_time_frame: OmhTimeFrame


class OmhBodyTemperature(BaseModel):
    body_temperature: OmhUnitValue
    effective_time_frame: OmhTimeFrame


class OmhTotalSleepTime(BaseModel):
    total_sleep_time: OmhDurationUnitValue
    effective_time_frame: OmhTimeFrame


OmhSleepEpisodeType = Literal["in_bed", "awake", "light_sleep", "deep_sleep", "rem_sleep", "unknown"]


class OmhSleepEpisodeBody(BaseModel):
    sleep_episode_type: OmhSleepEpisodeType
    time_interval: OmhTimeInterval


class OmhSleepEpisode(BaseModel):
    sleep_episode: OmhSleepEpisodeBody
    effective_time_frame: OmhTimeFrame


OmhPhysicalActivityType = Literal[
    "walking",
    "running",
    "cycling",
    "swimming",
    "strength_training",
    "yoga",
    "workout",
    "unknown",
]


class OmhPhysicalActivity(BaseModel):
    activity_name: Optional[str] = None
    physical_activity: OmhPhysicalActivityType
    effective_time_frame: OmhTimeFrame
    distance: Optional[OmhUnitValue] = None
    duration: Optional[OmhDurationUnitValue] = None
    calories_burned: Optional[OmhUnitValue] = None


class OmhStepCount(BaseModel):
    step_count: int
    effective_time_frame: OmhTimeFrame


class OmhKcalBurned(BaseModel):
    kcal_burned: OmhUnitValue
    effective_time_frame: OmhTimeFrame


OmhBody = Union[
    OmhHeartRate,
    OmhHeartRateVariability,
    OmhBloodPressure,
    OmhOxygenSaturation,
    OmhRespiratoryRate,
    OmhBodyTemperature,
    OmhTotalSleepTime,
    OmhSleepEpisode,
    OmhPhysicalActivity,
    OmhStepCount,
    OmhKcalBurned,
]


TBody = TypeVar("TBody", bound=BaseModel)


class OmhDataPoint(BaseModel, Generic[TBody]):
    header: OmhHeader
    body: TBody


# --- Sensr response types (mirrors the TS repo pragmatically) ---


class SensrBiometricHrv(BaseModel):
    rmssd_ms: Optional[float] = None
    sdnn_ms: Optional[float] = None
    pnn50: Optional[float] = None


class SensrBiometricBloodPressure(BaseModel):
    systolic_mmhg: float
    diastolic_mmhg: float


class SensrBiometric(BaseModel):
    id: str
    user_id: str
    type: str
    timestamp_ms: int
    value: Optional[float] = None
    unit: Optional[str] = None
    hrv: Optional[SensrBiometricHrv] = None
    blood_pressure: Optional[SensrBiometricBloodPressure] = None


class SensrSleepSummary(BaseModel):
    user_id: str
    date: str
    start_time_ms: Optional[int] = None
    end_time_ms: Optional[int] = None
    total_sleep_minutes: Optional[float] = None
    time_in_bed_minutes: Optional[float] = None
    awake_minutes: Optional[float] = None
    light_sleep_minutes: Optional[float] = None
    deep_sleep_minutes: Optional[float] = None
    rem_sleep_minutes: Optional[float] = None


class SensrSleepEpisodeSegment(BaseModel):
    start_time_ms: int
    end_time_ms: int
    stage: str


class SensrSleepDetailsDay(BaseModel):
    user_id: str
    date: str
    start_time_ms: int
    end_time_ms: int
    segments: list[SensrSleepEpisodeSegment]


class SensrActivity(BaseModel):
    id: str
    user_id: str
    start_time_ms: int
    end_time_ms: int
    type: str
    name: Optional[str] = None
    steps: Optional[int] = None
    distance_m: Optional[float] = None
    calories_kcal: Optional[float] = None


class SensrCalorieDetailsBucket(BaseModel):
    start_time_ms: int
    end_time_ms: int
    calories_kcal: float


class SensrCalorieDetailsResponse(BaseModel):
    user_id: str
    granularity: str
    buckets: list[SensrCalorieDetailsBucket]


class SensrVitals(BaseModel):
    user_id: str
    timestamp_ms: int
    resting_heart_rate: Optional[float] = None
    respiration_rate: Optional[float] = None
    spo2: Optional[float] = None
    temperature_c: Optional[float] = None


class SensrPagination(BaseModel):
    next_cursor: Optional[str] = None


class SensrPaginatedResponse(BaseModel):
    data: list[dict]
    pagination: Optional[SensrPagination] = None
