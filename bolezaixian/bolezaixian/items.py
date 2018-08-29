# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader

class BolezaixianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class bolezaixian(scrapy.Item):
    title = scrapy.Field(
        input_processor = MapCompose()
    )
    time = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    save = scrapy.Field()
    vote = scrapy.Field()
    said = scrapy.Field()
    front_image = scrapy.Field()
    front_image_path = scrapy.Field()

class LagouJobItem(scrapy.Item):
    # 拉勾网职位信息字段
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field()
    degree_need = scrapy.Field()
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    jod_desc = scrapy.Field()
    job_address = scrapy.Field()
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    tags = scrapy.Field()
    crawls_time = scrapy.Field()

def LagouItemLoader(ItemLoader):
    # 重载Itemloader
    default_output_processor = ItemLoader.TakeFirst()

    work_years = scrapy.Field()


