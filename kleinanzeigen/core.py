from typing import List
from .net import KleinanzeigenAPI
from .extract import extract, Offer

async def parse(
    keywords: List[str],
    page: int = 0,
    max_price: int = None,
    min_price: int = None,
    radius: int = 1,
    category_id: int = None,
    location_id: int = None 
) -> List[Offer]:
    api = KleinanzeigenAPI()
    resp = await api.fetch_ads_page(
        keywords=keywords,
        page_num=page,
        max_price=max_price,
        min_price=min_price,
        radius=radius,
        category_id=category_id,
        location_id=location_id
    )
    await api.close()
    return extract(resp)
