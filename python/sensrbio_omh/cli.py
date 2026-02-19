from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

import click
from dotenv import load_dotenv

from sensrbio_omh.client.sensr_client import SensrClient
from sensrbio_omh.converters.sensr_to_omh import SensrToOmhConverter
from sensrbio_omh.mappers import MapperType


@click.group()
def main() -> None:
    """Sensr → OMH export CLI."""


@main.command()
@click.option("--user-id", required=True, type=str)
@click.option("--start", "start_date", required=True, type=str, help="YYYY-MM-DD")
@click.option("--end", "end_date", required=True, type=str, help="YYYY-MM-DD")
@click.option("--type", "type_", type=str, help="OMH type (e.g. heart-rate)")
@click.option("--all", "all_", is_flag=True, help="Export all supported OMH types")
@click.option("--output", type=click.Path(dir_okay=False, path_type=Path), default=None)
def export(user_id: str, start_date: str, end_date: str, type_: str | None, all_: bool, output: Path | None) -> None:
    """Export a user's Sensr data to OMH datapoints."""

    load_dotenv(override=False)
    api_key = os.getenv("SENSR_API_KEY")
    base_url = os.getenv("SENSR_BASE_URL", "https://api.getsensr.io")

    if not api_key:
        raise click.ClickException("Missing SENSR_API_KEY (set env var or .env)")

    async def _run() -> list[dict]:
        async with SensrClient(api_key=api_key, base_url=base_url) as client:
            conv = SensrToOmhConverter(client)
            if all_:
                points = await conv.convert_all(user_id=user_id, start_date=start_date, end_date=end_date)
            else:
                if not type_:
                    raise click.ClickException("Provide --type or use --all")
                points = await conv.convert_by_type(
                    user_id=user_id, start_date=start_date, end_date=end_date, type=type_  # type: ignore[arg-type]
                )
            return [p.model_dump(mode="json") for p in points]

    data = asyncio.run(_run())
    text = json.dumps(data, indent=2)
    if output:
        output.write_text(text + "\n", encoding="utf-8")
    else:
        click.echo(text)
