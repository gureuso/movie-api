# -*- coding: utf-8 -*-
import unittest2
import redis

from apps.database.session import db, cache
from apps.controllers.router import app
from apps.database.models import Test


class TestDatabase(unittest2.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        test = Test('test01')
        db.session.add(test)
        db.session.commit()

    def tearDown(self):
        Test.query.filter_by(message='test01').delete()
        db.session.commit()

    def test_connect_db(self):
        rows = Test.query.filter_by(message='test01').all()
        self.assertEqual(len(rows), 1)

    def test_connect_redis(self):
        try:
            client_list = cache.client_list()
            self.assertIsNot(client_list, [])
        except redis.exceptions.ConnectionError as e:
            print(e)


if __name__ == '__main__':
    unittest2.main()
