import json
from pathlib import Path

import pytest


@pytest.fixture()
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture()
def sensr_biometrics(fixtures_dir: Path):
    return json.loads((fixtures_dir / "sensr-biometrics.json").read_text(encoding="utf-8"))


@pytest.fixture()
def sensr_sleep(fixtures_dir: Path):
    return json.loads((fixtures_dir / "sensr-sleep.json").read_text(encoding="utf-8"))


@pytest.fixture()
def sensr_activities(fixtures_dir: Path):
    return json.loads((fixtures_dir / "sensr-activities.json").read_text(encoding="utf-8"))
