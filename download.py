from flickrapi import FlickrAPI
from urllib.request import urlretrieve
import os, time, sys

# API キーの情報

key = "dc823d33459cdb76a9f4bb63f5a9b648"
secret = "691c6ea03ea6d083"

# 重要：リクエストを送るタイミングが短すぎると画像取得先のサーバを逼迫してしまうか、
# スパムとみなされてしまう可能性があるので、待ち時間を 1 秒間設ける。
wait_time = 1

# コマンドライン引数の 1 番目の値を取得
keyword = sys.argv[1]
# 画像を保存するディレクトリを指定
savedir = "./" + keyword

# FlickrAPI にアクセス

# FlickrAPI(キー、シークレット、データフォーマット{json で受け取る})
flickr = FlickrAPI(key, secret , format='parsed-json')
result = flickr.photos.search(
    text = keyword,
    # 取得するデータ件数
    per_page = 400,
    # 取得するデータ件数
    media = 'photos',
    # データの並び順(関連順)
    sort = 'relevance',
    # UI コンテンツを表示しない
    safe_search = 1,
    # 取得したいオプションの値(url_q->画像のアドレスが入っている情報、licence -> ライセンス情報)
    extras = 'url_q, license'
)

# 結果を表示
photos = result['photos']

for i, photo in enumerate(photos['photo']):
    url_q = photo['url_q']
    filepath = savedir + '/' + photo['id'] + '.jpg'
    # ファイルが重複していたらスキップする
    if os.path.exists(filepath): continue
    # データをダウンロードする
    urlretrieve(url_q, filepath)
    # 重要：サーバを逼迫しないように 1 秒待つ
    time.sleep(wait_time)