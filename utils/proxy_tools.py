from urllib.parse import urlparse


def url_to_dict(proxy_url: str) -> dict:
    parsed = urlparse(proxy_url)

    result = {
        "proxy_type": parsed.scheme,
        "addr": parsed.hostname,
        "port": parsed.port,
    }

    if parsed.username:
        result["username"] = parsed.username

    if parsed.password:
        result["password"] = parsed.password

    return result