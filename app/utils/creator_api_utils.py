import json
import os

from amazon_creatorsapi import AmazonCreatorsApi, Country
from dotenv import load_dotenv

load_dotenv()


ID = os.environ["AMAZON_CREATOR_API_ID"]
SECRET = os.environ["AMAZON_CREATOR_API_SECRET"]
VERSION = os.environ["AMAZON_CREATOR_API_VERSION"]
TAG = os.environ["AMAZON_TAG"]
COUNTRY = Country.JP

KINDLE_BROWSE_NODE_ID = "2250738051"


class AmazonApiUtils:
    def __init__(self):
        self.api = AmazonCreatorsApi(
            credential_id=ID,
            credential_secret=SECRET,
            version=VERSION,
            tag=TAG,
            country=COUNTRY,
        )

    def search_items(self, keywords: str, item_count: int = 10):
        response = self.api.search_items(
            item_count=item_count,
            keywords=keywords,
            browse_node_id=KINDLE_BROWSE_NODE_ID,
        )
        # レスポンスを辞書型に変換
        response_json = response.__dict__
        return response_json
