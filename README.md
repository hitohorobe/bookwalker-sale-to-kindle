# bookwalker-sale-to-kindle
- Bookwalker のセールのページから商品一覧を取得し、Kindle版のセール対象書籍一覧ページのURLを組立てて返すツール

## 構成
- CLIツール
- API(未実装)
- クローラー(未実装)

## 使い方
### 準備
以下のものを事前に取得しておく
- Amazon アソシエイトのアソシエイトタグ(例: hito-horobe-22)
- Amazon PAAPI のアクセスキー
- Amazon PAAPI のシークレット
- Amazon の国別コード（例：JP）
- bit.lyのアクセストークン

### CLIツール
- `cp .env.example .env`
- `.env`ファイルに環境変数を貼り付け
- `poetry install`
- `poetry shell`
- `python make_kindle_link.py <bookwalkerのセールのページのURL>`
コンソールに短縮URLが出力される
