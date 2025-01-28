from app.utils.scraping_utils import BookwalkerScraping


def test_is_valid_url():
    valid_url = "https://bookwalker.jp/campaign/39129/"
    assert BookwalkerScraping.is_valid_url(valid_url) == True

    invalid_url = "https://bookwalker.jp/select/3443/"
    assert BookwalkerScraping.is_valid_url(invalid_url) == False


def test_regularize_url():
    url = "https://bookwalker.jp/campaign/39123/?detail=0&page=2"
    assert (
        BookwalkerScraping.regularize_url(url)
        == "https://bookwalker.jp/campaign/39123/?detail=1"
    )


def test_get_page():
    url = "https://bookwalker.jp/campaign/39129/"
    response = BookwalkerScraping.get_page(url)
    assert response.status_code == 200


def test_get_page_length():
    single_page_url = "https://bookwalker.jp/campaign/39129/"
    response = BookwalkerScraping.get_page(single_page_url)
    assert BookwalkerScraping.get_page_length(response) == 1

    multi_page_url = "https://bookwalker.jp/campaign/39123/"
    response = BookwalkerScraping.get_page(multi_page_url)
    assert BookwalkerScraping.get_page_length(response) == 2


def test_get_campaign_items():
    campaign_url = "https://bookwalker.jp/campaign/39129/"
    items = BookwalkerScraping.get_campaign_items(campaign_url)
    assert items is not None
