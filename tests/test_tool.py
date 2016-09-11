# -*- coding: utf-8 -*-
from unittest import TestCase
from sohu import URLTool


class URLToolTest(TestCase):
    def test_tool(self):
        url = URLTool("http://m.sohu.com/column/address/?parameter")
        assert url.column == "column" and url.address == "address"

        url = URLTool("http://m.sohu.com/column/address/")
        assert url.column == "column" and url.address == "address"

        url = URLTool("http://m.sohu.com/column/address")
        assert url.column == "column" and url.address == "address"

        url = URLTool("http://m.sohu.com/column/")
        assert url.column == "column" and url.address == ""

        url = URLTool("http://m.sohu.com/column")
        assert url.column == "column" and url.address == ""

        url = URLTool("http://m.sohu.com/")
        assert url.column == "" and url.address == ""

        url = URLTool("http://m.sohu.com")
        assert url.column == "" and url.address == ""
