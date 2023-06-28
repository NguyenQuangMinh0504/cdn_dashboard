def get_domain_slug(url: str):
    """
    Trả về slug của domain dựa trên input url
    """
    if url.startswith("www."):
        url = url.removeprefix("www.")
    return url.split(".")[0]


def get_domain_cdn(url: str):
    """
    Trả về domain cdn của domain
    """
    domain_cdn = get_domain_slug(url=url) + ".sapphirecdn.com"
    return domain_cdn
