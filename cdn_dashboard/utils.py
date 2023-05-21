from urllib.parse import urlparse


def get_domain_slug(url):
    """
    Trả về slug của domain dựa trên input url
    """
    print("Url is: ", url)
    parse_url = urlparse(url=url)
    print("Net loc is", parse_url.netloc)
    netloc_parts = parse_url.netloc.split(".")

    if len(netloc_parts) > 2:
        return netloc_parts[1]
    return netloc_parts[0]
