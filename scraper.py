# -*- coding: utf-8 -*-
"""
第一个爬虫：抓取 books.toscrape.com 的书名 / 价格 / 评分 / 库存，保存成 CSV。

一个静态页面爬虫的最小完整流程：
    发请求 -> 拿到 HTML -> 解析提取字段 -> 保存数据

运行方式（在该目录下打开终端）：
    python scraper.py

注意：books.toscrape.com 是专门给爬虫练习用的网站，随便抓，不用担心法律问题。
"""

import csv
import sys

import requests
from bs4 import BeautifulSoup

# Windows 控制台默认是 GBK 编码，打印 £ 这类字符会报 UnicodeEncodeError。
# 这一行把标准输出强制改成 UTF-8，问题就没了。
sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "https://books.toscrape.com/"
TIMEOUT = 15

# 带上 User-Agent，让请求看起来像正常浏览器发的
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
}


def fetch_page(url: str) -> str:
    """发 HTTP 请求，返回网页的 HTML 文本。"""
    resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()      # 状态码不是 200 就直接抛异常，别带着错误往下跑
    resp.encoding = "utf-8"      # 手动指定编码，防止特殊符号乱码
    return resp.text


def parse_books(html: str) -> list[dict]:
    """从 HTML 里提取每一本书的信息。"""
    soup = BeautifulSoup(html, "lxml")
    books = []

    # select 用的是 CSS 选择器，和你在浏览器 F12 里看到的一模一样
    for item in soup.select("article.product_pod"):
        books.append({
            "title": item.h3.a["title"],                                    # 书名（在 a 标签的 title 属性里）
            "price": item.select_one("p.price_color").get_text(strip=True),  # 价格
            "rating": item.select_one("p.star-rating")["class"][1],          # 评分（在 class 的第二个值里）
            "in_stock": item.select_one("p.instock.availability").get_text(strip=True),
        })

    return books


def save_csv(rows: list[dict], filename: str = "books.csv") -> None:
    """把数据写成 CSV 文件。"""
    if not rows:
        print("没抓到数据，跳过保存。")
        return

    # utf-8-sig 会带上 BOM，这样中文 Excel 打开不会乱码
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"已保存 {len(rows)} 条数据到 {filename}")


def main() -> None:
    html = fetch_page(BASE_URL)       # 1. 拿页面
    books = parse_books(html)         # 2. 解析字段

    for b in books[:5]:               # 3. 先打印前 5 条看看
        print(f"{b['title'][:40]:<42} {b['price']:>8}  {b['rating']}")

    save_csv(books)                   # 4. 存盘


if __name__ == "__main__":
    main()