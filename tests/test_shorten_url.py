import json
from unittest.mock import patch

from app.utils.bitly_utils import shorten_url
from tests.conftest import make_response


def test_shorten_url():
    url = "https://www.amazon.co.jp/b?node=203879213051"
    fake_response = make_response(
        json.dumps({"link": "https://amzn.to/dummy1234"}), status=200
    )

    with patch("app.utils.bitly_utils.requests.post", return_value=fake_response):
        shortened_url = shorten_url(url)

    assert shortened_url.startswith("https://amzn.to/")
