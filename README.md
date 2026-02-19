<p align="center">
  <h1 align="center">sensrbio-openmhealth</h1>
  <p align="center">
    Export <a href="https://getsensr.io">Sensor Bio</a> health data as <a href="https://www.openmhealth.org/">Open mHealth</a> compliant JSON
  </p>
</p>

<p align="center">
  <a href="https://github.com/SensorBio/sensrbio-openmhealth/actions/workflows/ci.yml"><img src="https://github.com/SensorBio/sensrbio-openmhealth/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://www.openmhealth.org/"><img src="https://img.shields.io/badge/standard-Open%20mHealth-00B894.svg" alt="Open mHealth"></a>
  <a href="./node"><img src="https://img.shields.io/badge/node-%3E%3D20-339933?logo=node.js&logoColor=white" alt="Node >= 20"></a>
  <a href="./python"><img src="https://img.shields.io/badge/python-%3E%3D3.11-3776AB?logo=python&logoColor=white" alt="Python >= 3.11"></a>
  <a href="https://github.com/SensorBio/sensrbio-openmhealth"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
</p>

---

## What is Open mHealth?

[Open mHealth](https://www.openmhealth.org/) (OMH) is an open standard for representing mobile health data. It defines a library of **reusable, composable JSON schemas** for common health data types like heart rate, blood pressure, sleep, physical activity, and more.

**Why it matters:**

- **Interoperability**: Health data from different wearables and apps can be represented in a single, consistent format. A heart rate reading looks the same whether it came from a Sensr device, Apple Watch, Fitbit, or Oura Ring.
- **Standardized schemas**: Each data type (heart rate, SpO2, sleep, etc.) has a formally defined JSON schema with required fields, units, and validation rules. No more guessing what `value: 72` means.
- **Research-ready**: OMH is used in clinical research and digital health platforms. Exporting in OMH format means your data can plug directly into research pipelines, EHR systems, and analytics platforms.
- **IEEE 1752 alignment**: Many OMH schemas have been adopted into the [IEEE 1752](https://standards.ieee.org/ieee/1752/10069/) standard for mobile health data.

Every OMH data point follows a standard envelope:

```json
{
  "header": {
    "id": "unique-id",
    "creation_date_time": "2026-02-07T12:00:00Z",
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
    "heart_rate": { "value": 72, "unit": "beats/min" },
    "effective_time_frame": { "date_time": "2026-02-07T08:30:00Z" }
  }
}
```

Learn more: [Open mHealth Documentation](https://www.openmhealth.org/documentation/) | [OMH Schemas on GitHub](https://github.com/openmhealth/schemas)

---

## What This Repo Does

This library connects to the [Sensr Bio API](https://developers.getsensr.io/) and converts raw wearable data (biometrics, sleep, activities, calories) into Open mHealth compliant JSON data points.

**Use it when you need to:**
- Export Sensr data into a standardized format for research or clinical use
- Feed wearable data into systems that speak Open mHealth (EHRs, FHIR servers, analytics platforms)
- Build interoperability layers between Sensr and other health data ecosystems

Available in **two languages** with feature parity:

| | Node/TypeScript | Python |
|---|---|---|
| **Directory** | [`node/`](./node/) | [`python/`](./python/) |
| **Package** | `@sensrbio/openmhealth` | `sensrbio-openmhealth` |
| **Runtime** | Node >= 20 | Python >= 3.11 |
| **HTTP Client** | `fetch` (built-in) | `httpx` (async) |
| **Models** | TypeScript interfaces | Pydantic v2 |
| **CLI** | `sensr-to-omh` | `sensr-to-omh` |
| **Tests** | vitest | pytest |
| **Docs** | [`node/README.md`](./node/README.md) | [`python/README.md`](./python/README.md) |

---

## Supported Data Types

| Sensr API | Sensr Field | OMH Schema | Version |
|-----------|-------------|------------|---------|
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

Detailed field-level mapping rules: [`docs/MAPPING.md`](./docs/MAPPING.md)

---

## Quick Start

### Node / TypeScript

```bash
cd node && npm install
```

```typescript
import { SensrClient, SensrToOmhConverter } from '@sensrbio/openmhealth';

const client = new SensrClient({ apiKey: process.env.SENSR_API_KEY! });
const converter = new SensrToOmhConverter(client);

const points = await converter.convertAll({
  userId: 'user_abc123',
  dateRange: { startDate: '2026-02-01', endDate: '2026-02-07' },
});

console.log(JSON.stringify(points, null, 2));
```

**CLI:**

```bash
sensr-to-omh --api-key "$SENSR_API_KEY" --user-id user_abc123 \
  --start-date 2026-02-01 --end-date 2026-02-07 --pretty
```

Full docs: [`node/README.md`](./node/README.md)

### Python

```bash
cd python && pip install -e .
```

```python
import asyncio
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
    print(f"Exported {len(points)} OMH data points")

asyncio.run(main())
```

**CLI:**

```bash
sensr-to-omh export --api-key "$SENSR_API_KEY" --user-id user_abc123 \
  --start 2026-02-01 --end 2026-02-07
```

Full docs: [`python/README.md`](./python/README.md)

---

## Architecture

```
sensrbio-openmhealth/
├── README.md                   ← you are here
├── LICENSE                     ← MIT
├── CONTRIBUTING.md             ← contribution guide
├── .github/workflows/ci.yml   ← GitHub Actions CI (Node 20/22 + Python 3.11/3.12/3.13)
├── docs/
│   ├── MAPPING.md              ← field-level Sensr → OMH mapping rules
│   └── SCHEMA-VERSIONS.md     ← which OMH schema versions we target
├── node/                       ← Node/TypeScript implementation
│   ├── README.md
│   ├── src/
│   │   ├── client/             ← Sensr API client (fetch, auto-pagination)
│   │   ├── schemas/            ← OMH TypeScript types
│   │   ├── mappers/            ← 11 data type mappers
│   │   ├── converters/         ← high-level converter
│   │   └── cli.ts              ← CLI entry point
│   └── tests/
└── python/                     ← Python implementation
    ├── README.md
    ├── sensrbio_omh/
    │   ├── client/             ← Sensr API client (httpx async, auto-pagination)
    │   ├── schemas/            ← OMH Pydantic v2 models
    │   ├── mappers/            ← 11 data type mappers
    │   ├── converters/         ← high-level converter
    │   └── cli.py              ← CLI entry point (Click)
    └── tests/
```

Both implementations share the same:
- Mapping logic (SpO2 normalization, F→C temp conversion, HRV RMSSD/SDNN preference, sleep stage mapping)
- Test fixture data
- Documentation

---

## Configuration

Both implementations read from environment variables or accept config at initialization:

| Variable | Required | Description |
|----------|----------|-------------|
| `SENSR_API_KEY` | Yes | Your Sensr organization API key |
| `SENSR_BASE_URL` | No | Override API base URL (default: `https://api.getsensr.io`) |

Get your API key from the [Sensr Web Dashboard](https://platform.getsensr.io) → Developers menu.

---

## Running Tests

```bash
# Node
cd node && npm test

# Python
cd python && pytest
```

CI runs on every push and PR against `main`:
- Node: tested on v20 and v22
- Python: tested on 3.11, 3.12, and 3.13

---

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for guidelines. When adding or modifying mappers, please update both language implementations to maintain feature parity.

---

## Related Resources

- [Sensr API Documentation](https://developers.getsensr.io/)
- [Open mHealth Documentation](https://www.openmhealth.org/documentation/)
- [OMH Schemas (GitHub)](https://github.com/openmhealth/schemas)
- [IEEE 1752 Standard](https://standards.ieee.org/ieee/1752/10069/)
- [FHIR OMH-to-FHIR Mapping](https://build.fhir.org/ig/HL7/openmhealth/)

---

## License

MIT — see [`LICENSE`](./LICENSE)
