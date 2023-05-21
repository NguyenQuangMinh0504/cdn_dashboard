def get_domain_slug(url: str):
    """
    Trả về slug của domain dựa trên input url
    """
    if url.startswith("www."):
        url = url.removeprefix("www.")
    return url.split(".")[0]
