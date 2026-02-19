import pytest

from sensrbio_omh.mappers.heart_rate import HeartRateMapper
from sensrbio_omh.mappers.heart_rate_variability import HeartRateVariabilityMapper
from sensrbio_omh.mappers.oxygen_saturation import OxygenSaturationMapper
from sensrbio_omh.schemas.types import SensrBiometric


def test_maps_heart_rate(sensr_biometrics):
    biometrics = [SensrBiometric.model_validate(x) for x in sensr_biometrics["data"]]
    hr = next(b for b in biometrics if b.type == "heart_rate")
    pts = HeartRateMapper().map(hr)
    assert len(pts) == 1
    assert pts[0].header.schema_id.name == "heart-rate"
    assert pts[0].body.heart_rate.unit == "beats/min"
    assert pts[0].body.heart_rate.value == 62


def test_maps_oxygen_saturation_normalizes_percent(sensr_biometrics):
    biometrics = [SensrBiometric.model_validate(x) for x in sensr_biometrics["data"]]
    sp = next(b for b in biometrics if b.type == "spo2")
    pts = OxygenSaturationMapper().map(sp)
    assert len(pts) == 1
    assert pts[0].body.oxygen_saturation.unit == "%"
    assert pts[0].body.oxygen_saturation.value == pytest.approx(97.5, rel=1e-3)


def test_maps_hrv_rmssd_preferred(sensr_biometrics):
    biometrics = [SensrBiometric.model_validate(x) for x in sensr_biometrics["data"]]
    hrv = next(b for b in biometrics if b.type == "hrv")
    pts = HeartRateVariabilityMapper().map(hrv)
    assert len(pts) == 1
    assert pts[0].header.schema_id.name == "heart-rate-variability"
    assert pts[0].body.heart_rate_variability.unit == "ms"
    assert pts[0].body.heart_rate_variability.value == pytest.approx(42.5, rel=1e-2)
    assert pts[0].body.measure == "RMSSD"
