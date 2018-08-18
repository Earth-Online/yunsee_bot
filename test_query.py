#!coding:utf-8
#  Created by bluebird on 2018/8/18
from unittest import TestCase
from main import query

test_url = "python.org"


class TestQuery(TestCase):
    def test_query(self):
        self.assertIsNotNone(query(test_url))
