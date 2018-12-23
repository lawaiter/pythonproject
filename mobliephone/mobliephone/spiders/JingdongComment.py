# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
#   程序：JingdongComment.py
#   版本：0.1
#   作者：lawaiter
#   日期：编写日期20180411
#   语言：Python 3.6
#   功能：从mysql中读取对应的手机类型和京东上面的网店地址，然后爬取评论内容和评论时间
#   TODO 下步将京东爬虫改写为多线程爬虫，同时要将pipelines进行数据库异步存储改写
# -------------------------------------------------------------------------

import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import pymysql
from random import randint
import re
# from mobliephone.items import MobliephoneItem
# from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher


# 从数据库中读取对应的手机类型和京东网店对应的地址
def get_phone_url_from_mysql():
    # 连接存取着手机的京东网店数据库
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='tentan', db='JingdongPhoneComment', port=3306, charset="utf8", use_unicode=True)
    cursor = conn.cursor()
    query_phone_info = "SELECT phone_type, url FROM phoneurls"
    phone_url_lists = []
    # 对应手机类型和网店地址进行查询
    try:
        cursor.execute(query_phone_info)
        print("已经查询到数据")
        for i in cursor.fetchall():
            phone_type = i[0]
            phone_shop = i[1]
            # 将数据存在列表中备用查询
            phone_url_lists.append([phone_type, phone_shop])
    except:
        print("读取数据失败")
    cursor.close()
    conn.close()
    print(phone_url_lists)
    return phone_url_lists


# 对于京东网店的评论进行ITEM迭代返回
def parse_shop_comment(phoneitem, comments_cons, comments_times, comments_stars, phone_kinds, num):
    phone_item = phoneitem
    phone_item['comment_con'] = ''.join(comments_cons[num])
    phone_item['comment_time'] = comments_times[num]
    phone_item['comment_star'] = comments_stars[num]
    phone_item['phone_name'] = phone_kinds
    print(phone_item['phone_name'])
    print(phone_item['comment_time'])
    print(phone_item['comment_con'])
    print(phone_item['comment_star'])
    print("----------------------------------------------------------------------")
    yield phone_item


# 这是计划加入的超时处理的函数
# def func_timeout():
#    pass

# 获取京东手机评论的主爬虫类
class JingdongCommentSpider(scrapy.Spider):

    name = 'JingdongComment'
    allowed_domains = ['https://shouji.jd.com/']
    start_urls = ['https://shouji.jd.com/']
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    # 这是启动IP代理的代码
    '''profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', 1)  # 默认值0，就是直接连接；1就是手工配置代理。  
    profile.set_preference('network.proxy.http', ip_ip)
    profile.set_preference('network.proxy.http_port', ip_port)
    profile.set_preference('network.proxy.ssl', ip_ip)
    profile.set_preference('network.proxy.ssl_port', ip_port)
    
    # 这是设置User-Agent
    profile.set_preference("general.useragent.override", user_agent)
    profile.update_preferences()
    driver = webdriver.Firefox(profile)'''


    def __init__(self):
        self.driver = webdriver.Firefox(firefox_options=self.firefox_options, firefox_profile=None)
        super(JingdongCommentSpider, self).__init__()
        # 传递信息,也就是当爬虫关闭时scrapy会发出一个spider_closed的信息,当这个信号发出时就调用closeSpider函数关闭这个浏览器.
        '''dispatcher.connect(self.closespider, signals.spider_closed)'''

    def closespider(self, spider):
        print("spider closed")
        # 当爬虫退出的时关闭浏览器
        self.driver.quit()

    # 对网店页面的内容进行解析
    def parse_phone(self):
        comment_cons = []
        comment_times = []
        comment_stars = []
        # 获取该页所有的评论列表
        comment_con = self.driver.find_elements_by_xpath("//div[@class='comment-column J-comment-column']/"
                                                         "p[@class='comment-con']")
        phone_info = self.driver.find_elements_by_class_name("order-info")
        comment_star = self.driver.find_elements_by_xpath("//div[@class='comment-column J-comment-column']/div[1]")
        phone_kind = self.driver.find_element_by_xpath("//div[@class='item ellipsis']").text
        for comment in comment_con:
            comment_cons.append(comment.text)
        for phone_info in phone_info:
            time_tup = re.match(".*(\d{4})-(\d{2})-(\d{2}).*(\d{2}):(\d{2})", phone_info.text).groups()
            comment_times.append(''.join(list(time_tup)))
        for star in comment_star:
            a = re.match('.*star(\d)', star.get_attribute("class"))
            if a:
                comment_stars.append(a.group(1))
        print(phone_kind, comment_cons, comment_times, comment_stars)
        return phone_kind, comment_cons, comment_times, comment_stars

    # 解析网店评论的主要部分
    def parse(self, response):
        gotten_urls = []
        phone_list = get_phone_url_from_mysql()
        for i in phone_list:
            phone_name = i[0]
            phone_shop_url = i[1]
            if phone_shop_url in gotten_urls:
                continue
            else:
                try:
                    gotten_urls.append(phone_shop_url)
                    self.driver.get(phone_shop_url)
                    time.sleep(randint(15, 20))
                    # 点击页面中的评论选项
                    if re.match('.*手机壳.*', self.driver.find_element_by_xpath("//div[@class='item ellipsis']").text):
                        continue
                    else:
                        try:
                            self.driver.find_element_by_xpath("//li[@data-anchor='#comment']").click()
                            time.sleep(randint(3, 5))
                            # 连续获得该网店下所有的评论
                            for times in range(0, 10000):
                                # 将第一页的评论储存起来，用来重新爬取的时候的比较
                                if times == 0:
                                    phone_kind, comment_con, comment_time, comment_star = self.parse_phone()
                                    for nu in range(0, len(comment_con)):
                                        print(('进入'+phone_shop_url))
                                        print(nu)
                                        m = parse_shop_comment(MobliephoneItem(), comment_con, comment_time,
                                                               comment_star, phone_kind, nu)
                                        for everyone in m:
                                            yield everyone
                                    if self.driver.find_element_by_xpath("//div[@class='com-table-footer']/div[class"
                                                                         "='ui-page-wrap clearfix']/div[@class="
                                                                         "'ui-page']/a[@class='ui-pager-next']"):
                                        self.driver.find_element_by_xpath("//div[@class='com-table-footer']/div["
                                                                          "@class='ui-page-wrap clearfix']/div"
                                                                          "@class='ui-page']/a["
                                                                          "@class='ui-pager-next']").click()
                                        time.sleep(randint(7, 10))
                                    else:
                                        print("该店铺下的评论获取完毕")
                                        break
                                else:
                                    phone_kind, comment_con, comment_time, comment_star = self.parse_phone()
                                    for nu in range(0, len(comment_con)):
                                        print(('进入'+phone_shop_url))
                                        print(nu)
                                        m = parse_shop_comment(MobliephoneItem(), comment_con, comment_time,
                                                               comment_star, phone_kind, nu)
                                        for everyone in m:
                                            yield everyone
                                    if self.driver.find_element_by_xpath("//div[@class='com-table-footer']/div["
                                                                         "@class='ui-page-wrap clearfix']/div[@"
                                                                         "class='ui-page']/a[@class='ui-pager-next']"):
                                        self.driver.find_element_by_xpath("//div[@class='com-table-footer']/div@class="
                                                                          "'ui-page-wrap clearfix']/div[@class='ui"
                                                                          "-page']/a[@class='ui-pager-next']").click()
                                        time.sleep(randint(7, 10))
                                    else:
                                        print("该店铺下的评论获取完毕")
                                        break
                        except:
                            print("获取字段不正常")
                except:
                    print("不能正常访问的url记录下来")
                    # 计划加入处理不正常访问的网店的地址continue
