# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from elasticsearch_dsl.connections import connections
from .models.Es_models import JINGDONGCOMMENT


es = connections.create_connection(JINGDONGCOMMENT._doc_type.using)


# 在搜索框输入之后，生成一定的搜索建议
def gen_suggets(index, info_tuple):
    used_words = set()
    suggets = []
    # 对于输入的字符，分析文本和对应的权重
    for text, weight in info_tuple:
        if text:
            # 调用Es的analyze的接口进行分析
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter': ['lowercase']}, body=text)
            analyzed_words = set([r['token'] for r in words['tokens'] if len(r['token']) > 1])
            new_words = analyzed_words - used_words
        else:
            new_words = set()
        if new_words:
            suggets.append({"input": list(new_words), "weight": weight})
    return suggets


class MobliephoneItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    comment_time = scrapy.Field()
    comment_con = scrapy.Field()
    phone_name = scrapy.Field()
    comment_star = scrapy.Field()

    # 将item保存到es数据模型之中
    def save_to_es(self):
        from .models import Es_models
        # models的对象
        jingdong_comments = Es_models.JINGDONGCOMMENT()
        # 将获得的数据，通过Item将数据写入Elsaticsearch中的mappings(字段)
        jingdong_comments.comment_time = self['comment_time']
        jingdong_comments.comment_star = self['comment_star']
        jingdong_comments.phone_name = self['phone_name']
        jingdong_comments.comment_con = self['comment_con']
        jingdong_comments.suggest = gen_suggets(JINGDONGCOMMENT._doc_type.index, ((jingdong_comments.phone_name, 10), (jingdong_comments.comment_con, 7)))

        # 保存实例化后的数据模型,类似Django中的model
        jingdong_comments.save()
