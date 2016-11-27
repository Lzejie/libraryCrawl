# -*- coding: utf-8 -*-
import scrapy
import re
import json
import urllib

from libraryCrawl.items import BookItem

class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = ['http://210.38.207.15:169/web/bookinfo.aspx?ctrlno=%s'%index for index in range(1, 695500)]

    bookInfoUrl = 'https://api.douban.com/v2/book/isbn/%s'

    re_title = re.compile(u'　　(.*?)／')
    re_author = re.compile(u'／(.*?)．—')
    re_publicPlace = re.compile(u'．—(.*?)：')
    re_publisher = re.compile(u'：(.*?)，')
    re_publicYear = re.compile(u'，(.*?)\n')
    re_ISBN = re.compile(u'ISBN(.*?)：')


    def parse(self, response):
        content = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_bookcardinfolbl"]/text()').extract()
        bid = response.url.split('=')[-1]
        title = self.re_title.findall(content[0])[0]
        author = self.re_author.findall(content[0])[0]
        publicPlace = self.re_publicPlace.findall(content[0])[0]
        try:
            publisher = self.re_publisher.findall(content[0])[0]
        except:
            publisher = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_bookcardinfolbl"]/a/text()').extract()[0]
        publicYear = content[1].split(u'，')[1]
        # summery = content[5]
        try:
            ISBN = self.re_ISBN.findall(''.join(content))[0].replace(u'-', '')
            if u'（' in ISBN:
                ISBN = ISBN[:-3]
        except:
            ISBN = ''

        jsonData = json.loads(urllib.urlopen(self.bookInfoUrl%ISBN).read())
        try:
            imgLarge = jsonData['images']['large']
            imgMedium = jsonData['images']['medium']
            imgsmall = jsonData['images']['small']
        except:
            imgLarge = ''
            imgMedium = ''
            imgsmall = ''

        item = BookItem()
        item['id'] = bid
        item['title'] = title
        item['author'] = author
        item['publicPlace'] = publicPlace
        item['publicYear'] = publicYear
        item['publisher'] = publisher
        # item['summery'] = summery
        item['ISBN'] = ISBN
        item['imgLarge'] = imgLarge
        item['imgMedium'] = imgMedium
        item['imgSmall'] = imgsmall

        yield item


