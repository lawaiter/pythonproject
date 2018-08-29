# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
#   程序：TestCommentAnalyze.py
#   版本：0.1
#   作者：lawaiter
#   日期：编写日期20180512
#   语言：Python 3.6
#   功能：从mysql中读取评论内容和评论时间，进行评论数据信息挖掘处理，主要是绘制词云和统计情感分析数值
# -------------------------------------------------------------------------
import time
import MySQLdb
from random import randint
import re
import csv
import numpy as np
from snownlp import SnowNLP
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
import jieba.posseg as psg

# 从数据库中获取特定型号的手机评论数据,并且将器械如CSV文件，备用
"""
data = []
f = open("mix2s.csv", "w", encoding='utf-8-sig')
wr = csv.writer(f)
conn = MySQLdb.connect("127.0.0.1", "root", "tentan", "jindongphoneurls", charset="utf8", use_unicode=True)
cur = conn.cursor()
query = " select * from phonecomments where phone_name like("%MIX2S%") or phone_name like("%Mix2s%") or phone_name like
("%mix2s%") or phone_name like("%Mix 2s%") or phone_name like("%MIX 2S%")"
cur.execute(query)
res = cur.fetchall()
for row in res:
    star = row[2]
    comment = row[3]
    time = row[4]
    # print([star, comment, time])
    wr.writerow(star, comment, time)
"""



# 从数据库中取出相应的手机评论进行分析
# 利用snownlp进行分析
"""
sum = 0
count = 0
com = ""
conn = MySQLdb.connect("127.0.0.1", "root", "tentan", "jindongphoneurls", charset="utf8", use_unicode=True)
cur = conn.cursor()
query = "select * from phonecomments where phone_name like('%MIX2S%') or phone_name like('%Mix2s%') or phone_name " \
        "like('%mix2s%') or phone_name like('%Mix 2s%') or phone_name like('%MIX 2S%')"
cur.execute(query)
res = cur.fetchall()
for row in res:
    count = count + 1
    comment = row[3]
    time = row[4]  # 可以统计评论的时间段，七天一个周期，使用pycharts绘制出直方图
    star = row[2]  # 可以计算该型手机的评论星星数
    com += comment
    print(comment)
    # 进行关键词抽取 s = SnowNLP(comment)  print(s.keywords(limit=20))
    # 在该手机店购买该型号手机的情感分析 sum += s.sentiments print(s.sentiments)
a = SnowNLP(com)
# 计算关键词 print(a.keywords(limit=20))
# 在该手机店购买该型号手机的综合情感分析数值 print(float(sum/count))


# 描绘出该型手机评论词云
# 使用全模式进行分词 b = ','.join(jieba.cut(com, cut_all=True))
li = [x.word for x in psg.cut(com) if x.flag.startswith('n') or x.flag.startswith('v') or x.flag.startswith("a")]
b = ",".join('%s' % id for id in li)
print(b)
font_path = "C:\\Users\\pro2\\Desktop\\msyh.ttc"
my_word = WordCloud(font_path=font_path,max_words=400,random_state=42,width=3840,height=2560,margin=1).generate(b)
plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
plt.imshow(my_word)
plt.axis("off")
# 电脑上没有可以打开SVG的工具 plt.savefig('C:\\Users\\pro2\\Desktop\\words.svg',format='svg')
plt.show()
"""


# 下面市调用百度云开发平台进行分词和情感分析的例子
import urllib.request, sys, requests
import json


# s首先获取access_token，备用
# client_id 为官网获取的AK， client_secret 为官网获取的SK
"""
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=B8UkeXdysqcAUN8U6fiFqhKM&client_secret=YSBqpzBsjpP5eSbizIXWWGUqED1Iy8ZR'
request = urllib.request.Request(host)
request.add_header('Content-Type', 'application/json; charset=UTF-8')
content = json.loads(urllib.request.urlopen(request).read().decode(encoding="utf-8"))
if (content):
    access_token  = content["access_token"]
    print(access_token)
"""

# 调用百度词法分析接口，对评论进行词法分析, 初步试验的结果好于jieba分词的效果
"""
from aip import AipNlp

# 你的 APPID AK SK
APP_ID = '11234179'
API_KEY = 'B8UkeXdysqcAUN8U6fiFqhKM'
SECRET_KEY = 'YSBqpzBsjpP5eSbizIXWWGUqED1Iy8ZR'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


relist = []
count = 0
com = ""
conn = MySQLdb.connect("127.0.0.1", "root", "tentan", "jindongphoneurls", charset="utf8", use_unicode=True)
cur = conn.cursor()
query = "select * from phonecomments where phone_name like('%MIX2S%') or phone_name like('%Mix2s%') or phone_name " \
        "like('%mix2s%') or phone_name like('%Mix 2s%') or phone_name like('%MIX 2S%')"
cur.execute(query)
res = cur.fetchall()
for row in res:
    count += 1
    comment = row[3]
    try:
        if count <= 100000:
            a = client.lexer(str(comment))
            for i in a["items"]:
                if i["pos"] == "n" or i["pos"] == "a" or i["pos"] == "an" or i["ne"] == "ORG":
                    relist.append(i["item"])
                    print(count)
        else:
            break
        print(relist)
    except:
        pass
b = ",".join('%s' % id for id in relist)
font_path = "C:\\Users\\pro2\\Desktop\\msyh.ttc"
my_word = WordCloud(font_path=font_path,max_words=200,random_state=42,width=2560,height=1440,margin=1).generate(b)
plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
plt.imshow(my_word)
plt.axis("off")
plt.show()
"""

# 这是使用百度情感倾向分析接口，进行商品评论情感倾向的分析
"""
from aip import AipNlp

# 你的 APPID AK SK
APP_ID = '11234179'
API_KEY = 'B8UkeXdysqcAUN8U6fiFqhKM'
SECRET_KEY = 'YSBqpzBsjpP5eSbizIXWWGUqED1Iy8ZR'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


relist = []
count = 0
com = ""
conn = MySQLdb.connect("127.0.0.1", "root", "tentan", "jindongphoneurls", charset="utf8", use_unicode=True)
cur = conn.cursor()
query = "select * from phonecomments where phone_name like('%MIX2S%') or phone_name like('%Mix2s%') or phone_name " \
        "like('%mix2s%') or phone_name like('%Mix 2s%') or phone_name like('%MIX 2S%')"
cur.execute(query)
res = cur.fetchall()
zero = 0
first = 0
second = 0
for row in res:
    comment = row[3]
    try:
        if count <= 100:
        # 调用情感分析接口进行情感分析
            a = client.sentimentClassify(comment)
            for i in a["items"]:
                print(type(i["sentiment"]))
                if i["sentiment"] == 2:
                    second += 1
                    print(second, count)
                elif i["sentiment"] == 1:
                    first += 1
                    print(first, count)
                elif i["sentiment"] == 0:
                    zero += 1
                    print(zero, count)
                else:
                    print("NO,score")
        else:
            break
        count += 1
    except:
        pass
print(zero, first, second)
print(float(zero/count), float(first/count), float(second/count))
"""

# 这是使用百度评论观点抽取，进行收集数据分析的例子
"""
from aip import AipNlp

# 你的 APPID AK SK
APP_ID = '11234179'
API_KEY = 'B8UkeXdysqcAUN8U6fiFqhKM'
SECRET_KEY = 'YSBqpzBsjpP5eSbizIXWWGUqED1Iy8ZR'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


result = []
count = 0
conn = MySQLdb.connect("127.0.0.1", "root", "tentan", "jindongphoneurls", charset="utf8", use_unicode=True)
cur = conn.cursor()
query = "select * from phonecomments where phone_name like('%MIX2S%') or phone_name like('%Mix2s%') or phone_name " \
        "like('%mix2s%') or phone_name like('%Mix 2s%') or phone_name like('%MIX 2S%')"
cur.execute(query)
res = cur.fetchall()
# 如果有可选参数
options = {}
options["type"] = 13
for row in res:
    comment = row[3]
    try:
        # 带参数调用评论观点抽取 """
"""
        a = client.commentTag(comment, options)
        if count <= 100:
            for i in a["items"]:
                result.append(i["prop"] + i["adj"])
        else:
            break
    except:
        pass
b = ",".join('%s' % id for id in result)
font_path = "C:\\Users\\pro2\\Desktop\\msyh.ttc"
my_word = WordCloud(font_path=font_path,max_words=200,random_state=42,width=2560,height=1440,margin=1).generate(b)
plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
plt.imshow(my_word)
plt.axis("off")
plt.show()
"""

