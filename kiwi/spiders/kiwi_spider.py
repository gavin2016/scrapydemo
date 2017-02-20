# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from kiwi.items import TopicItem, AuthorInfo, ReplyItem
class KiwiSpider(CrawlSpider):
    name = "kiwi"
    allowed_domains = ["douban.com"]

    anchorTitleXPath = 'a/text()'
    anchorHrefXPath = 'a/@href'

    start_urls = [
        "https://www.douban.com/group/topic/90895393/?start=0",
    ]
    rules = (
        Rule(
            LinkExtractor(allow=(r'/group/[^/]+/discussion\?start=\d+',)),
                callback='parse_topic_list',
                follow=True
        ),
        Rule(
            LinkExtractor(allow=(r'/group/topic/\d+/$',)),  # 帖子内容页面
                callback='parse_topic_content',
                follow=True
        ),
        Rule(
            LinkExtractor(allow=(r'/group/topic/\d+/\?start=\d+',)), # 帖子内容页面
                callback='parse_topic_content',
                follow=True
        ),
    )

    # 帖子详情页面
    def parse_topic_content(self, response):
        # 标题XPath
        titleXPath = '//html/head/title/text()'
        # 帖子内容XPath
        contentXPath = '//div[@class="topic-content"]/p/text()'
        # 发帖时间XPath
        timeXPath = '//div[@class="topic-doc"]/h3/span[@class="color-green"]/text()'
        # 发帖人XPath
        authorXPath = '//div[@class="topic-doc"]/h3/span[@class="from"]'

        item = TopicItem()
        # 当前页面Url
        item['url'] = response.url
        # 标题
        titleFragment = Selector(response).xpath(titleXPath)
        item['title'] = str(titleFragment.extract()[0]).strip()

        # 帖子内容
        contentFragment = Selector(response).xpath(contentXPath)
        strs = [line.extract().strip() for line in contentFragment]
        item['content'] = '\n'.join(strs)
        # 发帖时间
        timeFragment = Selector(response).xpath(timeXPath)
        if timeFragment:
            item['time'] = timeFragment[0].extract()

        # 发帖人信息
        authorInfo = AuthorInfo()
        authorFragment = Selector(response).xpath(authorXPath)
        if authorFragment:
            authorInfo['authorName'] = authorFragment[0].xpath(self.anchorTitleXPath).extract()[0]
            authorInfo['authorUrl'] = authorFragment[0].xpath(self.anchorHrefXPath).extract()[0]

        item['author'] = dict(authorInfo)

        # 回复列表XPath
        replyRootXPath = r'//div[@class="reply-doc content"]'
        # 回复时间XPath
        replyTimeXPath = r'div[@class="bg-img-green"]/h4/span[@class="pubtime"]/text()'
        # 回复人XPath
        replyAuthorXPath = r'div[@class="bg-img-green"]/h4'

        replies = []
        itemsFragment = Selector(response).xpath(replyRootXPath)
        for replyItemXPath in itemsFragment:
            replyItem = ReplyItem()
            # 回复内容
            contents = replyItemXPath.xpath('p/text()')
            strs = [line.extract().strip() for line in contents]
            replyItem['content'] = '\n'.join(strs)
            # 回复时间
            timeFragment = replyItemXPath.xpath(replyTimeXPath)
            if timeFragment:
                replyItem['time'] = timeFragment[0].extract()
            # 回复人
            replyAuthorInfo = AuthorInfo()
            authorFragment = replyItemXPath.xpath(replyAuthorXPath)
            if authorFragment:
                replyAuthorInfo['authorName'] = authorFragment[0].xpath(self.anchorTitleXPath).extract()[0]
                replyAuthorInfo['authorUrl'] = authorFragment[0].xpath(self.anchorHrefXPath).extract()[0]

            replyItem['author'] = dict(replyAuthorInfo)
            # 添加进回复列表
            replies.append(dict(replyItem))

        item['reply'] = replies
        yield item

    # 帖子列表页面
    def parse_topic_list(self, response):
        # 帖子列表XPath(跳过表头行)
        topicRootXPath = r'//table[@class="olt"]/tr[position()>1]'
        # 单条帖子条目XPath
        titleXPath = r'td[@class="title"]'
        # 发帖人XPath
        authorXPath = r'td[2]'
        # 回复条数XPath
        replyCountXPath = r'td[3]/text()'
        # 发帖时间XPath
        timeXPath = r'td[@class="time"]/text()'

        topicsPath = Selector(response).xpath(topicRootXPath)
        for topicItemPath in topicsPath:
            item = TopicItem()
            titlePath = topicItemPath.xpath(titleXPath)
            item['title'] = titlePath.xpath(self.anchorTitleXPath).extract()[0]
            item['url'] = titlePath.xpath(self.anchorHrefXPath).extract()[0]
            # 发帖时间
            timePath = topicItemPath.xpath(timeXPath)
            if timePath:
                item['time'] = timePath[0].extract()
                # 发帖人
                authorPath = topicItemPath.xpath(authorXPath)
                authInfo = AuthorInfo()
                authInfo['authorName'] = authorPath[0].xpath(self.anchorTitleXPath).extract()[0]
                authInfo['authorUrl'] = authorPath[0].xpath(self.anchorHrefXPath).extract()[0]
                item['author'] = dict(authInfo)
                # 回复条数
                replyCountPath = topicItemPath.xpath(replyCountXPath)
                item['replyCount'] = replyCountPath[0].extract()

            item['content'] = ''
            yield item

    parse_start_url = parse_topic_content