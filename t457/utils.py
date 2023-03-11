from urllib.parse import (
    parse_qsl,
    urljoin,
    urlsplit, 
    urlunsplit,
)


def normalize_url(site_url, url):
    parts = urlsplit(url)

    # lower case the scheme and the host
    scheme = parts.scheme.lower()
    netloc = parts.netloc.lower()
    
    # TODO: uppercase escape sequences
    
    # TODO: remove default port
    
    # TODO: decode unreserved characters
    
    # TODO: encode non-URI characters
    
    # TODO: encode spaces
    
    # if there is a query string, sort the parameters and values to normalize the URL
    query_string = parts.query
    if query_string:
        query_string = '&'.join(f'{nm}={val}' for nm, val in sorted(parse_qsl(query_string)))
        
    # recombine the URL ignoring any fragment
    rel_uri = urlunsplit((scheme, netloc, parts.path, query_string, ''))

    # and make absolute
    return urljoin(site_url, rel_uri)
