from sensrbio_omh.mappers.physical_activity import PhysicalActivityMapper
from sensrbio_omh.mappers.step_count import StepCountMapper
from sensrbio_omh.schemas.types import SensrActivity


def test_maps_physical_activity(sensr_activities):
    activities = [SensrActivity.model_validate(x) for x in sensr_activities["data"]]
    pts = PhysicalActivityMapper().map(activities[0])
    assert len(pts) == 1
    assert pts[0].header.schema_id.name == "physical-activity"
    assert pts[0].body.duration and pts[0].body.duration.unit == "s"
    assert pts[0].body.distance and pts[0].body.distance.unit == "m"
    assert pts[0].body.calories_burned and pts[0].body.calories_burned.unit == "kcal"


def test_maps_step_count_from_activity(sensr_activities):
    activities = [SensrActivity.model_validate(x) for x in sensr_activities["data"]]
    pts = StepCountMapper().map(activities[0])
    assert len(pts) == 1
    assert pts[0].header.schema_id.name == "step-count"
    assert pts[0].body.step_count == 3200
