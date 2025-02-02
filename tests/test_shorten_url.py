from app.utils.bitly_utils import shorten_url


def test_shorten_url():
    url = "https://www.amazon.co.jp/b?node=203879213051"
    shortened_url = shorten_url(url)
    assert shortened_url.startswith("https://amzn.to/")
