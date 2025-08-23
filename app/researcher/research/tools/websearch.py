import aiohttp
from ... import constant

class WebSearchTool:
    def __init__(self):
        self.api_key = constant.serp_ai_api_key
        self.base_url = constant.serp_url

    async def search(self, query: str):
        params = {
            "q": query,
            "api_key": self.api_key,
            "engine": "google"
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("organic_results", [])
                    else:
                        print(f"[WebSearch Error] Status: {response.status}")
                        return []
        except Exception as e:
            print(f"[WebSearch Exception] {str(e)}")
            return []
        
        finally:
            await session.close()
