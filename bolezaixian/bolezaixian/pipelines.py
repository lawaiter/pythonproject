# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class BolezaixianPipeline(object):
    def process_item(self, item, spider):
        return item


class imagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value["path"]
            item["front_image_path"] = image_file_path
            return item


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open("bolearticle.json", "w", encoding="UTF-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self):
        self.file.close()


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect("127.0.0.1", "root", "tentan", "bilezaixian", charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into articleinfo(title, time2, url, url_object_id, save, vote, said, front_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["time"], item["url"], item["url_object_id"], item["save"], item["vote"], item["said"], item["front_image"]))
        self.conn.commit()


class MysqlTwistedPipeline(object):
    # 这个类pipeline， 用来进行异步存入数据库操作
    def __init__(self):
        self.dbpool = dbpool

    @classmethod  # 定义为类方法
    # 这是建立twisited提供的异步处理的连接池
    def from_setting(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            password=settings["MYSQL_PASSWORD"],
            user=settings["MYSQL_USER"],
            db=settings["MYSQL_DBNAME"],
            charset="utf8",
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item):
        # 使用twisted将mysql插入变成异步执行
        #  do_insert为我们具体进行的插入操作， item实际上就是我们需要存在的项目数据
        # 调用bdpool的runinteraction（执行插入动作）方法，进行异步操作
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 遇到异常的时候，进行异常处理
        query.addErrback(self.handle_error)  # 处理异常的具体动作

    def handle_error(self, failure):
        # 处理异常的具体动作就是打印出异常
        # 这个函数是我们自己可以定义的，具体处理异常的动作由我们自己进行定义
        print(failure)

    def do_insert(self, cursor, item):
        # 这是函数就是执行具体的插入动作
        insert_sql = """
            insert into articleinfo(title, time2, url, url_object_id, save, vote, said, front_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (item["title"], item["time"], item["url"], item["url_object_id"], item["save"], item["vote"], item["said"], item["front_image"]))