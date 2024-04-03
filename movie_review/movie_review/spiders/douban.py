# -*- coding: utf-8 -*-
import re
import csv
import os
import requests
from lxml.html import fromstring


import scrapy
from scrapy.http import Request


class DouBanSpider(scrapy.Spider):
    name = 'douban'

    def start_requests(self):
        if hasattr(self, 'movie_id'): 
            # The usage example: scrapy crawl douban -a movie_id=30424374
            top_list = [self.movie_id + '\n']
            self.review_csv_filename = f'review.{self.movie_id}.csv'
        else:
            if hasattr(self, 'top_list_path'):
                top_list_path = self.top_list_path
                self.review_csv_filename = f'review.{os.path.basename(top_list_path)}.csv'
            else:
                top_list_path = './data/top.txt'
                self.review_csv_filename = 'review.csv'
            with open(top_list_path, 'r') as f:
                top_list = f.readlines()
        
        if hasattr(self, 'episode'):
            self.review_csv_filename = self.review_csv_filename.replace('.csv', f'.{self.episode}.csv')

        for movie_id in top_list:
            if hasattr(self, 'episode'):
                # # Get last start 
                # response = requests.get("https://movie.douban.com/subject/{}/episode/{}/?discussion_start=0".format(movie_id, self.episode))
                # print(response.text)
                # soup = fromstring(response.text)
                # last_start_link = soup.xpath('//*[@id="content"]/div/div[1]/div[4]/a[10]/@href').get()
                # last_start = int(re.search(r'discussion_start=(\d+)', last_start_link).group(1))

                for start in range(0,230 + 1,10):
                    url = "https://movie.douban.com/subject/{}/episode/{}/?discussion_start={}".format(movie_id, self.episode, start)
                    yield Request(url=url)
            else:
                for start in range(0, 200, 20):
                    movie_id = movie_id.replace('\n', '')
                    url = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=new_score&status=P'.format(movie_id, start)
                    yield Request(url=url)

    def parse(self, response):
        if hasattr(self, 'episode'):
            review_list = response.xpath('//p/span[@class=""]/text()').extract()
        else:
            review_list = response.xpath('//span[@class="short"]/text()').extract()
        # XPath to the link to the last page in episode review response.xpath('//*[@id="content"]/div/div[1]/div[4]/a[10]/@href').get()
        print(review_list)
        for review in review_list:
            review = review.strip()
            review = review.replace('\t', '')
            review = review.replace('\n', '')
            review = review.replace('\xa0', '')
            review = review.replace('\ufeff', '')
            review = review.replace('\u200b', '')

            if review:
                review_csv_path = os.path.join('.','data',self.review_csv_filename)
                # Create the csv file if it doesn't exist
                if not os.path.exists(review_csv_path):
                    with open(review_csv_path, 'w', encoding='utf-8-sig') as f:
                        # Use utf-8-sig to avoid encoding issue https://blog.csdn.net/weixin_46640900/article/details/110602702
                        csv_write = csv.writer(f)
                        csv_write.writerow(['review'])
                with open(review_csv_path, 'a+', encoding='utf-8-sig') as f:
                    csv_write = csv.writer(f)
                    data_row = [review]
                    csv_write.writerow(data_row)
