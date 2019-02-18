import unittest
import json
from main import app as tested_app
from models import db as tested_db
from config import TestConfig
from models import Book

tested_app.config.from_object(TestConfig)
# I did not test my delete methods, because I used it to clear up my table, and it works when I need to rerun tests.


class TestBook(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = tested_db
        self.db.drop_all()
        # there seems to be a problem with tearDown method.
        # It does not clear everything out everytime we test, so there's always an error with UNIQUE constraints.
        # Had to manually delete everything with my delete method with Postman and rerun testBook.
        self.db.create_all()
        self.db.session.add(Book(id=1, book_code=12345678, title="Once Upon a Time", author="JK", year=2010,
                                 user_id=1, library_id=1))
        self.db.session.add(Book(id=2, book_code=123, title="Home Alone", author="Dan", year=2010,
                                 user_id=2, library_id=2))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Book.query.delete()
        self.db.session.commit()

    def test_get_all_book(self):
        # send the request and check the response status code
        response = self.app.get("/book")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        book_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(book_list), list)
        self.assertDictEqual(book_list[0], {"id": "1", "book_code": "12345678", "title": "Once Upon a Time",
                                            "author": "JK", "year": "2010", "user_id": "1", "library_id": "1"})
        self.assertDictEqual(book_list[1], {"id": "2", "book_code": "123", "title": "Home Alone",
                                            "author": "Dan", "year": "2010", "user_id": "2", "library_id": "2"})

    def test_get_book_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/book/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        book = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(book, {"id": "1", "book_code": "12345678", "title": "Once Upon a Time",
                                    "author": "JK", "year": "2010", "user_id": "1", "library_id": "1"})

    def test_get_book_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/book/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this book id."})
    #

    def test_put_book_with_new_id(self):
        # send the request and check the response status code
        response = self.app.put("/book", data={"id": 3, "book_code": 12345678, "title": "Once Upon a Time",
                                "author": "JK", "year": "2010", "user_id": 1, "library_id": 1})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "Successfully added book."})

        # check if the DB was updated correctly
        book = Book.query.filter_by(id=3).first()
        self.assertEqual(book.book_code, 12345678)
