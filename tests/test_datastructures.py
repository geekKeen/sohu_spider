# -*- coding: utf-8 -*-
from unittest import TestCase
from sohu import Storage, URLTool


class DataStructuresTest(TestCase):
    def test_storage(self):
        storage = Storage()

        string = "http://m.sohu.com/column/address/?parameter"
        assert string not in storage
        storage.add(string)
        assert string in storage

        string = "http://m.sohu.com/column/address/"
        assert string in storage
        string = "http://m.sohu.com/column/address1/"
        assert string not in storage
        string = "http://m.sohu.com/column1/address/"
        assert string not in storage
        string = "http://m.sohu.com/column1/address1/"
        assert string not in storage

        string = "http://m.sohu.com/column/address"
        assert string in storage

        string = "http://m.sohu.com/column/"
        assert string not in storage
        storage.add(string)
        string = "http://m.sohu.com/column"
        assert string in storage

        string = "http://m.sohu.com/"
        assert string not in storage
        storage.add(string)
        string = "http://m.sohu.com"
        assert string in storage
