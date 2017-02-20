# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from datetime import  datetime
from selenium import webdriver
from fundequity import FundEquity

class PageSpider(object):
    def __init__(self):
        phantomjsPath = "/Library/Frameworks/Python.framework/Versions/3.5/phantomjs/bin/phantomjs"
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        cap["phantomjs.page.settings.loadImages"] = False
        cap["phantomjs.page.settings.disk-cache"] = False
        self.driver = webdriver.PhantomJS(executable_path=phantomjsPath, desired_capabilities=cap)

    def fetchPage(self, url):
        self.driver.get(url)
        html = self.driver.page_source
        return html

    def parse(self, html):
        fundListXPath = r'//div[@id="maininfo_all"]/table[@id="ilist"]/tbody/tr[position()>1]'
        itemsFragment = Selector(text=html).xpath(fundListXPath)
        for itemXPath in itemsFragment:
            attrXPath = itemXPath.xpath(r'td[1]/text()')
            text = attrXPath[0].extract().strip()
            if text != "-":
                fe = FundEquity()
                fe.serial = text

                attrXPath = itemXPath.xpath(r'td[2]/text()')
                text = attrXPath[0].extract().strip()
                fe.date = datetime.strptime(text, "%Y-%m-%d")

                attrXPath = itemXPath.xpath(r'td[3]/text()')
                text = attrXPath[0].extract().strip()
                fe.code = text

                attrXPath = itemXPath.xpath(r'td[4]/a/text()')
                text = attrXPath[0].extract().strip()
                fe.name = text

                attrXPath = itemXPath.xpath(r'td[5]/text()')
                text = attrXPath[0].extract().strip()
                fe.equity = text

                attrXPath = itemXPath.xpath(r'td[6]/text()')
                text = attrXPath[0].extract().strip()
                fe.accumulationEquity = text

                attrXPath = itemXPath.xpath(r'td[7]/font/text()')
                text = attrXPath[0].extract().strip()
                fe.increment = text

                attrXPath = itemXPath.xpath(r'td[8]/font/text()')
                text = attrXPath[0].extract().strip().strip('%')
                fe.growthRate = text

                attrXPath = itemXPath.xpath(r'td[9]/a/text()')
                if len(attrXPath) > 0:
                    text = attrXPath[0].extract().strip()
                    if text == "购买":
                        fe.canBuy = True
                    else:
                        fe.canBuy = False

                attrXPath = itemXPath.xpath(r'td[10]/font/text()')
                if len(attrXPath) > 0:
                    text = attrXPath[0].extract().strip()
                    if text == "赎回":
                        fe.canRedeem = True
                    else:
                        fe.canRedeem = False

                yield fe

    def __del__(self):
        self.driver.quit()

def test():
    spider = PageSpider()
    html = spider.fetchPage("http://www.kjj.com/index_kfjj.html")
    for item in spider.parse(html):
        print(item)
    del spider

if __name__ == "__main__":
    test()