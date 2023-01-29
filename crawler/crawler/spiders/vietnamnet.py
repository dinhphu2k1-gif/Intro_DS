import os
import scrapy
from scrapy.linkextractors import LinkExtractor


class TienphongSpider(scrapy.Spider):
    name = 'vietnamnet'
    allowed_domains = ['vietnamnet.vn']
    # start_urls = [
    #     'http://tienphong.vn/mien-bac-don-khong-khi-lanh-mua-keo-dai-tu-dem-nay-post1485966.tpo']
    
    start_urls = [
        'https://vietnamnet.vn/benh-nhan-duoc-chua-khoi-ung-thu-ngay-trong-ngay-phat-hien-benh-2084638.html']
    file = "/source/vietnamnet.txt"
    path = os.getcwd()+file
    with open(path, "r") as f:
        for line in f.readlines():
            link = line.strip()
            start_urls.append(link)
            for i in range(1, 20):
                start_urls.append(link + "-page" + str(i))
    f.close()

    def parse(self, response):
        le = LinkExtractor(
            allow_domains=self.allowed_domains,
            restrict_xpaths='//h3[contains(@class, "vnn-title")]/a',
        )
        for link in le.extract_links(response):
            print(link.url)
            yield scrapy.Request(url=link.url, callback=self.parse_item)
    
        
    def parse_item(self, response):
        title = ' '.join(self.parse_title(response).split())
        summary = ' '.join(self.parse_summary(response).split())
        content = ' '.join(self.parse_content(response).split())
        time = ' '.join(self.parse_time(response).split())
        topic = ' '.join(self.parse_topic(response).split())
        # print(title)
        # print(summary)
        # print(content)
        
        if title == None or summary == None or content == "":
            return
        scraped_info = {
            'title' : title,
            'summary' : summary,
            'content' : content,
            'time': time,
            'topic': topic
        }

        # yield or give the scraped info to scrapy
        yield scraped_info

    def parse_time(self, response):
        time = response.xpath('//*[contains(@class,"breadcrumb-box__time")]/p/span/text()')
        return time.get()

    def parse_title(self, response):
        title = response.xpath('//*[contains(@class,"newsFeature__header-title")]/text()')
        return title.get()

    def parse_summary(self, response):
        # summary = response.xpath('//article/div[1]/div[1]/div[1]/text()')
        summary = response.xpath('//*[contains(@class,"newFeature__main-textBold")]/text()')
        return summary.get()
    def parse_topic(self, response):
        topic = response.xpath('//*[contains(@class,"breadcrumb-box__link ")]/p/a/text()')
        return topic.get()

    def parse_content(self, response):
        content = ' '.join([
            ' '.join(
                line.strip()
                for line in p.xpath('.//text()').extract()
                if line.strip()
            )
            # for p in response.xpath('//article/div[1]/div[1]/div[3]/p')
            for p in response.xpath('//*[contains(@class, "maincontent")]/div/p')
        ])

        return content
