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
import re
import requests
import MySQLdb
from mobliephone.tools.GetEveryPhoneType import get_xiaomi_phone_list, get_meizu_phone_list, get_huawei_phone_list


get_other_phone_list = []

# TODO 下步添加如何判断手机类型的方法
phone_name = get_xiaomi_phone_list() + get_meizu_phone_list() + get_huawei_phone_list()


def get_taobao_phones_format_urls(phone):
    format_urls = []
    phone_lists = phone
    for i in phone_lists:
        # 构造规范的每种手机的淘宝搜索页面URL
        format_urls.append('https://s.taobao.com/search?q=' + str(i))
    return format_urls


# 进行对应的数据库和数据表创建
def create_database_and_tables():
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='tentan', port=3306)
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

    # 创建包含手机名称和对应的网店地址的数据表
    create_database_and_tables()
    insert_sql = "INSERT INTO phoneurls(phone_type, url) VALUES(%s, %s)"
    # 连接到数据库
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='tentan', db='taobaophonecomment', charset="utf8", use_unicode=True)
    # 生成操作游标
    cursor = conn.cursor()

    # 从firefox中导出cookie
    cookies = {
            "name": "cna",
            "value": "edlYElwrHT4CATFf3tj9yCsP",
            "domain": ".taobao.com",
            "hostOnly": 'false',
            "path": "/",
            "secure": 'false',
            "httpOnly": 'false',
            "session": 'false',
            "expirationDate": '1854062997',
            "storeId": "firefox-default",
            "sameSite": "no_restriction",
            "firstPartyDomain": ""
        }

    # 自定义请求头
    headers = {
               'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0",
               }

    # 获得每种手机的固定的搜索url列表
    every_phone_format_urls = get_taobao_phones_format_urls(phone_name)

    # 对于每种手机的搜索URL进行遍历
    for every_phone_format_url in every_phone_format_urls:
        # 获得手机类型的关键词
        type_key_word = re.compile(r'.*q=(.*)', re.I)
        # 获得手机的类型名称
        every_phone_type = re.match(type_key_word, every_phone_format_url).group(1)

        # 使用requests获得每种手机的搜索页面结果
        content = requests.get(every_phone_format_url, headers=headers, cookies=cookies).text

        # 获得每种手机的所有网店页面地址列表
        keys = re.compile(r'"detail_url":"//.*?,"view_price"')
        # 找到每个网店页面地址
        for detail_url in re.findall(keys, content):
            # 解析出具体单个的网页页面地址
            every_detail_url = re.match(r'"detail_url":"//(.*?)","view_price"', detail_url).group(1)
            # 添加https头，构造完整的URL， 其中上一步解析出来的内容是含有unicode的str， 需要先按照utf-8编码，然后再解码城Unicode
            # 供python3本身输出，python3将自动将Unicode格式转换为Str格式输出
            phone_url = str('https://' + every_detail_url.encode('utf-8').decode('unicode_escape'))
            print(phone_url)
            # 将对应的手机种类、具体网店地址存入对应的phoneurls数据表
            try:
                cursor.execute(insert_sql, (str(every_phone_type), str(phone_url)))
                conn.commit()
            except:
                print("插入一条数据失败")
    # 关闭游标和数据库连接
    cursor.close()
    conn.close()


# 运行TaobaoSavePhoneUrls函数
if __name__ == '__main__':
    save_taobao_every_phone_url_list()
