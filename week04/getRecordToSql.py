import requests
from pathlib import *
import sys
from lxml import etree
import pymysql

# PEP-8
# Google Python 风格指引

rating_map = {"力荐": 5, "推荐": 4, "还行": 3, "较差": 2, "很差": 1}
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
header = {'user-agent': ua}


class Error(Exception):
    pass


class InDBFailed(Error):
    pass


def getCommentRating(selectorm):

    film_content = [i.text for i in selector.xpath(
        '//div[@class="comment"]//span[@class="short"]')]
    rating_word = selector.xpath(
        '//div[@class="comment"]//span[@class="comment-info"]//span[contains(@class, "rating")]/@title')
    rating_num = [rating_map[i] for i in rating_word]

    return [i for i in zip(film_content, rating_num)]


myurl = ['https://movie.douban.com/subject/34894753/comments?percent_type=h&limit=20&status=P&sort=new_score',
         'https://movie.douban.com/subject/34894753/comments?percent_type=m&limit=20&status=P&sort=new_score'
         ]

conn = pymysql.connect(host="localhost", user="root",
                       password="Geekbang123", database="db1")
cursor = conn.cursor()
try:
    result = []
    for i in myurl:
        response = requests.get(i, headers=header)
        selector = etree.HTML(response.text)
        result.extend(getCommentRating(selector))

except requests.exceptions.ConnectTimeout as e:
    print(f"requests库超时")
    sys.exit(1)
try:
    for i in result:
        sql = "insert into movieratingcomment(short, n_star) values('%s',%d)" % i
        cursor.execute(sql)
        conn.commit()
except InDBFailed:
    conn.rollback()
    print("fail insert into db, rolling back")
