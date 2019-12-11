# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ModelItem(scrapy.Item):

    Type = scrapy.Field()

    Assignee = scrapy.Field()

    Created = scrapy.Field()

    Created_Epoch = scrapy.Field()

    Description = scrapy.Field()

    Comments = scrapy.Field()

    pass

