# sensrbio-openmhealth

Export [Sensor Bio](https://getsensr.io) health data as [Open mHealth](https://www.openmhealth.org/) compliant JSON.

Pulls biometrics, sleep, activity, and calorie data from the Sensr API and converts it into standardized OMH data points that any OMH-compatible system can consume.

---

## Table of Contents

- [Supported Data Types](#supported-data-types)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage as a Library](#usage-as-a-library)
- [Usage as a CLI](#usage-as-a-cli)
- [Output Format](#output-format)
- [API Reference](#api-reference)
- [Development](#development)
- [License](#license)

---

## Supported Data Types

| Sensr API Endpoint | Sensr Field | OMH Schema | Version |
|--------------------|-------------|------------|---------|
| `/v1/biometrics` | `heart_rate` | `omh:heart-rate` | 2.0 |
| `/v1/biometrics` | `hrv` | `omh:heart-rate-variability` | 1.0 |
| `/v1/biometrics` | `blood_pressure` | `omh:blood-pressure` | 2.0 |
| `/v1/biometrics` | `spo2` | `omh:oxygen-saturation` | 2.0 |
| `/v1/biometrics` | `respiration_rate` | `omh:respiratory-rate` | 2.0 |
| `/v1/biometrics` | `temperature` | `omh:body-temperature` | 2.0 |
| `/v1/sleep` | summary | `omh:total-sleep-time` | 2.0 |
| `/v1/sleep/details/day` | segments | `omh:sleep-episode` | 2.0 |
| `/v1/activities` | activity | `omh:physical-activity` | 2.0 |
| `/v1/activities` | steps | `omh:step-count` | 2.0 |
| `/v1/calorie/details` | buckets | `omh:kcal-burned` | 2.0 |

See [`docs/MAPPING.md`](docs/MAPPING.md) for detailed field-level mapping rules.

---

## Installation

### From source

```bash
git clone https://github.com/sensrbio/sensrbio-openmhealth-python.git
cd sensrbio-openmhealth-python
pip install .
```

### For development

```bash
pip install -e ".[dev]"
```

### Requirements

- Python 3.11+
- Dependencies: `httpx`, `pydantic` (v2), `click`, `python-dotenv`

---

## Configuration

Copy `.env.example` to `.env` and set your values:

```bash
cp .env.example .env
```

```env
# Required: Your Sensr organization API key
SENSR_API_KEY=your-api-key-here

# Optional: Override the Sensr API base URL (default: https://api.getsensr.io)
SENSR_BASE_URL=https://api.getsensr.io
```

You can get your API key from the [Sensr Web Dashboard](https://platform.getsensr.io) under the Developers menu.

---

## Usage as a Library

### Basic: Export all data types for a user

```python
import asyncio
import json
from sensrbio_omh.client.sensr_client import SensrClient
from sensrbio_omh.converters.sensr_to_omh import SensrToOmhConverter

async def main():
    client = SensrClient(api_key="your-api-key")
    converter = SensrToOmhConverter(client)

    # Export all supported data types for a date range
    data_points = await converter.convert_all(
        user_id="user_abc123",
        start_date="2026-02-01",
        end_date="2026-02-07",
    )

    print(f"Exported {len(data_points)} OMH data points")
    print(json.dumps([dp.model_dump() for dp in data_points], indent=2))

asyncio.run(main())
```

### Export a specific data type

```python
import asyncio
from sensrbio_omh.client.sensr_client import SensrClient
from sensrbio_omh.converters.sensr_to_omh import SensrToOmhConverter

async def main():
    client = SensrClient(api_key="your-api-key")
    converter = SensrToOmhConverter(client)

    # Export only heart rate data
    hr_points = await converter.convert_by_type(
        user_id="user_abc123",
        start_date="2026-02-01",
        end_date="2026-02-07",
        data_type="heart-rate",
    )

    # Available types:
    # "heart-rate", "heart-rate-variability", "blood-pressure",
    # "oxygen-saturation", "respiratory-rate", "body-temperature",
    # "total-sleep-time", "sleep-episode", "physical-activity",
    # "step-count", "kcal-burned"

asyncio.run(main())
```

### Use the Sensr client directly

```python
import asyncio
from sensrbio_omh.client.sensr_client import SensrClient

async def main():
    client = SensrClient(
        api_key="your-api-key",
        base_url="https://api.getsensr.io",  # optional
    )

    # Fetch raw biometrics (auto-paginated)
    biometrics = await client.get_biometrics(
        user_id="user_abc123",
        start_time_ms=1738368000000,
        end_time_ms=1738972800000,
    )

    # Fetch sleep summary for a specific day
    sleep = await client.get_sleep(
        user_id="user_abc123",
        date="2026-02-05",
    )

    # Fetch activities (auto-paginated)
    activities = await client.get_activities(
        user_id="user_abc123",
        start_time_ms=1738368000000,
        end_time_ms=1738972800000,
    )

    # Fetch calorie details with granularity
    calories = await client.get_calorie_details(
        user_id="user_abc123",
        granularity="week",
        start_date="2026-02-01",
        end_date="2026-02-07",
    )

asyncio.run(main())
```

### Use individual mappers

```python
from sensrbio_omh.schemas.types import SensrBiometric
from sensrbio_omh.mappers.heart_rate import HeartRateMapper

mapper = HeartRateMapper()

sensr_record = SensrBiometric(
    id="bio_001",
    user_id="user_abc123",
    type="heart_rate",
    timestamp_ms=1738368000000,
    value=72,
)

omh_data_points = mapper.map(sensr_record)
# Returns a list of OmhDataPoint[OmhHeartRate]
```

### Write to file

```python
import asyncio
import json
from sensrbio_omh.client.sensr_client import SensrClient
from sensrbio_omh.converters.sensr_to_omh import SensrToOmhConverter

async def main():
    client = SensrClient(api_key="your-api-key")
    converter = SensrToOmhConverter(client)

    points = await converter.convert_all(
        user_id="user_abc123",
        start_date="2026-02-01",
        end_date="2026-02-07",
    )

    with open("omh-export.json", "w") as f:
        json.dump([dp.model_dump() for dp in points], f, indent=2)

    print(f"Wrote {len(points)} data points to omh-export.json")

asyncio.run(main())
```

### Use with pandas (data analysis)

```python
import asyncio
import pandas as pd
from sensrbio_omh.client.sensr_client import SensrClient
from sensrbio_omh.converters.sensr_to_omh import SensrToOmhConverter

async def main():
    client = SensrClient(api_key="your-api-key")
    converter = SensrToOmhConverter(client)

    points = await converter.convert_by_type(
        user_id="user_abc123",
        start_date="2026-02-01",
        end_date="2026-02-28",
        data_type="heart-rate",
    )

    # Flatten to a DataFrame
    rows = []
    for dp in points:
        body = dp.body
        rows.append({
            "timestamp": dp.header.creation_date_time,
            "heart_rate_bpm": body.heart_rate.value,
        })

    df = pd.DataFrame(rows)
    print(df.describe())

asyncio.run(main())
```

---

## Usage as a CLI

### Export all data types

```bash
sensr-to-omh export \
  --api-key "$SENSR_API_KEY" \
  --user-id "user_abc123" \
  --start "2026-02-01" \
  --end "2026-02-07" \
  --output omh-export.json
```

### Export a specific type

```bash
sensr-to-omh export \
  --api-key "$SENSR_API_KEY" \
  --user-id "user_abc123" \
  --start "2026-02-01" \
  --end "2026-02-07" \
  --type heart-rate \
  --output heart-rate.json
```

### Export to stdout (pipe to jq, etc.)

```bash
sensr-to-omh export \
  --api-key "$SENSR_API_KEY" \
  --user-id "user_abc123" \
  --start "2026-02-01" \
  --end "2026-02-07" \
  | jq '.[].header.schema_id.name' | sort | uniq -c
```

### Export all types to stdout

```bash
sensr-to-omh export \
  --api-key "$SENSR_API_KEY" \
  --user-id "user_abc123" \
  --start "2026-02-01" \
  --end "2026-02-07" \
  --all
```

### CLI Options

```
sensr-to-omh export [OPTIONS]

Options:
  --api-key TEXT     Sensr org API key (or SENSR_API_KEY env var)
  --base-url TEXT    Sensr API base URL (default: https://api.getsensr.io)
  --user-id TEXT     Sensr user ID to export
  --start TEXT       Start date, inclusive (YYYY-MM-DD)
  --end TEXT         End date, inclusive (YYYY-MM-DD)
  --type TEXT        Specific OMH data type to export (omit for all)
  --all              Export all data types (default if --type not set)
  --output TEXT      Output file path (default: stdout)
  --help             Show help
```

### Using environment variables

```bash
export SENSR_API_KEY="your-key"
sensr-to-omh export --user-id user_abc123 --start 2026-02-01 --end 2026-02-07
```

---

## Output Format

Every data point follows the [Open mHealth data point schema](https://www.openmhealth.org/documentation/#/schema-docs/schema-library):

```json
{
  "header": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "creation_date_time": "2026-02-07T12:00:00.000Z",
    "schema_id": {
      "namespace": "omh",
      "name": "heart-rate",
      "version": "2.0"
    },
    "acquisition_provenance": {
      "source_name": "Sensr Bio",
      "modality": "sensed"
    }
  },
  "body": {
    "heart_rate": {
      "value": 72,
      "unit": "beats/min"
    },
    "effective_time_frame": {
      "date_time": "2026-02-05T08:30:00.000Z"
    }
  }
}
```

### More examples

<details>
<summary>Blood Pressure</summary>

```json
{
  "body": {
    "systolic_blood_pressure": { "value": 120, "unit": "mmHg" },
    "diastolic_blood_pressure": { "value": 80, "unit": "mmHg" },
    "effective_time_frame": { "date_time": "2026-02-05T09:00:00.000Z" }
  }
}
```
</details>

<details>
<summary>Oxygen Saturation</summary>

```json
{
  "body": {
    "oxygen_saturation": { "value": 98.5, "unit": "%" },
    "effective_time_frame": { "date_time": "2026-02-05T08:30:00.000Z" }
  }
}
```
</details>

<details>
<summary>Sleep Episode</summary>

```json
{
  "body": {
    "sleep_episode": {
      "sleep_episode_type": "deep_sleep",
      "time_interval": {
        "start_date_time": "2026-02-05T01:30:00.000Z",
        "end_date_time": "2026-02-05T02:45:00.000Z"
      }
    },
    "effective_time_frame": {
      "time_interval": {
        "start_date_time": "2026-02-05T01:30:00.000Z",
        "end_date_time": "2026-02-05T02:45:00.000Z"
      }
    }
  }
}
```
</details>

<details>
<summary>Step Count</summary>

```json
{
  "body": {
    "step_count": 8432,
    "effective_time_frame": {
      "time_interval": {
        "start_date_time": "2026-02-05T06:00:00.000Z",
        "end_date_time": "2026-02-05T22:00:00.000Z"
      }
    }
  }
}
```
</details>

---

## API Reference

### `SensrClient`

```python
SensrClient(
    api_key: str,
    base_url: str = "https://api.getsensr.io",
    headers: dict[str, str] | None = None,
)
```

| Method | Returns | Description |
|--------|---------|-------------|
| `get_biometrics(user_id, start_time_ms?, end_time_ms?, limit?)` | `list[SensrBiometric]` | Paginated biometrics |
| `get_activities(user_id, start_time_ms?, end_time_ms?, limit?)` | `list[SensrActivity]` | Paginated activities |
| `get_sleep(user_id, date)` | `SensrSleepSummary` | Sleep summary for a date |
| `get_sleep_details_day(user_id, date)` | `SensrSleepDetailsDay` | Sleep segments for a date |
| `get_calorie_details(user_id, granularity, start_date, end_date)` | `SensrCalorieDetailsResponse` | Calorie data |
| `get_scores(user_id, date)` | `dict` | Daily scores |
| `get_vitals(user_id, start_time_ms?, end_time_ms?, limit?)` | `list[SensrVitals]` | Paginated vitals |

### `SensrToOmhConverter`

```python
SensrToOmhConverter(client: SensrClient)
```

| Method | Returns | Description |
|--------|---------|-------------|
| `convert_all(user_id, start_date, end_date)` | `list[OmhDataPoint]` | Export all 11 types |
| `convert_by_type(user_id, start_date, end_date, data_type)` | `list[OmhDataPoint]` | Export one specific type |

---

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=sensrbio_omh

# Lint
ruff check .

# Format
ruff format .
```

---

## Contributing

PRs welcome. When changing mapping logic, please update:
1. The mapper + its unit test
2. Test fixtures in `tests/fixtures/`
3. `docs/MAPPING.md`

---

## License

MIT
