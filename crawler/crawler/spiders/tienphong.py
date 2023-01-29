import os
import scrapy
from scrapy.linkextractors import LinkExtractor


class TienphongSpider(scrapy.Spider):
    name = 'tienphong'
    allowed_domains = ['tienphong.vn']
    # start_urls = [
    #     'http://tienphong.vn/mien-bac-don-khong-khi-lanh-mua-keo-dai-tu-dem-nay-post1485966.tpo']
    
    start_urls = [
        'https://tienphong.vn/kinh-te/']
    
    file = "/source/tienphong.txt"
    path = os.getcwd()+file
    
    with open(path, "r") as f:
        for line in f.readlines():
            start_urls.append(line.strip())
            # print(line)
    f.close()

    def parse(self, response):
        le = LinkExtractor(
            allow_domains=self.allowed_domains,
            restrict_xpaths='//*[@class="cms-link"]',
        )
        print("ok1111")
        for link in le.extract_links(response):
            print("ok22")
            print(link.url)
            yield scrapy.Request(url=link.url, callback=self.parse_item)
    
        
    def parse_item(self, response):
        title = self.parse_title(response)
        summary = self.parse_summary(response)
        content = self.parse_content(response)
        print(title)
        print(summary)
        print(content)
        
        scraped_info = {
            'title' : title,
            'summary' : summary,
            'content' : content
        }

        # yield or give the scraped info to scrapy
        yield scraped_info

    def parse_title(self, response):
        title = response.xpath('/html/head/title/text()')
        return title.get()

    def parse_summary(self, response):
        # summary = response.xpath('//article/div[1]/div[1]/div[1]/text()')
        summary = response.xpath('//*[@class="article__sapo cms-desc"]/text()')
        return summary.get()

    def parse_content(self, response):
        content = ' '.join([
            ' '.join(
                line.strip()
                for line in p.xpath('.//text()').extract()
                if line.strip()
            )
            # for p in response.xpath('//article/div[1]/div[1]/div[3]/p')
            for p in response.xpath('//*[@class="article__body cms-body"]/p')
        ])

        return content
