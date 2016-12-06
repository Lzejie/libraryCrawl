# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class BookItem(scrapy.Item):
    _id = Field()
    title = Field()
    author = Field()
    publicYear = Field()
    publisher = Field()
    summery = Field()
    ISBN = Field()
    imgLarge = Field()
    imgMedium = Field()
    imgSmall = Field()