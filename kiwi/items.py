# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AuthorInfo(scrapy.Item):
    authorName = scrapy.Field()  # 作者昵称
    authorUrl = scrapy.Field()  # 作者Url

class ReplyItem(scrapy.Item):
    content = scrapy.Field()  # 回复内容
    time = scrapy.Field()  # 发布时间
    author = scrapy.Field() # 回复人(AuthorInfo)

class TopicItem(scrapy.Item):
    title = scrapy.Field() # 帖子标题
    url = scrapy.Field() # 帖子页面Url
    content = scrapy.Field() # 帖子内容
    time = scrapy.Field()  # 发布时间
    author = scrapy.Field() # 发帖人(AuthorInfo)
    reply = scrapy.Field() # 回复列表(ReplyItem list)
    replyCount = scrapy.Field() # 回复条数
