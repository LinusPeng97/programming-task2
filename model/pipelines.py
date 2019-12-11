# -*- coding: utf-8 -*-
import csv

class ModelPipeline(object):

    def process_item(self, item, spider):
        f = open('issusInfo.csv', 'a+', encoding='utf-8-sig')
        writer = csv.writer(f)
        writer.writerow((item['Type'], item['Assignee'], item['Created'], item['Created_Epoch'], item['Description'], item['Comments']))
        return item


    def close_spider(self, spider):
        self.filename.close()
