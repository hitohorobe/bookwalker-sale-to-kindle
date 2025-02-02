from app.utils.paapi_utils import AmazonPaapi


def test_search_items():
    amazon = AmazonPaapi()
    keywords = " きもちわるいから君がすき　３巻 まんがタイムKRコミックス"
    response = amazon.search_items(keywords)
    assert response is not None
    assert response["_items"][0].asin
    assert response["_items"][0].offers.listings[0].price.amount
    assert response["_items"][0].item_info.title.display_value
    assert response["_items"][0].detail_page_url
