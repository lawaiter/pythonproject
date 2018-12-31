# -*- coding: utf-8 -*-
# # -------------------------------------------------------------------------
# #   程序：TasobaoSavePhoneUrls.py
# #   版本：0.1
# #   作者：lawaiter
# #   日期：编写日期20181030
# #   语言：Python 3.6
# #   功能：从数据库中读取手机类型，然后在淘宝上找对对应的网店，然后将网店的url存入数据库备用
# #        目前是使用selenium进行爬取。
# # -------------------------------------------------------------------------
# # -------------------------------------------------------------------------
# #   程序：TasobaoSavePhoneUrls.py
# #   版本：0.1.1
# #   作者：lawaiter
# #   日期：编写日期20181223
# #   语言：Python 3.6
# #   功能：取消原来使用cooikes获取的方式，改用pyppteer,
# #        另外经过分析，淘宝反爬措施简直变态，测试后发现天猫可以爬取，将爬取目标改为天猫
# # -------------------------------------------------------------------------

import pymysql
import asyncio
import pyppeteer
from pyppeteer import launch
import requests


from mobliephone.tools.GetEveryPhoneType import get_xiaomi_phone_list, get_meizu_phone_list, get_huawei_phone_list


get_other_phone_list = []


# TODO 下步添加如何判断手机类型的方法
phone_name = get_xiaomi_phone_list() + get_meizu_phone_list() + get_huawei_phone_list()


def get_taobao_phones_format_urls(phone):
    format_urls = []
    phone_lists = phone
    for i in phone_lists:
        # 构造规范的每种手机的淘宝搜索页面URL
        format_urls.append('https://list.tmall.com/search_product.htm?q=' + str(i))
    return format_urls


# 进行对应的数据库和数据表创建
def create_database_and_tables():
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='tentan', port=3306)
    cursor = conn.cursor()
    # 创建淘宝评论数据库的语句
    create_database = """CREATE  DATABASE IF NOT EXISTS TaobaoPhoneComment"""
    # 创建手机和对应网店地址数据表
    create_table_phoneurls = """CREATE TABLE IF NOT EXISTS phoneurls(id int not null primary key auto_increment, phone_type varchar(255), url varchar(255))"""
    # 创建某种类型手机的淘宝评论的数据表
    create_table_phonecomments = """CREATE TABLE IF NOT EXISTS phonecomments(id int not null primary key auto_increment, phone_name varchar(255), comment_star varchar(255), comment_con TEXT, comment_time varchar(255))"""
    try:
        cursor.execute(create_database)
        conn.select_db("TaobaoPhoneComment")
        cursor.execute(create_table_phoneurls)
        conn.commit()
        cursor.execute(create_table_phonecomments)
        conn.commit()
        print("1:创建数据库及数据表成功")
    except:
        # conn.select_db("TaobaoPhoneComment")
        try:
            cursor.execute(create_table_phoneurls)
            print("2:phoneurls数据表创建成功")
            cursor.execute(create_table_phonecomments)
            cursor.commit()
        except:
            cursor.execute(create_table_phonecomments)
            print("3:phonecomments数据表创建成功")
            cursor.commit()
    finally:
        cursor.close()
        conn.close()


# 将京东上的某种类型的手机所有的网店地址存入数据表
def save_taobao_every_phone_url_list():

    global phone_name

    # 获得每种手机的固定的搜索url列表
    every_phone_format_urls = get_taobao_phones_format_urls(phone_name)


    # 创建包含手机名称和对应的网店地址的数据表
    create_database_and_tables()
    insert_sql = "INSERT INTO phoneurls(phone_type, url) VALUES(%s, %s)"
    # 连接到数据库
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='tentan', db='TaobaoPhoneComment', charset="utf8", use_unicode=True)
    # 生成操作游标
    cursor = conn.cursor()
    for i in every_phone_format_urls:
        content = requests.get(i)
        print(content.text)

    # async def main():
    #     browser = await launch()
    #     page = await browser.newPage()
    #     try:
    #         await page.goto('https://taobao.com', {
    #             'timeout': 0,
    #             'waitUntil': 'networkidle0'
    #         })
    #     except:
    #         # 无网络 'net::ERR_INTERNET_DISCONNECTED','net::ERR_TUNNEL_CONNECTION_FAILED'
    #         raise
    #     # 这是获得爬取的网页的内容
    #     text = await page.content()
    #     print(text)
    #     await browser.close()
    #
    # asyncio.get_event_loop().run_until_complete(main())


# 运行TaobaoSavePhoneUrls函数
if __name__ == '__main__':
    save_taobao_every_phone_url_list()

