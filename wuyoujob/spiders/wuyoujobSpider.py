# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import Spider
from wuyoujob.items import WuyoujobItem


class jobSpider(Spider):
    name = 'wuyoujob'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 LBBROWSER',
        'Accept': 'text/css,*/*;q=0.1',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Referer': 'close',
        'Host': 'js.51jobcdn.com'};

    def start_requests(self):
        url1 = 'http://search.51job.com/list/000000,000000,0000,00,9,99,%25E4%25BA%25A4%25E4%25BA%2592%25E8%25AE%25BE%25E8%25AE%25A1%25E5%25B8%2588,2,'
        url2 = '.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        url = url1 + '1' + url2
        yield Request(url=url, headers=self.headers)

    def parse(self, response):
        for i in range(1, 43):
            url1 = 'http://search.51job.com/list/000000,000000,0000,00,9,99,%25E4%25BA%25A4%25E4%25BA%2592%25E8%25AE%25BE%25E8%25AE%25A1%25E5%25B8%2588,2,'
            url2 = '.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
            next_url = url1 + str(i) + url2
            #print next_url
            yield Request(next_url, headers=self.headers, callback=self.parse_page)

    def parse_page(self, response):
        item = WuyoujobItem()
        jobs = response.xpath('//div[@class="dw_table"]/div[@class="el"]')
        for job in jobs:
            item['companyname'] = job.xpath('span[@class="t2"]/a[@target="_blank"]/text()').extract()[0]
            item['workingplace'] = job.xpath('span[@class="t3"]/text()').extract()[0]
            item['salary'] = job.xpath('span[@class="t4"]/text()').extract()[0]
            item['posttime'] = job.xpath('span[@class="t5"]/text()').extract()[0]
            item['jobname'] = job.xpath('p[@class="t1 "]/span/a[@target="_blank"]/text()').extract()[0]
            yield item