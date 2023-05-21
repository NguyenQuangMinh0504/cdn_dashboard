from urllib.parse import urlparse


def get_domain_slug(url):
    """
    Trả về slug của domain dựa trên input url
    """
    parse_url = urlparse(url=url)
    netloc_parts = parse_url.netloc.split(".")

    print("net loc part is", netloc_parts)

    if len(netloc_parts) > 2:
        return netloc_parts[1]
    return netloc_parts[0]
