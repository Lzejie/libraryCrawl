# -*- coding: utf-8 -*-

from pymongo import *

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class LibrarycrawlPipeline(object):
    def __init__(self):
        mongodb = MongoClient('localhost', 27017)
        db = mongodb.books
        self.collection = db.books
        self.errorCollection = db.errors
    def process_item(self, item, spider):
        try:
            self.collection.insert(item)
        except:
            errData = {'_id':item['_id'], 'ISBN':item['ISBN']}
            self.errorCollection.insert(errData)
        return item
