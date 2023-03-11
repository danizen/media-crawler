# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
from typing import Optional


@dataclass
class T457Item:
    status: int
    url: str
    mime_type: str
    length: Optional[int]

    @classmethod
    def load_from(cls, response):
        url = response.url

        # extract content-type and remove charset and other decorators
        mime_type = response.headers['Content-Type'].decode('utf-8')
        pos = mime_type.find(';')
        if pos > -1:
            mime_type = mime_type[0:pos]

        # extract content-length if available
        length = None
        if 'Content-Length' in response.headers:
            length = int(response.headers['Content-Length'].decode('utf-8'))
        return cls(response.status, url, mime_type, length)
