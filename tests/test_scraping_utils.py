from unittest.mock import patch

from app.utils.scraping_utils import BookwalkerScraping

CAMPAIGN_URL = "https://bookwalker.jp/campaign/48572/"


def test_is_valid_url():
    assert BookwalkerScraping.is_valid_url("https://bookwalker.jp/campaign/39129/") == True
    assert BookwalkerScraping.is_valid_url("https://bookwalker.jp/select/3443/") == True
    assert BookwalkerScraping.is_valid_url("https://example.com/campaign/39129/") == False


def test_regularize_url():
    url = "https://bookwalker.jp/campaign/39123/?detail=0&page=2"
    assert (
        BookwalkerScraping.regularize_url(url)
        == "https://bookwalker.jp/campaign/39123/?detail=1"
    )


def test_get_page(campaign_48572_response):
    with patch("app.utils.scraping_utils.requests.get", return_value=campaign_48572_response):
        response = BookwalkerScraping.get_page(CAMPAIGN_URL)
        assert response.status_code == 200


def test_get_page_length(campaign_48572_response):
    assert BookwalkerScraping.get_page_length(campaign_48572_response) == 1


def test_get_campaign_items(campaign_48572_response):
    with patch("app.utils.scraping_utils.requests.get", return_value=campaign_48572_response):
        items = BookwalkerScraping.get_campaign_items(CAMPAIGN_URL)
        assert items is not None
        assert len(items.items) > 0
