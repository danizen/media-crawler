from scrapy import Request
from scrapy.spiders import SitemapSpider
from t457.utils import normalize_url
from t457.items import T457Item


class MediaSpider(SitemapSpider):
    name = "media"
    allowed_domains = [
        't457.org',
        'www.t457.org',
        'static.wixstatic.com',
    ]
    sitemap_urls = [
        'https://www.t457.org/sitemap.xml',
    ]

    def start_requests(self):
        return super().start_requests()

    def parse(self, response):
        base_url = response.css('head > base').attrib.get('href', response.url)

        for selector in response.css('a'):
            url = selector.attrib.get('href')
            if url is not None and 'javascript:' not in url:
                norm_url = normalize_url(base_url, url)
                yield Request(norm_url, self.parse)
                
        for selector in response.css('img'):
            url = selector.attrib.get('src')
            if url is not None and 'javascript:' not in url:
                norm_url = normalize_url(base_url, url)
                yield Request(norm_url, self.parse_media, method='HEAD')
        
    def parse_media(self, response):
        item = T457Item.load_from(response)
        yield item

    # closed(self) is called when the spider is closed