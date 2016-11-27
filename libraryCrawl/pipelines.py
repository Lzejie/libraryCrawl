# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class LibrarycrawlPipeline(object):
    def __init__(self):
        self.f = open('/home/lizejie/project/python/spider/libraryCrawl/data/bookInfo.txt', 'ab')

    def process_item(self, item, spider):
        eachData = []
        for each in item.values():
            eachData.append(each.replace('\n', '').replace('\r', ''))
        dataStr = '\n'.join(eachData).encode('utf8')
        self.f.write(dataStr)
        return item
