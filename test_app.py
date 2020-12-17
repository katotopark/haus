import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from api import app
from models import setup_db, Inhabitant, Inquiry
from config import bearer_tokens, database_setup

superintendent_auth_header = {"Authorization": bearer_tokens["superintendent"]}
inhabitant_auth_header = {"Authorization": bearer_tokens["inhabitant"]}


class HausTestCase(unittest.TestCase):
    """This class represents the haus test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_path = os.environ.get(
            "DATABASE_URL",
            "postgresql://{}/{}".format(
                database_setup["port"], database_setup["database_name_production"]
            ),
        )
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_inhabitants(self):
        res = self.client().get("/inhabitants", headers=superintendent_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["inhabitants"])
        self.assertEqual(len(data["inhabitants"]), data["total_count"])

    def test_401_get_inhabitants_with_invalid_permissions(self):
        res = self.client().get("/inhabitants", headers=inhabitant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], "invalid_permissions")
        self.assertTrue(data["description"])

    def test_get_inquiries(self):
        res = self.client().get("/inquiries", headers=inhabitant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["inquiries"])

    def test_401_get_inquiries_without_auth_header(self):
        res = self.client().get("/inquiries", headers={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], "no_authorization_header")
        self.assertTrue(data["description"])

    def test_post_inquiry(self):
        previous_inquiries = Inquiry.query.all()
        new_inquiry = {"inquirer_id": 1, "items": "some items", "tag": "some tag"}
        res = self.client().post(
            "/inquiries", headers=inhabitant_auth_header, json=new_inquiry
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_count"], len(previous_inquiries) + 1)

    def test_400_post_inquiry_without_body(self):
        res = self.client().post("/inquiries", headers=inhabitant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_401_post_inquiry_with_invalid_permissions(self):
        new_inquiry = {"inquirer_id": 1, "items": "some items", "tag": "some tag"}
        res = self.client().post(
            "/inquiries", headers=superintendent_auth_header, json=new_inquiry
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], "invalid_permissions")
        self.assertTrue(data["description"])

    def test_patch_inquiry_status(self):
        current_inquiries = Inquiry.query.all()
        inquiry_id = current_inquiries[-1].id
        res = self.client().patch(
            f"/inquiries/{inquiry_id}", headers=inhabitant_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["inquiry"])

    def test_404_patch_inquiry_status_with_invalid_id(self):
        res = self.client().patch("/inquiries/100", headers=inhabitant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_405_patch_inquiry_status_without_id(self):
        res = self.client().patch("/inquiries", headers=inhabitant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_delete_inquiry_with_id(self):
        current_inquiries = Inquiry.query.all()
        inquiry_id = current_inquiries[-1].id
        res = self.client().delete(
            f"/inquiries/{inquiry_id}", headers=inhabitant_auth_header
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["inquiries"]), data["total_count"])

    def test_404_delete_inquiry_with_invalid_id(self):
        res = self.client().delete("/inquiries/100", headers=inhabitant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_405_delete_inquiry_without_id(self):
        res = self.client().delete("/inquiries", headers=inhabitant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()