import pandas as pd
df = pd.read_excel('E:/Blackcoffee/data/input.xlsx')
urls=df['URL'].tolist()

import os
os.system("scrapy crawl content")

import scrapy
class ContentSpider(scrapy.Spider):
    name = 'content'
    start_urls = urls
    def parse(self, response):
        #Extracting the content using css selectors
        titles = response.css('.entry-title::text').getall()
        cont = [response.xpath('//p/text()').getall()]
   
       
        #Give the extracted content row wise
        for item in zip(titles,cont):
            #create a dictionary to store the scraped info
            scraped_info = {
                'title' : item[0],
                'cont' : item[1],
            }

            #yield or give the scraped info to scrapy
            
            yield scraped_info

