from typing import TypedDict, List, Optional, Any, Generator
from abc import ABC
from bs4 import BeautifulSoup
from bs4.element import Tag

from .utils import clear_string

class Offer(TypedDict):
    id: int
    title: str
    url: str
    image: Optional[str] = None
    created_at: str
    location: str
    description: str
    price: int
    discount: Optional[int] = None
    is_VB: bool
    delivery: bool
    top: bool
    pro: bool

class BaseExtractor(ABC):
    """
    BaseExtractor for extract datas from kleinanzeigen offer

    :param item: item html content from kleinanzeigen
    """

    def __init__(self):
        pass

    def extract(self, item: Tag)  -> Any:
        pass

class AttributeExtractor(BaseExtractor):
    """
    Extract attribute data
    """

    def __init__(self, attribute: str):
        self.attribute = attribute
        super().__init__()

    def extract(self, item: Tag):
        if item: return item.get(self.attribute)

class TextExtractor(BaseExtractor):
    """
    Extract text from element or returns Noen
    """
    def extract(self, item: Tag) -> Optional[str]:
        if hasattr(item, "find"): return "".join(item.findAll(text=True, recursive=False))

class TextExtractorByClass(TextExtractor):
    """
    Extract data from item by class

    :param class_name: class name of content
    """

    def __init__(self, tag: str, class_name: str):
        self.class_name = class_name
        self.tag = tag
        super().__init__()

    def extract(self, item: Tag):
        el = item.find(self.tag, attrs={"class":self.class_name})
        return super().extract(el)

class AttributeExtractorByTag(AttributeExtractor):
    """
    Extract attribute from item by class

    :param class_name: class name of content
    :param attribute: name of attribute
    :tag: name of tag
    """

    def __init__(self, tag: str, attribute: str):
        self.tag = tag
        super().__init__(attribute)

    def extract(self, item: Tag):
        el = item.find(self.tag)
        return super().extract(el)

class PriceExtractorByClass(TextExtractorByClass):
    """
    Extract price from kleinanzeigen content
    """

    SECURE_CHARS: List[str] = list("0123456789")

    def extract(self, item: Tag):
        unsecure_price = super().extract(item)
        if unsecure_price:
            secure_price = "".join([char for char in unsecure_price if char in self.SECURE_CHARS])
            if len(secure_price) > 0: return int(secure_price)

class ExistsInExtractorByClass(TextExtractorByClass):
    """
    Finding exists string in item and if exists returns True
    or not exists then returns False

    :string: string in content
    """

    def __init__(self, string: str, *args, **kwargs):
        self.string = string
        super().__init__(*args, **kwargs)

    def extract(self, item: Tag):
        element = super().extract(item)
        if element: return self.string in element

class ExistsInAttribute(AttributeExtractor):
    """
    Checks if in attribute exists string
    if exists returns True
    if not then returns False

    :string: string for existing
    """

    def __init__(self, string: str, *args, **kwargs):
        self.string = string
        super().__init__(*args, **kwargs)

    def extract(self, item):
        attribute = super().extract(item)
        if attribute: return self.string in attribute

_extractors = {
    "id":AttributeExtractorByTag(tag="article", attribute="data-adid"),
    "title":TextExtractorByClass(tag="a", class_name="ellipsis"),
    "url": AttributeExtractorByTag(tag="article", attribute="data-href"),
    "image":AttributeExtractorByTag("img", attribute="src"),
    "created_at":TextExtractorByClass(tag="div", class_name="aditem-main--top--right"),
    "location": TextExtractorByClass(tag="div", class_name="aditem-main--top--left"),
    "description": TextExtractorByClass(tag="p", class_name="aditem-main--middle--description"),
    "price": PriceExtractorByClass(tag="p", class_name="aditem-main--middle--price-shipping--price"),
    "discount": PriceExtractorByClass(tag="p", class_name="aditem-main--middle--price-shipping--old-price"),
    "is_VB":ExistsInExtractorByClass(tag="div", class_name="aditem-main--middle--price-shipping", string="VB"),
    "delivery":ExistsInExtractorByClass(tag="div", class_name="aditem-main--bottom", string="Versand möglich"), 
    "pro":ExistsInExtractorByClass(tag="div", class_name="aditem-main--bottom", string="PRO"),    
    "top":ExistsInAttribute(attribute="class", string="is-topad")
}

def clear_offers(offers: List[Offer]) -> List[Offer]:
    """
    Change list of offers: \n removes empty symbols
    """
    DISALLOWED_SYMBOLS = ["\n", "\t"]

    for offer in offers:
        for _, v in offer.items():
            if isinstance(v, str): offer[_] = clear_string(v, DISALLOWED_SYMBOLS).strip()

def extract_offers_data(offers: List[Tag]) -> Generator[Offer]:
    for el in offers:
        offer = Offer(
            **{k:extractor.extract(el) for k, extractor in _extractors.items()}    
        )
        yield offer

def extract(html: str) -> List[Offer]:
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("li", attrs={"class":"ad-listitem"})    
    offers = [offer for offer in extract_offers_data(items)]
    clear_offers(offers)
    return offers