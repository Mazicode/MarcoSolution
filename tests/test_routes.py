from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestGetFibonacciNumber:
    def test_valid_number(self):
        response = client.get("/fibonacci/10")
        assert response.status_code == 200
        assert response.json() == {"number": 10, "fibonacci": 55}

    def test_blacklisted_number(self):
        client.post("/blacklist", json={"number": 10})
        response = client.get("/fibonacci/10")
        assert response.status_code == 400
        assert response.json()["detail"] == "Number is blacklisted."
        client.request(method="DELETE", url="/blacklist", json={"number": 10})

    def test_negative_number(self):
        response = client.get("/fibonacci/-5")
        assert response.status_code == 422

    def test_non_integer_input(self):
        response = client.get("/fibonacci/abc")
        assert response.status_code == 422

    def test_large_number(self):
        response = client.get("/fibonacci/50")
        assert response.status_code == 200
        assert response.json()["fibonacci"] == 12586269025  # Validate for a large Fibonacci number


class TestGetFibonacciList:
    def test_get_fibonacci_list(self):
        response = client.get("/fibonacci?n=10&page=1&page_size=5")
        assert response.status_code == 200
        assert "numbers" in response.json()
        assert len(response.json()["numbers"]) == 5

    def test_get_fibonacci_list_with_blacklist(self):
        client.post("/blacklist", json={"number": 5})
        response = client.get("/fibonacci?n=10&page=1&page_size=5")
        assert response.status_code == 200
        numbers = [item["number"] for item in response.json()["numbers"]]
        assert 5 not in numbers
        client.request(method="DELETE", url="/blacklist", json={"number": 5})

    def test_pagination_with_large_list(self):
        response = client.get("/fibonacci?n=100&page=2&page_size=20")
        assert response.status_code == 200
        assert len(response.json()["numbers"]) == 20
        assert response.json()["numbers"][0]["number"] == 21

    def test_invalid_pagination_parameters(self):
        response = client.get("/fibonacci?n=10&page=0&page_size=5")
        assert response.status_code == 422

        response = client.get("/fibonacci?n=10&page=1&page_size=0")
        assert response.status_code == 422

    def test_no_numbers_to_display(self):
        client.post("/blacklist", json={"number": 1})
        client.post("/blacklist", json={"number": 2})
        client.post("/blacklist", json={"number": 3})
        response = client.get("/fibonacci?n=3&page=1&page_size=5")
        assert response.status_code == 200
        assert len(response.json()["numbers"]) == 0  # All numbers are blacklisted
        client.request(method="DELETE", url="/blacklist", json={"number": 1})
        client.request(method="DELETE", url="/blacklist", json={"number": 2})
        client.request(method="DELETE", url="/blacklist", json={"number": 3})


class TestBlacklistNumber:
    def test_blacklist_number(self):
        response = client.post("/blacklist", json={"number": 10})
        assert response.status_code == 200
        assert response.json()["message"] == "Number 10 has been blacklisted."

    def test_blacklist_existing_number(self):
        client.post("/blacklist", json={"number": 15})
        response = client.post("/blacklist", json={"number": 15})
        assert response.status_code == 200  # Redis will not throw an error for duplicate values
        assert response.json()["message"] == "Number 15 has been blacklisted."
        client.request(method="DELETE", url="/blacklist", json={"number": 15})

    def test_blacklist_invalid_number(self):
        response = client.post("/blacklist", json={"number": "abc"})
        assert response.status_code == 422  # Input validation should fail

    def test_blacklist_negative_number(self):
        response = client.post("/blacklist", json={"number": -5})
        assert response.status_code == 200  # Redis allows blacklisting negative numbers
        assert response.json()["message"] == "Number -5 has been blacklisted."
        client.request(method="DELETE", url="/blacklist", json={"number": -5})


class TestRemoveFromBlacklist:
    def test_remove_from_blacklist(self):
        client.post("/blacklist", json={"number": 10})
        response = client.request(method="DELETE", url="/blacklist", json={"number": 10})
        assert response.status_code == 200
        assert response.json()["message"] == "Number 10 has been removed from the blacklist."

    def test_remove_nonexistent_blacklist_number(self):
        response = client.request(method="DELETE", url="/blacklist", json={"number": 999})
        assert response.status_code == 200  # Redis will not throw an error for removing a non-existent value
        assert response.json()["message"] == "Number 999 has been removed from the blacklist."

    def test_remove_invalid_number(self):
        response = client.request(method="DELETE", url="/blacklist", json={"number": "abc"})
        assert response.status_code == 422  # Input validation should fail

    def test_remove_negative_number(self):
        client.post("/blacklist", json={"number": -10})
        response = client.request(method="DELETE", url="/blacklist", json={"number": -10})
        assert response.status_code == 200
        assert response.json()["message"] == "Number -10 has been removed from the blacklist."
