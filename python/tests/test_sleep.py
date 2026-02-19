from sensrbio_omh.mappers.sleep_episode import SleepEpisodeMapper
from sensrbio_omh.mappers.total_sleep_time import TotalSleepTimeMapper
from sensrbio_omh.schemas.types import SensrSleepDetailsDay, SensrSleepSummary


def test_maps_total_sleep_time(sensr_sleep):
    summary = SensrSleepSummary.model_validate(sensr_sleep["summary"])
    pts = TotalSleepTimeMapper().map(summary)
    assert len(pts) == 1
    assert pts[0].header.schema_id.name == "total-sleep-time"
    assert pts[0].body.total_sleep_time.unit == "min"
    assert pts[0].body.total_sleep_time.value == 420


def test_maps_sleep_episode_segments(sensr_sleep):
    details = SensrSleepDetailsDay.model_validate(sensr_sleep["details_day"])
    pts = SleepEpisodeMapper().map(details)
    assert len(pts) > 0
    types = {p.body.sleep_episode.sleep_episode_type for p in pts}
    assert "in_bed" in types
    assert "light_sleep" in types
    assert "deep_sleep" in types
    assert "awake" in types
    assert "rem_sleep" in types
