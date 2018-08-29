# -*- coding: utf-8 -*-
import scrapy


class DbbookSpider(scrapy.Spider):
    name = 'dbbook'
    allowed_domains = ['http://xz.58.com/chuzu/']
    start_urls = ['http://xz.58.com/chuzu/?utm_source=link&spm=s-41968205011985\
                  -pe-f-801.psy_startpage_site&PGTID=0d3090a7-001d-7815-a9d0-9b\
                  77cf6f84fb&ClickID=2']

    def parse(self, response):
        prices = response.xpath("/html/body/div[3]/div[1]/div[5]/div[2]/ul/li[@\
                                sortid]/div[3]/div[2]/b/text()").extract()
        print(type(prices))
        print(prices)