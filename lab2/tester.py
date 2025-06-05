import unittest
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


class TestAllRoutes(unittest.TestCase):
    def test_root(self):
        resp = client.get("/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["message"], "Hello World!")
        self.assertIn("description", data)

    def test_hello(self):
        resp = client.get("/hello", params={"name": "Alice"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["message"], "Hello Alice, how are you?")
        self.assertIn("description", data)

    def test_sum(self):
        resp = client.get("/sum/3/5")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["sum"], "8")
        self.assertIn("description", data)

    def test_wiki_redirect(self):
        resp = client.get("/wiki/Python_(programming_language)", follow_redirects=False)
        self.assertIn(resp.status_code, (302, 307))
        location = resp.headers.get("location", "")
        self.assertTrue(location.startswith("https://en.wikipedia.org/wiki/"))

    def test_weather_default(self):
        resp = client.get("/weather")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["city"], "Boston")
        self.assertIn("weather", data)
        self.assertIn("description", data)

    def test_weather_custom(self):
        resp = client.get("/weather", params={"city": "New York"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["city"], "New York")

    def test_length(self):
        resp = client.get("/length/hello")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["text"], "hello")
        self.assertEqual(data["length"], 5)
        self.assertIn("description", data)

    def test_prime_true(self):
        resp = client.get("/prime/17")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["number"], 17)
        self.assertTrue(data["is_prime"])

    def test_prime_false(self):
        resp = client.get("/prime/18")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["number"], 18)
        self.assertFalse(data["is_prime"])

    def test_register_and_login_and_list_users_cookie(self):
        new_name = "testuser"
        new_pin = 9999
        resp_reg = client.post("/register", json={"name": new_name, "pin": new_pin})
        self.assertEqual(resp_reg.status_code, 200)
        data_reg = resp_reg.json()
        self.assertTrue(data_reg["success"])
        self.assertIn("description", data_reg)

        # Login with that user
        resp_login = client.post("/login", json={"name": new_name, "pin": new_pin})
        self.assertEqual(resp_login.status_code, 200)
        data_login = resp_login.json()
        self.assertTrue(data_login["success"])
        token = data_login["token"]
        self.assertIsInstance(token, str)

        # List users without cookie → should return success=False
        resp_no_cookie = client.get("/users")
        self.assertEqual(resp_no_cookie.status_code, 200)
        data_no_cookie = resp_no_cookie.json()
        self.assertFalse(data_no_cookie["success"])

        # List users with cookie → should return the list
        resp_users = client.get("/users", cookies={"token": token})
        self.assertEqual(resp_users.status_code, 200)
        data_users = resp_users.json()
        self.assertTrue(data_users["success"])
        self.assertIn(new_name, data_users["users"])
        self.assertIn("description", data_users)

    def test_list_users_header(self):
        # First, login as the built‐in user "caua" (pin 28) to get token
        resp_login = client.post("/login", json={"name": "caua", "pin": 28})
        self.assertEqual(resp_login.status_code, 200)
        data_login = resp_login.json()
        self.assertTrue(data_login["success"])
        token = data_login["token"]

        # Call /users-header with wrong token
        resp_wrong = client.get("/users-header", headers={"Authorization": "Bearer wrongtoken"})
        self.assertEqual(resp_wrong.status_code, 200)
        data_wrong = resp_wrong.json()
        self.assertFalse(data_wrong["success"])
        self.assertIsNone(data_wrong["users"])

        # Call /users-header with correct token
        resp_ok = client.get("/users-header", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(resp_ok.status_code, 200)
        data_ok = resp_ok.json()
        self.assertTrue(data_ok["success"])
        self.assertIn("caua", data_ok["users"])
        self.assertIn("description", data_ok)

    def test_header_and_cookie_independence(self):
        # If both cookie and header present but header is wrong, must still fail
        resp_both = client.get(
            "/users-header",
            cookies={"token": "invalid"},
            headers={"Authorization": "Bearer invalid"},
        )
        self.assertEqual(resp_both.status_code, 200)
        data_both = resp_both.json()
        self.assertFalse(data_both["success"])


if __name__ == "__main__":
    unittest.main()

