import os
import json
from dotenv import load_dotenv
from amazon_paapi import AmazonApi

load_dotenv()


KEY = os.environ["AMAZON_API_KEY"]
SECRET = os.environ["AMAZON_API_SECRET"]
TAG = os.environ["AMAZON_TAG"]
COUNTRY = os.environ["AMAZON_COUNTRY"]

KINDLE_BROWSE_NODE_ID = "2250738051"


class AmazonPaapi:
    def __init__(self):
        self.api = AmazonApi(KEY, SECRET, TAG, COUNTRY)

    def search_items(self, keywords: str, item_count: int = 10):
        response = self.api.search_items(
            item_count=item_count,
            keywords=keywords,
            browse_node_id=KINDLE_BROWSE_NODE_ID,
        )
        # レスポンスを辞書型に変換
        respose_json = response.__dict__
        return respose_json
