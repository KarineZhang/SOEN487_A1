import unittest
import json
from main import app as tested_app
from models import db as tested_db
from config import TestConfig
from models import Library

tested_app.config.from_object(TestConfig)
# I did not test my delete methods, because I used it to clear up my table, and it works when I need to rerun tests.


class TestLibrary(unittest.TestCase):
    def setUp(self):
        # set up the test DB
        self.db = tested_db
        self.db.drop_all()
        # there seems to be a problem with tearDown method.
        # It does not clear everything out everytime we test, so there's always an error with UNIQUE constraints.
        # Had to manually delete everything with my delete method with Postman and rerun testLibrary.
        self.db.create_all()
        self.db.session.add(Library(id=1, name="Bibliotheque Nationale", address="123 Berri",
                                    telephone="514-123-1234", email="bn@biblio.com"))
        self.db.session.add(Library(id=2, name="Bibliotheque St-Michel", address="1234 St-Michel",
                                    telephone="514-111-4321", email="bsm@biblio.com"))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Library.query.delete()
        self.db.session.commit()

    def test_get_all_library(self):
        # send the request and check the response status code
        response = self.app.get("/library")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        library_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(library_list), list)
        self.assertDictEqual(library_list[0], {"id": "1", "name": "Bibliotheque Nationale", "address": "123 Berri",
                                               "telephone": "514-123-1234", "email": "bn@biblio.com"})
        self.assertDictEqual(library_list[1], {"id": "2", "name": "Bibliotheque St-Michel", "address": "1234 St-Michel",
                                               "telephone": "514-111-4321", "email": "bsm@biblio.com"})

    def test_get_library_with_valid_id(self):
        # send the request and check the response status code
        response = self.app.get("/library/1")
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        library = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(library, {"id": "1", "name": "Bibliotheque Nationale", "address": "123 Berri",
                                       "telephone": "514-123-1234", "email": "bn@biblio.com"})

    def test_get_library_with_invalid_id(self):
        # send the request and check the response status code
        response = self.app.get("/library/1000000")
        self.assertEqual(response.status_code, 404)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Cannot find this library id."})

    def test_put_library_with_new_id(self):
        # send the request and check the response status code
        response = self.app.put("/library", data={"id": 4, "name": "Bibliotheque Nationale", "address": "123 Berri",
                                                  "telephone": "514-123-1234", "email": "bn@biblio.com"})
        self.assertEqual(response.status_code, 200)

        # convert the response data from json and call the asserts
        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 200, "msg": "Successfully added library."})

        # check if the DB was updated correctly
        library = Library.query.filter_by(id=4).first()
        self.assertEqual(library.address, "123 Berri")
