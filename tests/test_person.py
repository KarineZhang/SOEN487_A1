import unittest
import json
from main import app as tested_app
from models import db as tested_db
from config import TestConfig
from models import User

tested_app.config.from_object(TestConfig)


class TestUser(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(User(id=1, name="Alice"))
        self.db.session.add(User(id=2, name="Bob"))
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
        self.assertDictEqual(user_list[0], {"id": "1", "name": "Alice"})
        self.assertDictEqual(user_list[1], {"id": "2", "name": "Bob"})

    def test_get_user_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/user/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        user = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(user, {"id": "1", "name": "Alice"})

    def test_get_user_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/user/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this user id."})

    def test_put_user_without_id(self):
        # do we really need to check counts?
        initial_count = User.query.filter_by(name="Amy").count()

        # send the request and check the response status code
        response = self.app.put("/user", data={"name": "Amy"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        updated_count = User.query.filter_by(name="Amy").count()
        self.assertEqual(updated_count, initial_count+1)

    def test_put_user_with_new_id(self):
        # send the request and check the response status code
        response = self.app.put("/user", data={"id": 3, "name": "Amy"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "success"})

        # check if the DB was updated correctly
        user = User.query.filter_by(id=3).first()
        self.assertEqual(user.name, "Amy")
