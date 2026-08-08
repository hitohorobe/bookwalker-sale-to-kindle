from unittest.mock import patch

from creatorsapi_python_sdk.models.item import Item
from creatorsapi_python_sdk.models.item_info import ItemInfo
from creatorsapi_python_sdk.models.money import Money
from creatorsapi_python_sdk.models.offer_listing_v2 import OfferListingV2
from creatorsapi_python_sdk.models.offer_price_v2 import OfferPriceV2
from creatorsapi_python_sdk.models.offers_v2 import OffersV2
from creatorsapi_python_sdk.models.search_result import SearchResult
from creatorsapi_python_sdk.models.single_string_valued_attribute import (
    SingleStringValuedAttribute,
)

from app.utils.creator_api_utils import AmazonApiUtils

FAKE_SEARCH_RESULT = SearchResult(
    items=[
        Item(
            asin="B0DUMMYASIN",
            detail_page_url="https://www.amazon.co.jp/dp/B0DUMMYASIN",
            item_info=ItemInfo(
                title=SingleStringValuedAttribute(
                    display_value="きもちわるいから君がすき 3巻 まんがタイムKRコミックス"
                )
            ),
            offers_v2=OffersV2(
                listings=[
                    OfferListingV2(price=OfferPriceV2(money=Money(amount=550, currency="JPY")))
                ]
            ),
        )
    ]
)


def test_search_items():
    with patch("app.utils.creator_api_utils.AmazonCreatorsApi") as mock_api_cls:
        mock_api_cls.return_value.search_items.return_value = FAKE_SEARCH_RESULT
        amazon = AmazonApiUtils()
        keywords = " きもちわるいから君がすき　３巻 まんがタイムKRコミックス"
        response = amazon.search_items(keywords)

    assert response is not None
    assert response["items"][0].asin
    assert response["items"][0].offers_v2.listings[0].price.money.amount
    assert response["items"][0].item_info.title.display_value
    assert response["items"][0].detail_page_url
