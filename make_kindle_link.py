import argparse
import time
from dotenv import load_dotenv
from app.utils.scraping_utils import BookwalkerScraping
from app.utils.paapi_utils import AmazonPaapi
from app.utils.bitly_utils import shorten_url, make_url_list


load_dotenv()


def main():
    amazon = AmazonPaapi()

    parser = argparse.ArgumentParser(
        description="Get Kindle link from Bookwalker campaign URL"
    )
    parser.add_argument("url", help="Bookwalker campaign URL")
    # BookwalkerのURLを引数にとる。引数がない場合はエラーを出力する
    args = parser.parse_args()
    url = args.url
    if not url:
        print("Please input Bookwalker campaign URL")
    # BookwalkerのURLが正しいかどうかを判定する
    if not BookwalkerScraping.is_valid_url(url):
        print("Invalid URL")
        return
    # URLを正規化する
    url = BookwalkerScraping.regularize_url(url)
    # ページを取得する
    response = BookwalkerScraping.get_page(url)
    # キャンペーンのページが何ページあるか取得する
    page_length = BookwalkerScraping.get_page_length(response)

    # 結果のasinを格納するリスト
    asins = []
    # キャンペーンページの商品情報を取得して一覧で返す
    campaign = BookwalkerScraping.get_campaign_items(url)
    items = campaign.items
    for item in items:
        # 商品情報を出力する
        # print(item)
        # 商品情報をAmazonで検索する。検索は商品名+レーベル+出版社名で行う
        keywords = f"{item.title} {item.company}"
        try:
            if item.label:
                keywords += f" {item.label}"
            response = amazon.search_items(keywords=keywords)
            # asinをリストに追加する
            asins.append(response["_items"][0].asin)
            print(item.title + " を取得... asin:" + response["_items"][0].asin)
        except Exception as e:
            print(f"Error: {e}")
        # 1秒待機する
        time.sleep(1)
    # asin 120件ごとに区切り、短縮URLを取得する
    # urlの形式は https://www.amazon.co.jp/s?i=digital-text&hidden-keywords=asin1|asin2|asin3...
    print(asins)
    url_list = make_url_list(asins)
    for url in url_list:
        print(shorten_url(url))


if __name__ == "__main__":
    main()
