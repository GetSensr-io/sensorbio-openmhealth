# @sensrbio/openmhealth

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

See [`docs/MAPPING.md`](../docs/MAPPING.md) for detailed field-level mapping rules.

---

## Installation

```bash
# npm
npm install @sensrbio/openmhealth

# yarn
yarn add @sensrbio/openmhealth

# pnpm
pnpm add @sensrbio/openmhealth
```

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

```typescript
import { SensrClient, SensrToOmhConverter } from '@sensrbio/openmhealth';

const client = new SensrClient({ apiKey: process.env.SENSR_API_KEY! });
const converter = new SensrToOmhConverter(client);

// Export all supported data types for a date range
const dataPoints = await converter.convertAll({
  userId: 'user_abc123',
  dateRange: {
    startDate: '2026-02-01',
    endDate: '2026-02-07',
  },
});

console.log(`Exported ${dataPoints.length} OMH data points`);
console.log(JSON.stringify(dataPoints, null, 2));
```

### Export a specific data type

```typescript
import { SensrClient, SensrToOmhConverter } from '@sensrbio/openmhealth';

const client = new SensrClient({ apiKey: process.env.SENSR_API_KEY! });
const converter = new SensrToOmhConverter(client);

// Export only heart rate data
const heartRatePoints = await converter.convertByType(
  {
    userId: 'user_abc123',
    dateRange: { startDate: '2026-02-01', endDate: '2026-02-07' },
  },
  'heart-rate'
);

// Available types:
// 'heart-rate' | 'heart-rate-variability' | 'blood-pressure' |
// 'oxygen-saturation' | 'respiratory-rate' | 'body-temperature' |
// 'total-sleep-time' | 'sleep-episode' | 'physical-activity' |
// 'step-count' | 'kcal-burned'
```

### Use the Sensr client directly

```typescript
import { SensrClient } from '@sensrbio/openmhealth';

const client = new SensrClient({
  apiKey: process.env.SENSR_API_KEY!,
  baseUrl: 'https://api.getsensr.io', // optional
});

// Fetch raw biometrics (auto-paginated)
const biometrics = await client.getBiometrics({
  userId: 'user_abc123',
  startTimeMs: Date.parse('2026-02-01T00:00:00Z'),
  endTimeMs: Date.parse('2026-02-07T23:59:59Z'),
});

// Fetch sleep summary for a specific day
const sleep = await client.getSleep({
  userId: 'user_abc123',
  date: '2026-02-05',
});

// Fetch activities (auto-paginated)
const activities = await client.getActivities({
  userId: 'user_abc123',
  startTimeMs: Date.parse('2026-02-01T00:00:00Z'),
  endTimeMs: Date.parse('2026-02-07T23:59:59Z'),
});

// Fetch calorie details with granularity
const calories = await client.getCalorieDetails({
  userId: 'user_abc123',
  granularity: 'week',
  startDate: '2026-02-01',
  endDate: '2026-02-07',
});
```

### Use individual mappers

```typescript
import { HeartRateMapper } from '@sensrbio/openmhealth';
import type { SensrBiometric } from '@sensrbio/openmhealth';

const mapper = new HeartRateMapper();

const sensrRecord: SensrBiometric = {
  id: 'bio_001',
  user_id: 'user_abc123',
  type: 'heart_rate',
  timestamp_ms: 1738368000000,
  value: 72,
};

const omhDataPoints = mapper.map(sensrRecord);
// Returns an array of OmhDataPoint<OmhHeartRate>
```

### Write to file

```typescript
import { writeFile } from 'node:fs/promises';
import { SensrClient, SensrToOmhConverter } from '@sensrbio/openmhealth';

const client = new SensrClient({ apiKey: process.env.SENSR_API_KEY! });
const converter = new SensrToOmhConverter(client);

const points = await converter.convertAll({
  userId: 'user_abc123',
  dateRange: { startDate: '2026-02-01', endDate: '2026-02-07' },
});

await writeFile('omh-export.json', JSON.stringify(points, null, 2));
console.log(`Wrote ${points.length} data points to omh-export.json`);
```

---

## Usage as a CLI

### Install globally

```bash
npm install -g @sensrbio/openmhealth
```

### Export all data types

```bash
sensr-to-omh \
  --api-key "$SENSR_API_KEY" \
  --user-id "user_abc123" \
  --start-date "2026-02-01" \
  --end-date "2026-02-07" \
  --pretty \
  --out omh-export.json
```

### Export to stdout (pipe to jq, etc.)

```bash
sensr-to-omh \
  --api-key "$SENSR_API_KEY" \
  --user-id "user_abc123" \
  --start-date "2026-02-01" \
  --end-date "2026-02-07" \
  | jq '.[] | select(.header.schema_id.name == "heart-rate")'
```

### CLI Options

```
sensr-to-omh [options]

Options:
  --api-key       Sensr org API key (or set SENSR_API_KEY env var)
  --base-url      Override Sensr API base URL (default: https://api.getsensr.io)
  --user-id       Sensr user ID to export data for
  --start-date    Start date, inclusive (YYYY-MM-DD)
  --end-date      End date, inclusive (YYYY-MM-DD)
  --out           Output file path (default: stdout)
  --pretty        Pretty-print JSON output
  --help, -h      Show help
```

### Using environment variables

All options can be set via env vars (CLI flags take precedence):

```bash
export SENSR_API_KEY="your-key"
export SENSR_USER_ID="user_abc123"
export START_DATE="2026-02-01"
export END_DATE="2026-02-07"

sensr-to-omh --pretty
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

### Example outputs by type

<details>
<summary>Blood Pressure</summary>

```json
{
  "header": { "schema_id": { "namespace": "omh", "name": "blood-pressure", "version": "2.0" } },
  "body": {
    "systolic_blood_pressure": { "value": 120, "unit": "mmHg" },
    "diastolic_blood_pressure": { "value": 80, "unit": "mmHg" },
    "effective_time_frame": { "date_time": "2026-02-05T09:00:00.000Z" }
  }
}
```
</details>

<details>
<summary>Sleep Episode</summary>

```json
{
  "header": { "schema_id": { "namespace": "omh", "name": "sleep-episode", "version": "2.0" } },
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
  "header": { "schema_id": { "namespace": "omh", "name": "step-count", "version": "2.0" } },
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

```typescript
new SensrClient(options: {
  apiKey: string;
  baseUrl?: string;       // default: https://api.getsensr.io
  headers?: Record<string, string>;
})
```

| Method | Returns | Description |
|--------|---------|-------------|
| `getBiometrics({userId, startTimeMs?, endTimeMs?, limit?})` | `SensrBiometric[]` | Paginated biometrics |
| `getActivities({userId, startTimeMs?, endTimeMs?, limit?})` | `SensrActivity[]` | Paginated activities |
| `getSleep({userId, date})` | `SensrSleepSummary` | Sleep summary for a date |
| `getSleepDetailsDay({userId, date})` | `SensrSleepDetailsDay` | Sleep segments for a date |
| `getCalorieDetails({userId, granularity, startDate, endDate})` | `SensrCalorieDetailsResponse` | Calorie data |
| `getScores({userId, date})` | Raw JSON | Daily scores |
| `getVitals({userId, startTimeMs?, endTimeMs?, limit?})` | `SensrVitals[]` | Paginated vitals |

### `SensrToOmhConverter`

```typescript
new SensrToOmhConverter(client: SensrClient)
```

| Method | Returns | Description |
|--------|---------|-------------|
| `convertAll({userId, dateRange})` | `OmhDataPoint<OmhBody>[]` | Export all 11 types |
| `convertByType({userId, dateRange}, type)` | `OmhDataPoint<OmhBody>[]` | Export one specific type |

---

## Development

```bash
# Install dependencies
npm install

# Run tests
npm test

# Build
npm run build

# Run in dev mode
npm run dev
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
