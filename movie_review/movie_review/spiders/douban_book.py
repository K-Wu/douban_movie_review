import scrapy
from .douban import DouBanSpider


class DouBanSpider(DouBanSpider, scrapy.Spider):
    name = 'douban_book'
    url_prefix = 'https://book.douban.com/subject/'