import unittest
import json
from main import app as tested_app
from models import db as tested_db
from config import TestConfig
from models import User

tested_app.config.from_object(TestConfig)

# I did not test my delete methods, because I used it to clear up my table, and it works when I need to rerun tests.


class TestUser(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = tested_db
        self.db.drop_all()
        # there seems to be a problem with tearDown method.
        # It does not clear everything out everytime we test, so there's always an error with UNIQUE constraints.
        # Had to manually delete everything with my delete method with Postman and rerun testUser.
        self.db.create_all()
        self.db.session.add(User(id=1, name="Karine", card=123, address="123 Street", telephone="514-111-1111",
                                 dob="12-12-2000", limit_books=4, email="karine@hotmail.com"))
        self.db.session.add(User(id=2, name="Bob", card=456, address="456 Street", telephone="514-466-1111",
                                 dob="10-10-1991", limit_books=3, email="bob@hotmail.com"))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        User.query.delete()
        self.db.session.commit()

    def test_get_all_user(self):
        # send the request and check the response status code
        response = self.app.get("/user")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        user_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(user_list), list)
        self.assertDictEqual(user_list[0], {"id": "1", "name": "Karine", "card": "123", "address": "123 Street",
                                            "telephone": "514-111-1111", "dob": "12-12-2000", "limit_books": "4",
                                            "email": "karine@hotmail.com"})
        self.assertDictEqual(user_list[1], {"id": "2", "name": "Bob", "card": "456", "address": "456 Street",
                                            "telephone": "514-466-1111", "dob": "10-10-1991", "limit_books": "3",
                                            "email": "bob@hotmail.com"})

    def test_get_user_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/user/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        user = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(user, {"id": "1", "name": "Karine", "card": "123", "address": "123 Street",
                                    "telephone": "514-111-1111", "dob": "12-12-2000", "limit_books": "4",
                                    "email": "karine@hotmail.com"})

    def test_get_user_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/user/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this user id."})

    # this test won't work
    # def test_put_user_without_id(self):
    #     response = self.app.post("/user", data={"id": 1, "name": "Karine", "card": 123, "address": "123 Street",
    #                                                      "telephone": "514-111-1111", "dob": "12-12-2000",
    #                                                      "limit_books": 4, "email": "karine@hotmail.com"})
    #     self.assertEqual(response.status_code, 200)
    #
    #     # convert the response data from json and call the asserts
    #     body = json.loads(str(response.data, "utf8"))
    #     self.assertDictEqual(body, {"code": 200, "msg": "success"})
    #
    #     # check if the DB was updated correctly
    #     updated_count = User.query.filter_by(name="Karine").count()
    #     self.assertEqual(updated_count, 1)

    def test_put_user_with_new_id(self):
        # send the request and check the response status code
        response = self.app.put("/user", data={"id": 3, "name": "Karine", "card": 123, "address": "123 Street",
                                               "telephone": "514-111-1111", "dob": "12-12-2000",
                                               "limit_books": 4, "email": "karine@hotmail.com"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "Successfully added user."})

        # check if the DB was updated correctly
        user = User.query.filter_by(id=3).first()
        self.assertEqual(user.name, "Karine")
