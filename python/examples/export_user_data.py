import asyncio
import json
import os

from dotenv import load_dotenv

from sensrbio_omh.client.sensr_client import SensrClient
from sensrbio_omh.converters.sensr_to_omh import SensrToOmhConverter


async def main() -> None:
    load_dotenv()
    api_key = os.environ["SENSR_API_KEY"]
    user_id = os.environ.get("SENSR_USER_ID", "user")
    start_date = os.environ.get("START_DATE", "2026-01-01")
    end_date = os.environ.get("END_DATE", "2026-01-07")

    async with SensrClient(api_key=api_key) as client:
        conv = SensrToOmhConverter(client)
        points = await conv.convert_all(user_id=user_id, start_date=start_date, end_date=end_date)
        print(json.dumps([p.model_dump(mode="json") for p in points], indent=2))


if __name__ == "__main__":
    asyncio.run(main())
