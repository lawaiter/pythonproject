import scrapy


class MobliephoneItem(scrapy.Item):
    # 定义你自己的Item在这里
    # name = scrapy.Field()
    comment_time = scrapy.Field()
    comment_con = scrapy.Field()
    comment_name = scrapy.Field()
    comment_star = scrapy.Field()
