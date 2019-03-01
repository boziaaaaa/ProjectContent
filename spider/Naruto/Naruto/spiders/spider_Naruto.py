#coding=utf8
import scrapy

class spider_Naruto(scrapy.Spider):
    name = "Naruto"
    allowed_domains = ['comic.kukudm.com']
    start_urls = ['http://comic.kukudm.com/comiclist/3/']
    def parse(self,response):
        urls = response.xpath('//dd/a[1]/@href').extract()
        for url_each in urls:
            print('http://comic.kukudm.com'+url_each)
        urls = response.xpath('//dd/a[1]/text()').extract()
        for url_each in urls:
            print(url_each)

