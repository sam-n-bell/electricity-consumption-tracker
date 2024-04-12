import unittest
from unittest import mock

from tests import client


class MyTestCase(unittest.TestCase):
    def test_system(self):
        response = client.get("/system")
        self.assertEqual(response.status_code, 200)

    @mock.patch("routers.system.validate_db_connection")
    def test_db_available(self, mock_val):
        mock_val.return_value = True
        response = client.get("/system/db")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["available"])

    @mock.patch("routers.system.validate_db_connection")
    def test_db_unavailable(self, mock_val):
        mock_val.return_value = False
        response = client.get("/system/db")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["available"])


if __name__ == "__main__":
    unittest.main()
