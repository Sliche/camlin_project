import httpx
import json
import os
from typing import Literal, Optional
from dotenv import load_dotenv
load_dotenv()


class NBPClient:
    BASE_URL = os.getenv("BANK_API_URL")

    def __init__(self):
        self.client = httpx.AsyncClient(base_url=self.BASE_URL, headers={"Accept": "application/json"})

    async def get_current_rate(self, currency: str) -> Optional[dict]:
        for table in ["A", "B"]:
            url = f"/exchangerates/rates/{table}/{currency.upper()}/"
            try:
                response = await self.client.get(url)
                response.raise_for_status()
                return response.json()["rates"][0]["mid"]
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    continue  # Try next table
                raise

        # Not found in A or B
        return None

    async def get_exchange_table(self, table: Literal["A", "B", "C"] = "A") -> dict:
        url = f"/exchangerates/tables/{table}/"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()


    async def close(self):
        await self.client.aclose()
