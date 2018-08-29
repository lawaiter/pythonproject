# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
#   程序：JGetEveryPhoneType.py
#   版本：0.1
#   作者：lawaiter
#   日期：编写日期20180411
#   语言：Python 3.6
#   功能：从手机官网上找到对应的手机类型，然后返回列表备用
# -------------------------------------------------------------------------
#   程序：JGetEveryPhoneType.py
#   版本：0.2
#   作者：lawaiter
#   日期：编写日期20180703
#   语言：Python 3.6
#   功能：从手机官网上找到对应的手机类型（完善除小米之外其他种类的手机的获取,其中锤子和nubia手机类型不能获取，华为只获取了一页类型）
#   TODO 下步计划加入获取锤子手机和Nubia手机类型的功能
# -------------------------------------------------------------------------
import requests
from scrapy.selector import Selector
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"}
phone_dict = {
            'xiaomi': 'https://www.mi.com/index.html',
            'meizu': 'https://lists.meizu.com/page/list/?categoryid=76',
            'huawei': 'https://www.vmall.com/list-36',
            'chuizi': 'https://www.smartisan.com/',
            'nubia': 'https://shop.nubia.com/phone'
            }

# 这是利用selenium进行各个品牌手机类型爬取
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


def get_xiaomi_phone_list():
    """用于获取小米手机官网小米手机种类"""
    xiaomi = requests.get(phone_dict['xiaomi'], headers=headers)
    xiaomi_phone_list = []
    selector = Selector(text=xiaomi.text)
    xiaomi_phone = selector.css('div .title a::text').extract()
    res = re.compile(r'"(小米[a-zA-Z0-9]+\s*[a-zA-Z0-9]+$)|(红米[a-zA-Z0-9]+\s*[a-zA-Z0-9]+$)|(小米[a-zA-Z0-9]+$)|"'
                     r'(红米[a-zA-Z0-9]+$)|(小米[a-zA-Z0-9]+.*版$)|(红米[a-zA-Z0-9]+.*版$)', re.I)
    for i in xiaomi_phone:
        if re.match(res, i) != None:
            xiaomi_phone_list.append(i)
    print(xiaomi_phone_list)
    return xiaomi_phone_list


def get_meizu_phone_list():
    """用于获取魅族手机类型，从魅族官网上"""
    meizu = requests.get(phone_dict["meizu"], headers=headers)
    selector = Selector(text=meizu.text)
    meizu_phone = selector.css("html body main#main.wrapper.page-search div.container section#goodsList.goods-list "
                                "ul#goodsListWrap.goods-list-wrap.clearfix li.gl-item a div.gl-item-wrap "
                                "h2::text").extract()
    print(meizu_phone)
    meizu_phone_list = meizu_phone
    return meizu_phone_list


def get_huawei_phone_list():
    """用于获取华为手机类型，从华为官网上"""
    huawei = requests.get(phone_dict["huawei"], headers=headers)
    selector = Selector(text=huawei.text)
    huawei_phone = selector.css("html body.wide div.layout div.channel-list div.pro-list.clearfix ul li div.pro-panels p.p-name a span::text").extract()
    print(huawei_phone)
    huawei_phone_list = huawei_phone
    return huawei_phone_list


# TODO 下步添加获取锤子手机的方法
def get_chuizi_phone_list():
    """用于获取锤子手机类型，从锤子官网上，动态网页技术功能待实现"""
    pass


# TODO 下步添加获取nubia手机的方法
def get_nubia_phone_list():
    """用于获取nubia手机类型，从nubia官网上，动态网页技术功能待实现"""
    pass

get_huawei_phone_list()
