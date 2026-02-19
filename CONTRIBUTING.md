# Contributing

Thanks for your interest in contributing to `sensrbio-openmhealth`! This project maintains feature parity between Node/TypeScript and Python implementations, so please keep both in sync when making changes.

## Getting Started

```bash
git clone https://github.com/AuBioSensorBio/sensrbio-openmhealth.git
cd sensrbio-openmhealth
```

### Node/TypeScript

```bash
cd node
npm install
npm test        # run tests
npm run build   # compile
npm run lint    # type-check
```

### Python

```bash
cd python
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest          # run tests
ruff check .    # lint
ruff format .   # format
```

## Making Changes

### Adding a new OMH mapper

1. **Both languages**: Add the mapper in `node/src/mappers/` and `python/sensrbio_omh/mappers/`
2. Register it in the mapper index/registry for both
3. Add test fixtures in `node/tests/fixtures/` and `python/tests/fixtures/`
4. Add unit tests for both implementations
5. Update `docs/MAPPING.md` with the field-level mapping rules
6. Update `docs/SCHEMA-VERSIONS.md` if targeting a new OMH schema version

### Modifying mapping logic

If you change how a Sensr field maps to an OMH field, update **both** implementations to stay in sync.

### Updating the Sensr client

If the Sensr API adds new endpoints, update both clients:
- `node/src/client/sensr-client.ts`
- `python/sensrbio_omh/client/sensr_client.py`

## Code Style

- **TypeScript**: Strict mode, ESM, no `any` where avoidable
- **Python**: Type hints everywhere, Pydantic v2 models, ruff for linting/formatting

## Pull Request Process

1. Fork the repo and create a feature branch
2. Make your changes in both languages (if applicable)
3. Ensure all tests pass: `npm test` (node) and `pytest` (python)
4. Update documentation if mapping logic changes
5. Submit a PR with a clear description of what changed and why

## Reporting Issues

Please include:
- Which language (Node, Python, or both)
- Sensr API response sample (anonymized) if relevant
- Expected vs actual OMH output
- Version of the package you're using
