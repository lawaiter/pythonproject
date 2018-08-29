# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request, HtmlResponse
from bolezaixian.items import LagouItemLoader, LagouJobItem
from bolezaixian.spiders.jobbole import get_md5
from datetime import datetime
from scrapy.loader import ItemLoader


agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
}

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    rules = (
        #Rule(LinkExtractor(allow=(r'zhaopin/.*'),), callback='parse_job',follow=True),
        #Rule(LinkExtractor(allow=(r'gongsi/\d+.html'),),  callback='parse_job',follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )

    def parse_job(self, response):
        # 这是专门用来解析拉勾网职位的函数
        item_loader = LagouItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css("title", ".job-name::attr(title)")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("salary", '.job_request .salary::text')
        item_loader.add_xpath("job_city", "//*[@class='job_request']/p/span[2]")
        item_loader.add_xpath("work_years", "//*[@class='job_request']/p/span[3]")
        item_loader.add_xpath("degree_need", "//*[@class='job_request']/p/span[4]")
        item_loader.add_xpath("job_type", "//*[@class='job_request']/p/span[5]")
        item_loader.add_css("tags", ".position-label li::text")
        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_css("job_advantage", ".publish_time::text")
        item_loader.add_css("company_name", "#job_company dt a img::attr(alt)")
        item_loader.add_css("company_url", "#job_comapny dt a a::attr(href)")
        item_loader.add_value("crawls_time", datetime.now())
        job_item = item_loader.load_item()
        return job_item

    def _build_request(self, rule, link):
        r = Request(url=link.url, callback=self._response_downloaded, headers=header)
        r.meta.update(rule=rule, link_text=link.text)
        return r
