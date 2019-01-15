# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi


class MobliephonePipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlTwistedPipeline(object):

    # 这个类pipeline， 用来进行异步存入数据库操作
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod  # 定义为类方法
    # 这是建立twisited提供的异步处理的连接池
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            password=settings["MYSQL_PASSWORD"],
            user=settings["MYSQL_USER"],
            db=settings["MYSQL_DBNAME"],
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        #  do_insert为我们具体进行的插入操作， item实际上就是我们需要存在的项目数据
        # 调用bdpool的runinteraction（执行插入动作）方法，进行异步操作
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 遇到异常的时候，进行异常处理
        query.addErrback(self.handle_error)  # 处理异常的具体动作
        return item

    def handle_error(self, failure, item, spider):
        # 处理异常的具体动作就是打印出异常
        # 这个函数是我们自己可以定义的，具体处理异常的动作由我们自己进行定义
        print(failure)

    def do_insert(self, cursor, item):
        # 这是函数就是执行具体的插入动作
        insert_sql = """INSERT INTO phonecomments(phone_name, comment_star, comment_con, comment_time, shop_name) VALUES (%s, %s, %s, %s)"""
        cursor.execute(insert_sql, (item["phone_name"], item['comment_star'], item["comment_con"], item["comment_time"]))


# 这是正常的将爬取到的数据存入Mysql数据库的Pipeline
class JingdongPipeline(object):

    # 初始化，首先是连接数据库
    def __init__(self):
        self.conn = pymysql.connect("127.0.0.1", "root", "tentan", "JingdongPhoneComment", charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    # 执行数据库插入新的数据的动作
    def process_item(self, item, spider):
        insert_sql = """INSERT INTO phonecomments(phone_name, comment_star, comment_con, comment_time) VALUES (%s, %s, %s, %s)"""
        self.cursor.execute(insert_sql, (item["phone_name"], item['comment_star'], item["comment_con"], item["comment_time"]))
        self.conn.commit()


# 这是一个返回时，将评论存储为文本的类
class MyCommentTextPipeline(object):
    pass


class ElasticsearchPipeline(object):

    """ 这是将scrapy获取的数据写入到elasticsearch中去"""

    def process_item(self, item, spider):
        # 将items转换为Es的中的数据模型
        item.save_to_es()
        # 返回item
        return item
