from urllib.parse import urljoin, urlsplit, urlunsplit
from w3lib.url import canonicalize_url


def normalize_url(base_url, url):
    url = urljoin(base_url, url)
    return canonicalize_url(url)


def normalize_media_url(base_url, url):
    url = urljoin(base_url, url)
    url = canonicalize_url(url)
    parts = urlsplit(url)
    
    path = parts.path
    return url