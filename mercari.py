import csv
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd
import re



with open("brand_sarch_list.csv", encoding="utf-8-sig") as f:

        # 検索ワード格納用の空リストを準備
    csv_lists = []
        # csvファイルの何行目を読み込むかを確認するためのカウンター
    counter = 0

        # csvファイルを1行ずつ読み込む
    reader = csv.reader(f)
    for row in reader:
        counter += 1
        csv_lists.append(row)
        try:
                # 検索ワードチェック
                # 空の場合、エラーメッセージを表示して終了する
            if(len(row[0]) == 0):
                print("File Error: 検索ワードがありません-> " +
                          "mercari_search.csv " + str(counter) + "行目")
                break
        except IndexError:
                # 行が空いている場合、エラーメッセージを表示して終了する
            print("File Error: CSVファイルに問題があります。行間を詰めるなどしてください。")
            break

print(csv_lists)


def search_mercari(search_words):

    url = "https://www.mercari.com/jp/search/?keyword=" + search_words + "&category_root=&brand_name=&brand_id=&size_group=&price_min=1000&price_max=&item_condition_id%5B1%5D=1&item_condition_id%5B2%5D=1&item_condition_id%5B3%5D=1&item_condition_id%5B4%5D=1&status_on_sale=1"
    ua= UserAgent()
    useragent = ua.random
    header = {'User-Agent': str(ua.chrome)}
    res = requests.get(url, headers=header)
    soup = BeautifulSoup(res.content, 'html.parser')
    time.sleep(3)
    browser = webdriver.Chrome()
    page = 1
    columns = ["title", "url", "price"]
    df = pd.DataFrame(columns=columns)
    # 配列名を指定する
    try:
        while(True):
            # ブラウザで検索
            browser.get(url)
            # 商品ごとのHTMLを全取得
            soup = BeautifulSoup(res.content, 'html.parser')
            items = soup.find_all(class_="items-box")
            # 何ページ目を取得しているか表示
            print(str(page) + "ページ取得中")
            # 次のページに進むためのURL
            for item in items:
                title = item.find(class_="items-box-name font-2").text
                url = "https://www.mercari.com" + item.find("a").get("href")
                price = item.find(class_="items-box-price font-5").text
                se = pd.Series([title, url, price], columns)
                df = df.append(se, columns)
            page += 1
            url = browser.find_element_by_css_selector("li.pager-next .pager-cell a").get_attribute("href")
            print("Moving to next page ...")
            

    except:
        print("Next page is nothing.")

        # 得たデータをCSVにして保存

        df.to_csv(search_words+".csv", encoding='utf_8_sig')
    print("Finish!")


for i in range(len(csv_lists)):
    search_mercari(csv_lists[i][0])