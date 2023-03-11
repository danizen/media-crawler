import logging
from functools import cached_property
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit
from scrapy import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import SitemapSpider

from t457.items import T457Item

LOG = logging.getLogger(__name__)


def clean_wixstatic_url(url):
    p = urlsplit(url)
    if p.netloc == 'static.wixstatic.com':
        # process to remove resizing, version, and fillcomponents
        last = p.path.split('/')[-1]
        pos = p.path.find(last)
        if pos > -1:
            path = p.path[0:pos]+last
            url = urlunsplit((
                p.scheme,
                p.netloc,
                path,
                p.query,
                ''
            ))
    return url


class MediaSpider(SitemapSpider):
    name = "media"
    allowed_domains = [
        't457.org',
        'www.t457.org',
        'static.wixstatic.com',
    ]
    download_path = None
    sitemap_urls = [
        'https://www.t457.org/sitemap.xml',
    ]

    @cached_property
    def media_method(self):
        if self.download_path is not None:
            return 'GET'
        else:
            return 'HEAD'
    
    @cached_property
    def anchors(self):
        return LxmlLinkExtractor(
            allow_domains=self.allowed_domains,
            canonicalize=True,
            unique=True
        )
        
    @cached_property
    def media(self):
        return LxmlLinkExtractor(
            allow_domains=self.allowed_domains,
            tags=('img',),
            attrs=('src',), 
            canonicalize=True,
            unique=True,
            deny_extensions=[]
        )

    def parse(self, response):
        item = T457Item.load_from(response)
        yield item

        base_url = response.css('head > base').attrib.get('href', response.url)
        for link in self.anchors.extract_links(response):
            # not sure if scrapy does the urljoin
            LOG.debug('anchor link: %s', link.url)
            url = urljoin(base_url, link.url)
            yield Request(url, self.parse)

        for link in self.media.extract_links(response):
            LOG.debug('media link: %s', link.url)
            url = urljoin(base_url, link.url)
            # link extractor will definitely clean-up the versioning
            url = clean_wixstatic_url(url)
            yield Request(url, self.parse_media, method=self.media_method)
        
    def parse_media(self, response):
        item = T457Item.load_from(response)
        yield item
        
        if self.download_path is not None:
            name = urlsplit(response.url).path.split('/')[-1]
            path = Path(self.download_path) / name
            with path.open('wb') as f:
                f.write(response.body)
            LOG.info('Saved %s', path)

    # closed(self) is called when the spider is closed