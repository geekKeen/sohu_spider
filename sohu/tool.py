# -*- coding: utf-8 -*-
import re
import logging
from functools import wraps
from urllib2 import (HTTPError, URLError,
                     Request, urlopen)


logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s:%(message)s"
)

log_func = {
    logging.CRITICAL: logging.critical,
    logging.ERROR: logging.error,
    logging.DEBUG: logging.debug,
    logging.INFO: logging.info
}


def logger(logger_level):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log_func[logger_level](
                "{func_name} done".format(func_name=func.func_name)
            )
            return func(*args, **kwargs)

        return wrapper

    return decorate


class URLTool(object):
    """
    url 处理工具
    例如：
    http://m.sohu.com/c/5/?parameter "c" 是 column; "5" 为 address
    http://m.sohu.com/help  "help"是 column, "" 为 address
    http://m.sohu.com/     "" 是column, ""为address
    """
    COLUMN_POSITION = 3
    ADDRESS_POSITION = 4
    URL_FORMAT = r'<a href="(.*?)".*?>'
    HOST = "http://m.sohu.com"

    def __init__(self, url):
        self.url = url
        self.url_segment = url.split("/", 6)
        self.url_segment.extend([""] * (6 - len(self.url_segment)))

    @property
    def column(self):
        return self.url_segment[self.COLUMN_POSITION]

    @property
    def address(self):
        return self.url_segment[self.ADDRESS_POSITION]

    # @logger(logging.DEBUG)
    def open(self):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) ' \
                     'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/49.0.2623.87 Safari/537.36'
        headers = {"user_agent": user_agent, "Connection": "keep-alive"}
        response = None
        request = Request(self.url, headers=headers)
        try:
            response = urlopen(request, timeout=3)
        except HTTPError as e:
            logging.warning(
                "{code} {reason} {url}".format(code=e.code, reason=e.reason, url=self.url)
            )
        except URLError as e:
            logging.warning(
                "{reason} {url}".format(reason="URLError", url=self.url)
            )
        finally:
            return "" if response is None \
                else response.read()

    def matched_urls(self, page):
        a_tags = re.finditer(self.URL_FORMAT, page)
        for a_tag in a_tags:
            url = a_tag.group(1)
            if url.startswith(self.HOST):
                yield url
            elif url.startswith("/") and not url.startswith("//"):
                yield self.HOST + url
