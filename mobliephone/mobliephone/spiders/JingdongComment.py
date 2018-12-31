# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
#   程序：JingdongComment.py
#   版本：0.1
#   作者：lawaiter
#   日期：编写日期20181231
#   语言：Python 3.6
#   功能：从mysql中读取对应的手机类型和京东上面的网店地址，然后爬取评论内容和评论时间
#   TODO 下步将京东爬虫改写为多线程爬虫，同时要将pipelines进行数据库异步存储改写
# -------------------------------------------------------------------------

import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from selenium.webdriver.common.action_chains import ActionChains
import pymysql

import time
from random import randint

import re
from mobliephone.items import MobliephoneItem


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
        dispatcher.connect(self.closespider, signals.spider_closed)

    def closespider(self, spider):
        print("spider closed")
        # 当爬虫退出的时关闭浏览器
        self.driver.quit()

    # 对网店页面的内容进行解析
    def parse_phone(self):
        comment_cons = []
        comment_times = []
        comment_stars = []
        phone_kinds = []
        # 获取该页所有的评论列表
        comment_con = self.driver.find_elements_by_xpath("//div[@class='comment-item']/div[@class='comment-column J-comment-column']/"
                                                         "p[@class='comment-con']")
        phone_info = self.driver.find_elements_by_class_name("order-info")
        comment_star = self.driver.find_elements_by_xpath("//div[@class='comment-item']/div[@class='comment-column J-comment-column']/div[1]")
        phone_kind = self.driver.find_elements_by_xpath("//div[@class='item ellipsis']")
        # 获取每条评论
        for comment in comment_con:
            comment_cons.append(comment.text)
        # 获取每条评论时间，格式为20181124
        for phone in phone_info:
            time_tup = re.match(".*(\d{4})-(\d{2})-(\d{2}).*(\d{2}):(\d{2})", phone.text).groups()
            comment_times.append(''.join(list(time_tup)))
        # 获取每条评论星等
        for star in comment_star:
            a = re.match('.*star(\d)', star.get_attribute("class"))
            if a:
                comment_stars.append(a.group(1))
        # 获取每条评论的手机类型
        for kind in phone_kind:
            phone_kinds.append(kind.text)
        print(phone_kinds, comment_cons, comment_times, comment_stars)
        return phone_kinds, comment_cons, comment_times, comment_stars

    # 解析网店评论的主要部分，采取的是使用selenium直接访问，然后点击评论翻页码
    def parse(self, response):
        # 记录已经爬取URL
        gotten_urls = []
        # 记录错误URL
        error_urls = []
        # 从数据库中获取手机网店数据
        phone_list = get_phone_url_from_mysql()
        # 提取数据名称和网店网址
        for record in phone_list:
            phone_name = record[0]
            phone_shop_url = record[1]
            # 如果已经爬取了，就不爬取
            if phone_shop_url in gotten_urls:
                continue
            else:
                try:
                    # 访问该网店
                    self.driver.get(phone_shop_url)
                    time.sleep(randint(10, 20))
                    # 如果是卖手机壳的网店，就不爬取
                    if re.match('.*手机壳.*', self.driver.find_element_by_xpath("//div[@class='item ellipsis']").text):
                        error_urls.append(phone_shop_url)
                        continue
                    else:
                        try:
                            gotten_urls.append(phone_shop_url)
                            # 找到评论按钮并点击
                            self.driver.find_element_by_xpath("//li[@data-anchor='#comment']").click()
                            time.sleep(randint(5, 8))
                            self.driver.implicitly_wait(20)
                            # 连续获得该网店下所有的评论
                            for times in range(0, 10000):
                                # 获取评论页第一页内容
                                phone_kind, comment_con, comment_time, comment_star = self.parse_phone()
                                if len(phone_name) >= len(phone_kind[0]):
                                    phone_kind = phone_name
                                try:
                                    # 依次写入每一评论页的每条评论，一个十个评论
                                    for nu in range(0, len(comment_con)):
                                        print(('进入' + phone_shop_url))
                                        print(nu)
                                        m = parse_shop_comment(MobliephoneItem(), comment_con, comment_time,
                                                               comment_star, phone_kind, nu)
                                        # 进入Pipeline,写入数据库
                                        for i in m:
                                            yield i
                                except:
                                    print("十个评论获取完毕")
                                finally:
                                    # 最后如果评论下一页存在的话，点击下一页评论
                                    if self.driver.find_element_by_xpath("//div[@class='com-table-footer']/div[@class='ui-page-wrap clearfix']/div[@class='ui-page']/a[@class='ui-pager-next']").text:
                                        print(self.driver.find_element_by_xpath("//div[@class='com-table-footer']/div[@class='ui-page-wrap clearfix']/div[@class='ui-page']/a[@class='ui-pager-next']").text)
                                        # 找到下一页所在的标签位置
                                        next_page_comment = self.driver.find_element_by_xpath("//div[@class='com-table-footer']/div[@class='ui-page-wrap clearfix']/div[@class='ui-page']/a[@class='ui-pager-next']")
                                        # 模拟鼠标滚动十分之一的页面
                                        scroll_js = "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight/2; return lenOfPage;"
                                        self.driver.execute_script(scroll_js)
                                        self.driver.execute_script(scroll_js)
                                        self.driver.execute_script(scroll_js)
                                        self.driver.execute_script(scroll_js)
                                        self.driver.execute_script(scroll_js)
                                        self.driver.execute_script(scroll_js)
                                        # 点击评论按钮
                                        time.sleep(randint(8, 13))
                                        next_page_comment.click()
                                        # 隐形等待加载
                                        self.driver.implicitly_wait(20)
                        except Exception as e:
                            # 捕获异常并打印
                            print(e)
                            print("获取字段不正常")
                except:
                    print("不能正常访问的url记录下来")
                    # 计划加入处理不正常访问的网店的地址continue
                    error_urls.append(phone_shop_url)
