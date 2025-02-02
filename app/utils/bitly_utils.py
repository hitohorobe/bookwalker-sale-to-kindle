import os
import requests


BITLY_API_URL = "https://api-ssl.bitly.com/v4/shorten"
BITLY_TOKEN = os.environ["BITLY_API_TOKEN"]


def shorten_url(url: str) -> str:
    """
    URLを短縮する
    """
    headers = {
        "Authorization": f"Bearer {BITLY_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "long_url": url,
    }
    # amazonのURLはamzn.toに短縮したい
    response = requests.post(BITLY_API_URL, headers=headers, json=data)

    # 200番台以外の場合はエラーを出力する
    if int(response.status_code) // 100 != 2:
        raise Exception(f"Error: {response.status_code} {response.text}")

    return response.json()["link"]


def make_url_list(asin_list: list) -> list:
    """
    asin 120件ごとに検索結果URLをつくり、URLのリストを返す
    """
    base_url = "https://www.amazon.co.jp/s?i=digital-text&hidden-keywords="
    url_list = []
    for i, asin in enumerate(asin_list):
        if asin:
            if i % 120 == 0:
                # 末尾にアソシエイトタグを付与する
                amazon_tag = os.environ["AMAZON_TAG"]
                tag = f"&tag={amazon_tag}"
                base_url += tag
                url_list.append(base_url)
            url_list[-1] += asin + "|"
    return url_list
