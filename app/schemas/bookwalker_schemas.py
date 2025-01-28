from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class BookwalkerItemSchema(BaseModel):
    title: str = Field(..., title="書籍タイトル")
    url: str = Field(..., title="書籍URL")
    author: List[str] = Field(..., title="著者")
    company: str = Field(..., title="出版社")
    price: int = Field(..., title="価格")
    label: Optional[str] = Field(title="レーベル", default=[None])


class BookwalkerCampaignSchema(BaseModel):
    title: str = Field(..., title="キャンペーンタイトル")
    url: str = Field(..., title="キャンペーンURL")
    items: List[BookwalkerItemSchema] = Field(..., title="商品情報")
    period: Optional[datetime] = Field(title="キャンペーン期間", default=[None])
