import scrapy
from scrapy.crawler import CrawlerProcess

class SpiderClassName(scrapy.Spider):
    name = "dc_spider"
    # Code for your spider
    def start_requests(self):
        urls = ['https://www.datacamp.com/courses-all']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse_front(self, response):
        course_blocks = response.css('div.course-block')
        course_links = course_blocks.xpath('./a/@href')
        links_to_follow = course_links.extract()
        for url in links_to_follow:
            yield response.follow(url=url, callback=self.parse_pages)
    
    def parse_pages(self, response):
        # Direct to the course title text
        crs_title = response.xpath('//h1[contains(@class, "title")]/text()')
        # Extract and clean the course title text
        crs_title_ext = crs_title.extract_first().strip()
        # Directo to the chapter title text
        ch_titles = response.css('h4.chapter__title::text')
        # Extract and clean the chapter title text
        ch_titles_ext = [t.strip() for t in ch_titles.extract()]
        dc_dict[crs_title_ext] = ch_titles_ext
process = CrawlerProcess()
process.crawl(SpiderClassName)
process.start()