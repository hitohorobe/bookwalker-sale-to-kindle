import pytest
from pathlib import Path
from requests.models import Response

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def make_response(html: str, status: int = 200, url: str = "") -> Response:
    r = Response()
    r.status_code = status
    r._content = html.encode("utf-8")
    r.encoding = "utf-8"
    r.url = url
    return r


@pytest.fixture
def campaign_48572_response():
    html = (FIXTURES_DIR / "campaign_48572_page1.html").read_text(encoding="utf-8")
    return make_response(
        html, url="https://bookwalker.jp/campaign/48572/?detail=1&page=1"
    )
