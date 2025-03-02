from aiohttp import ClientSession
from typing import List, Optional, Dict, Any

class KleinanzeigenAPI:
    # Make a HTTP requests to kleinanzeigen

    ENDPOINT: str = "https://www.kleinanzeigen.de/s-suchanfrage.html"
    
    def __init__(self):
        self.session = ClientSession()

    # Returns default params
    @property
    def default_params(self) -> Dict[str, Optional[str]]:
        return {
            "sortingField":"SORTING_DATE",
            "action":"find",
            "buyNowEnabled":"false",
            "adType":None,
            "posterType":None,
            "shippingCarrier":None 
        }

    # Closes client session
    async def close(self) -> None:
        await self.session.close()

    # Preparing params, replace None to empty string
    def prepare_params_dict(self, params: Dict[str, Optional[Any]]) -> Dict[str, str]:
        return {k: str(v) if v is not None else "" for k, v in params.items()}

    # Search offers from kleinanzeigen and return HTML content
    async def fetch_ads_page(
            self, 
            keywords: List[str],
            page_num: int = 1,
            max_price: int = None, 
            min_price: int = None, 
            radius: int = 1,
            location: str = None,
            category_id: int = None,
            location_id: int = None,
    ) -> Optional[str]:
        params = {
            "keywords":keywords,
            "categoryId":category_id,
            "locationStr":location,
            "radius":radius,
            "maxPrice":max_price,
            "minPrice":min_price,
            "pageNum":page_num,
            "locationId":location_id,
        }
        params.update(self.default_params)
        params |= self.prepare_params_dict(params)
        async with self.session.get(self.ENDPOINT, params=params) as response:
            return await response.text()

    async def fetch_details_page(url: str) -> Optional[str]:
        pass