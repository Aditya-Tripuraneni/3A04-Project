Use your virtualenv of choice (anaconda, uv, ensurevenv), then do `pip install -r requirements.<platform>.txt` for local development

Recommend [uv](https://docs.astral.sh/uv/) for simplicity and fast setup.

Then run `bentoml serve`:

```bash
bentoml serve service.py
```

Then access at `http://localhost:3000/v1/docs` for gateway.

For deployment ask `@aarnphm` (if you have bentocloud account, then do `bentoml deploy .`)

But you also need to setup ADC

## Development

If you add a new dependencies, then you should do it in `pyproject.toml` `dependencies` keys then run `make all` to generate platform-specific lockfiles.

For formatting the code just run `uv run ruff format`

## Endpoints

- `/v1/analyze`: three dispatchers to each agent.
