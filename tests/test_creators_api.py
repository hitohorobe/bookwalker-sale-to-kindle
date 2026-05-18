from app.utils.creator_api_utils import AmazonApiUtils


def test_search_items():
    amazon = AmazonApiUtils()
    keywords = " きもちわるいから君がすき　３巻 まんがタイムKRコミックス"
    response = amazon.search_items(keywords)
    assert response is not None
    assert response["items"][0].asin
    assert response["items"][0].offers_v2.listings[0].price.money.amount
    assert response["items"][0].item_info.title.display_value
    assert response["items"][0].detail_page_url
