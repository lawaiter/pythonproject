# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from bolezaixian.items import bolezaixian
import re
import hashlib
from scrapy.loader import ItemLoader


def get_md5(url):
    # 这是进行MD5转化url的函数(Unicode编码不支持转换MD5)
    if isinstance(url, str):# str类型等同于unicode编码，python3中没有Unicode这样的关键字
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobble.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    """
    
    1.获取文章列表页中的文章url并交给解析函数进行具体的解析
    2.获取下一页的URL并交给scrapy进行下载，下载完成后交给parse进行递归及解析处理
    """

    def parse(self, response):

        # 解析列表页中的URL并交给scrapy进行下载后解析
        post_nodes = response.css("#archive div.floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_img_url": image_url}, callback=self.parse_detail, dont_filter=True)

        # 提取下一页并交给scrapy进行下载
        next_urls = response.css('.next.page-numbers::attr(href)').extract_first("")
        if next_urls:
            yield Request(url=parse.urljoin(response.url, next_urls), callback=self.parse, dont_filter=True)
        else:
            return

    def parse_detail(self, response):
        bole_item = bolezaixian()
        # 这个函数负责解析具体的文章名称、时间、赞等内容
        try:
            title = response.xpath('//div[@class="entry-header" ]/h1/text()').extract()[0]
        except:
            title = "未知"
        try:
            front_image = response.meta.get("front_img_url", "")
        except:
            front_image = ""
        try:
            time = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip()[0:9]
        except:
            time = "未知"
        try:
            vote = response.xpath('//span[@class=" btn-bluet-bigger href-style vote-post-up   register-user-only "]/h10/text()').extract()
            if vote:
                vote = vote[0]
            else:
                vote = '0'
        except:
            vote = '0'
        try:
            save = response.xpath('//*/span[@class=" btn-bluet-bigger href-style bookmark-btn  register-user-only "]/text()').extract()
            if save:
                save = save[0].strip()[0]
                if re.match('.*[0-9]+.*', save):
                    pass
                else:
                    save = '0'
            else:
                save = "0"
        except:
            save = '0'
        try:
            said = response.xpath('//*/a[@href="#article-comment"]/text()').extract()
            if said:
                said = said[0].strip()[0]
            else:
                said = "0"
        except:
            said = '0'
        # 将内容输出到管道文件
        bole_item["title"] = title
        bole_item["url_object_id"] = get_md5(response.url)
        bole_item["url"] = response.url
        bole_item["save"] = save
        bole_item["vote"] = vote
        bole_item["said"] = said
        bole_item["front_image"] = [front_image]
        bole_item["time"] = time
        yield bole_item


    # 通过Itemloader进行Item的加载和提取
        item_loader = ItemLoader(item=bolezaixian(), response=response)
        item_loader.add_xpath("title", '//div[@class="entry-header" ]/h1/text()')
        item_loader.add_value("url", response.url)
        article_item = item_loader.load_item()


