import os
import re
from datetime import datetime
from logging import getLogger
from typing import Optional

import requests
from requests import Response
from bs4 import BeautifulSoup, element, Tag

from app.schemas.bookwalker_schemas import (
    BookwalkerItemSchema,
    BookwalkerCampaignSchema,
)


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
BOOKWALKER_CAMPAIGN_URL = "https://bookwalker.jp/campaign/"
TIMEOUT = 10

# 商品名に含まれていたら無視するキーワード一覧
IGNORE_KEYWORDS = ["分冊版", "試し読み", "無料", "お試し", "期間限定"]

logger = getLogger(__name__)


class BookwalkerScraping:
    """
    bookwalkerのキャンペーンページをスクレイピングするクラス
    - is_valid_url: URLが正しいかどうかを判定する
    - regularize_url: URLを正規化する
    - get_page: URLからページを取得する
    - get_page_length: キャンペーンのページが何ページあるか取得する
    - get_campaign_items: キャンペーンページの商品情報を取得して一覧で返す

    *ページ取得回数を削減するため、requestsを使って取得したレスポンスを引数に取るようにしている
    """

    def __init__(self) -> None:
        pass

    @classmethod
    def is_valid_url(cls, url: str) -> bool:
        """
        入力されたURLがBOOKWALKER_CAMPAIGN_URL以下のURLかどうかを判定する
        """
        is_str = isinstance(url, str)
        if not is_str:
            return False

        url = re.sub(r"\?.*", "", url)
        if not url.endswith("/"):
            url += "/"

        is_valid_domain = re.match(r"https://bookwalker.jp/.+?/[0-9]+/$", url)
        if not is_valid_domain:
            logger.error(f"Invalid URL: {url}")
            return False
        return True

    @classmethod
    def regularize_url(cls, url: str) -> str:
        """
        URLを正規化する
        - ドメイン検証
        - クエリパラメータ削除
        - 末尾に"?detail=1"を付与する
        """
        if not cls.is_valid_url(url):
            return ""
        url = re.sub(r"\?.*", "", url)
        if not url.endswith("/"):
            url += "/"
        url += "?detail=1"
        return url

    @classmethod
    def get_page(cls, url: str) -> Optional[Response]:
        """
        URLからページの中身を取得する
        """
        headers = {"User-Agent": USER_AGENT}
        try:
            response = requests.get(url, headers=headers, timeout=TIMEOUT)
            if response.status_code != 200:
                logger.error(f"Error: {response.status_code}")
                return None
            return response
        except TimeoutError as e:
            logger.error(f"TimeoutError: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error: {e}")
            return None

    @classmethod
    def get_page_length(cls, response: Response) -> int:
        """
        キャンペーンのページが何ページあるか取得する
        """
        is_valid_response = isinstance(response, Response)
        if not is_valid_response:
            return 0

        if response.status_code != 200:
            return 0
        soup = BeautifulSoup(response.text, "html.parser")
        pagination_buttons = soup.find_all(
            "a", attrs={"data-ga-category": "ページネーション"}
        )
        if len(pagination_buttons) == 0:
            return 1
        page_numbers = [
            int(button.text)
            for button in pagination_buttons
            if isinstance(button, Tag)
            and button.text is not None
            and button.text.isdigit()
        ]
        return max(page_numbers)

    @classmethod
    def get_campaign_items(cls, url: str) -> Optional[BookwalkerCampaignSchema]:
        """
        キャンペーンページの商品情報を取得して一覧で返す
        """
        is_valid_url = cls.is_valid_url(url)
        if not is_valid_url:
            return None

        url = cls.regularize_url(url)
        if not url:
            return None

        page = cls.get_page_length(cls.get_page(url))
        campaign_items = []
        periods = []

        for i in range(1, page + 1):
            response = cls.get_page(f"{url}&page={i}")
            if response is None:
                return None

            soup = BeautifulSoup(response.text, "html.parser")
            campaign_title_tag = soup.find("h2", class_="o-contents-section__title")
            if campaign_title_tag is None:
                return None
            campaign_title = campaign_title_tag.text
            campaign_item_cards = soup.find_all("li", class_="m-list-card")
            for campaign_item_card in campaign_item_cards:
                if not isinstance(campaign_item_card, Tag):
                    continue
                item_title_tag = campaign_item_card.find(
                    "span", class_="o-card-ttl__text"
                )
                if item_title_tag is None:
                    continue
                item_title = item_title_tag.text.strip()
                item_author_elements = campaign_item_card.find_all(
                    "dd", class_="a-card-author"
                )
                item_authors = [
                    author.text
                    for author in item_author_elements
                    if isinstance(author, Tag)
                ]
                item_company_element = campaign_item_card.find(
                    "div", class_="a-card-publisher"
                )
                item_company = (
                    item_company_element.find("a").text
                    if isinstance(item_company_element, Tag)
                    else ""
                )
                item_company = item_company.strip() if item_company else ""
                item_url_element = campaign_item_card.find("h2", class_="o-card-ttl")
                item_url = (
                    item_url_element.find("a").get("href") if item_url_element else ""
                )

                item_price = int(
                    campaign_item_card.find(
                        "span", class_="m-book-item__price-num"
                    ).text.replace(",", "")
                )
                item_label_element = campaign_item_card.find(
                    "div", class_="a-card-book-label"
                )
                item_label = (
                    item_label_element.find("a").text
                    if isinstance(item_label_element, Tag)
                    else ""
                )
                item_label = item_label.strip() if item_label else ""
                period_wrap = campaign_item_card.find("span", class_="a-card-period")
                if period_wrap is not None:
                    period_text = period_wrap.text
                    # YYYY/M/Dの部分だけを正規表現で抜粋
                    period_pattern = re.match(
                        r".*([0-9]{4}/[0-9]{1,2}/[0-9]{1,2}).*", period_text
                    )
                    if period_pattern is not None:
                        period = datetime.strptime(period_pattern.group(1), "%Y/%m/%d")
                        periods.append(period)

                # 商品名に含まれていたら無視するキーワードがあればスキップ
                if any(keyword in item_title for keyword in IGNORE_KEYWORDS):
                    continue
                bookwalker_item = BookwalkerItemSchema(
                    title=item_title,
                    url=item_url,
                    author=item_authors,
                    company=item_company,
                    label=item_label,
                    price=item_price,
                )
                campaign_items.append(bookwalker_item)

        if len(campaign_items) == 0:
            print("No items found.")
            return None

        if len(periods) > 0:
            period = min(periods)

            campaign = BookwalkerCampaignSchema(
                title=campaign_title,
                url=response.url,
                items=campaign_items,
                period=period,
            )
            print(campaign)
            return campaign
        else:
            campaign = BookwalkerCampaignSchema(
                title=campaign_title, url=response.url, items=campaign_items
            )
            print(campaign)

            return campaign
