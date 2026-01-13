import aiohttp

class DeribitClient:
    BASE_URL = "https://www.deribit.com/api/v2/public/get_index_price"

    async def fetch_price(self, ticker: str):
        params = {"index_name": f"{ticker.lower()}_usd"}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("result", {}).get("index_price")
                return None