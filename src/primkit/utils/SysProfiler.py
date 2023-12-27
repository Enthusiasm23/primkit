import platform
from fake_useragent import UserAgent
from urllib.parse import urlparse
from ..config import BROWSER, MFE_PRIMER


def get_system_type():
    return platform.system().lower()


def get_headers():
    ua = UserAgent(browsers=BROWSER, os=get_system_type())
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Referer': MFE_PRIMER,
        'User-Agent': ua.random
    }
    return headers


def get_user_agent():
    ua = UserAgent(browsers=BROWSER, os=get_system_type())
    headers = {
        'User-Agent': ua.random
    }
    return headers


def is_url(s):
    try:
        result = urlparse(s)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
