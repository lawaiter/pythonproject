# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MobliephoneItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    comment_time = scrapy.Field()
    phone_color = scrapy.Field()
    phone_price = scrapy.Field()
    comment_con = scrapy.Field()
    phone_name = scrapy.Field()
    phone_type = scrapy.Field()
    comment_star = scrapy.Field()

    pass
