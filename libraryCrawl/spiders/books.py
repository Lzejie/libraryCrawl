# -*- coding: utf-8 -*-
import scrapy
import re
import json
import urllib

from libraryCrawl.items import BookItem
from libraryCrawl.header import getHeader

class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = ['http://210.38.207.15:169/web/bookinfo.aspx?ctrlno=%s'%index for index in range(1, 695500)]

    bookInfoUrl = 'https://api.douban.com/v2/book/isbn/%s'

    re_title = re.compile(u'　　(.*?)／')
    re_author = re.compile(u'／(.*?)．—')
    re_publicPlace = re.compile(u'．—(.*?)：')
    re_publisher = re.compile(u'：(.*?)，')
    re_publicYear = re.compile(u'，(.*?)\n')
    re_ISBN = re.compile(u'ISBN ?(.*?)：| :?')


    def parse(self, response):
        content = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_bookcardinfolbl"]/text()').extract()
        bid = response.url.split('=')[-1]
        jsonData = {}
        try:
            ISBN = self.re_ISBN.findall(''.join(content))[0].replace(u'-', '')
            if u'（' in ISBN:
                ISBN = ISBN[:-3].replace(' ', '')
                jsonData = json.loads(urllib.urlopen(self.bookInfoUrl % ISBN).read())
        except:
            ISBN = ''

        if ISBN and jsonData.get('code', '0') != 6000:
            imgLarge = jsonData.get('images',{}).get('large', '')
            imgMedium = jsonData.get('images',{}).get('medium', '')
            imgsmall = jsonData.get('images',{}).get('small', '')

            title = jsonData.get('title', u'未找到书籍名')
            author = jsonData.get('author')
            publisher = jsonData.get('publisher', u'未找到出版社')
            publicYear = jsonData.get('pubdate', u'未知出版时间')
            summery = jsonData.get('summary', u'暂无')
        else:
            title = self.re_title.findall(content[0])[0]
            author = self.re_author.findall(content[0])[0]
            try:
                publisher = self.re_publisher.findall(content[0])[0]
            except:
                publisher = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_bookcardinfolbl"]/a/text()').extract()[0]
            publicYear = content[1].split(u'，')[1]
            summery = content[5]
            imgLarge = ''
            imgMedium = ''
            imgsmall = ''

        item = BookItem()
        item['_id'] = bid
        item['title'] = title
        item['author'] = author
        item['publicYear'] = publicYear
        item['publisher'] = publisher
        item['summery'] = summery
        item['ISBN'] = ISBN
        item['imgLarge'] = imgLarge
        item['imgMedium'] = imgMedium
        item['imgSmall'] = imgsmall

        yield item


