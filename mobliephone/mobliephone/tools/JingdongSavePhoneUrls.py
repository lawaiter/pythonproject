# -*- coding: utf-8 -*-
# # -------------------------------------------------------------------------
# #   程序：JingdongSavePhoneUrls.py
# #   版本：0.1
# #   作者：lawaiter
# #   日期：编写日期20180411
# #   语言：Python 3.6
# #   功能：从数据库中读取手机类型，然后在京东上找对对应的网店，然后存入数据库备用
# # -------------------------------------------------------------------------
#   程序：JingdongSavePhoneUrls.py
#   版本：0.2
#   作者：lawaiter
#   日期：编写日期20180703
#   语言：Python 3.6
#   功能：从数据库中读取手机类型，然后在京东上找对对应的网店，然后存入数据库备用(添加魅族、华为两种手机类型)
# # -------------------------------------------------------------------------
#   程序：JingdongSavePhoneUrls.py
#   版本：0.3
#   作者：lawaiter
#   日期：编写日期20181231
#   语言：Python 3.6
#   功能：修改技术实现为使用selenium
#   TODO 下步计划将获取到的手机类型进行判断，确保不会出现获取的类型错误的情况，一个思路是将获取到手机类型使用百度进行搜索对比不同网页。
# -------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pymysql

import re

from mobliephone.tools.GetEveryPhoneType import get_xiaomi_phone_list, get_meizu_phone_list, get_huawei_phone_list


get_other_phone_list = []

# TODO 下步添加如何判断手机类型的方法
phone_name = get_xiaomi_phone_list() + get_meizu_phone_list() + get_huawei_phone_list()


# 进行京东手机商品类型对应的urls地址
def get_jingdong_phones_format_urls(phone):
    format_urls = []
    phone_lists = phone
    for i in phone_lists:
        format_urls.append('https://search.jd.com/Search?keyword=' + str(i) + '手机&enc=utf-8')
    return format_urls


# 进行对应的数据库和数据表创建
def create_database_and_tables():
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='tentan', port=3306)
    cursor = conn.cursor()
    # 创建京东数据库的语句
    create_database = """CREATE  DATABASE IF NOT EXISTS JingdongPhoneComment"""
    # 创建手机和对应网店地址数据表
    create_table_phoneurls = """CREATE TABLE IF NOT EXISTS phoneurls(id int not null primary key auto_increment, phone_type varchar(255), url varchar(255))"""
    # 创建某种类型手机的京东评论的数据表
    create_table_phonecomments = """CREATE TABLE IF NOT EXISTS phonecomments(id int not null primary key auto_increment, phone_name varchar(255), comment_star varchar(255), comment_con TEXT, comment_time varchar(255))"""
    try:
        cursor.execute(create_database)
        conn.select_db("JingdongPhoneComment")
        cursor.execute(create_table_phoneurls)
        conn.commit()
        cursor.execute(create_table_phonecomments)
        conn.commit()
        print("1:创建数据库及数据表成功")
    except:
        # conn.select_db("JingdongPhoneComment")
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
def save_jingdong_every_phone_url_list():
    # global phone
    # 创建数据库和数据表
    create_database_and_tables()
    insert_sql = "INSERT INTO phoneurls(phone_type, url) VALUES(%s, %s)"
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='tentan', db='JingdongPhoneComment', charset="utf8", use_unicode=True)
    cursor = conn.cursor()
    # 构造通用搜索格式的URL
    format_urls = get_jingdong_phones_format_urls(phone_name)
    # 配置webdriver
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    driver = webdriver.Firefox(firefox_options=firefox_options, firefox_profile=None)
    # 循环爬取手机类型对应的网店地址，每页60个店
    for every_phone_format_url in format_urls:
        type_key_word = re.compile(r'.*keyword=(.*)&', re.I)
        # 从URL中，提取手机类型名称
        every_phone_type = re.match(type_key_word, every_phone_format_url).group(1)
        # 访问对应手机类型的搜索页面
        driver.get(every_phone_format_url)
        driver.implicitly_wait(20)
        # 找对页面上网店所有的地址，每页60个存为列表
        every_type_phone_url_list = driver.find_elements_by_xpath("//div[@class='p-name p-name-type-2']/a")
        for every_type_phone_url in every_type_phone_url_list:
            phone_url = every_type_phone_url.get_attribute('href')
            print(phone_url)
            try:
                print(every_phone_type)
                cursor.execute(insert_sql, (str(every_phone_type), str(phone_url)))
                conn.commit()
            except:
                print("插入一条数据失败")
    cursor.close()
    conn.close()


if __name__ == "__main__":
    save_jingdong_every_phone_url_list()
