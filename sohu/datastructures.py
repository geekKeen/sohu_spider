# -*- coding: utf-8 -*-
from .tool import URLTool


class Storage(object):
    """
    URL 的存储类，同时为 URL建立索引, 去重 URL
    _group_dict 根据 url 的 column 划分分组，
    key值为 column，value值为 set，set中存储 address
    """

    def __init__(self):
        self._group_dict = {}

    def add(self, url):
        _url = URLTool(url)
        column = _url.column
        if column not in self._group_dict.keys():
            self._group_dict[column] = set()
        address = _url.address
        self._group_dict[column].add(address)

    def __contains__(self, url):
        _url = URLTool(url)
        column = _url.column
        if column not in self._group_dict.keys():
            return False
        address = _url.address
        if address not in self._group_dict[column]:
            return False
        return True
