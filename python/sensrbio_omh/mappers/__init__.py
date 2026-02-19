from __future__ import annotations

from typing import Literal, TypedDict

from .blood_pressure import BloodPressureMapper
from .body_temperature import BodyTemperatureMapper
from .calories_burned import CaloriesBurnedMapper
from .heart_rate import HeartRateMapper
from .heart_rate_variability import HeartRateVariabilityMapper
from .oxygen_saturation import OxygenSaturationMapper
from .physical_activity import PhysicalActivityMapper
from .respiratory_rate import RespiratoryRateMapper
from .sleep_episode import SleepEpisodeMapper
from .step_count import StepCountMapper
from .total_sleep_time import TotalSleepTimeMapper


MapperType = Literal[
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


class MapperRegistry(TypedDict):
    heart_rate: HeartRateMapper
    heart_rate_variability: HeartRateVariabilityMapper
    blood_pressure: BloodPressureMapper
    oxygen_saturation: OxygenSaturationMapper
    respiratory_rate: RespiratoryRateMapper
    body_temperature: BodyTemperatureMapper
    total_sleep_time: TotalSleepTimeMapper
    sleep_episode: SleepEpisodeMapper
    physical_activity: PhysicalActivityMapper
    step_count: StepCountMapper
    kcal_burned: CaloriesBurnedMapper


def create_default_mappers():
    return {
        "heart-rate": HeartRateMapper(),
        "heart-rate-variability": HeartRateVariabilityMapper(),
        "blood-pressure": BloodPressureMapper(),
        "oxygen-saturation": OxygenSaturationMapper(),
        "respiratory-rate": RespiratoryRateMapper(),
        "body-temperature": BodyTemperatureMapper(),
        "total-sleep-time": TotalSleepTimeMapper(),
        "sleep-episode": SleepEpisodeMapper(),
        "physical-activity": PhysicalActivityMapper(),
        "step-count": StepCountMapper(),
        "kcal-burned": CaloriesBurnedMapper(),
    }
