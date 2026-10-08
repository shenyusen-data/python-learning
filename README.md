# python-learning

我的 Python / 爬虫学习记录。每学一个知识点就提交一次，慢慢攒成作品集。

## 环境

- Python 3.14.4
- requests / beautifulsoup4 / lxml

## 安装依赖

```bash
pip install -r requirements.txt
```

## 目录说明

| 文件 | 说明 |
| --- | --- |
| `scraper.py` | 第一个爬虫：抓取书籍信息并保存为 CSV |
| `books.csv` | 抓取结果（运行 scraper.py 后生成） |
| `requirements.txt` | 项目依赖 |

## 运行

```bash
python scraper.py
```

数据来源：[books.toscrape.com](https://books.toscrape.com/)（官方爬虫练习站）