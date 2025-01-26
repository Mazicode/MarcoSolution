from starlette.testclient import TestClient

from app.main import app
from app.routes import blacklist, fibonacci_cache

client = TestClient(app)


def test_get_fibonacci_number():
    blacklist.clear()
    fibonacci_cache.clear()

    response = client.get("/fibonacci/5")
    assert response.status_code == 200
    assert response.json() == {"number": 5, "fibonacci": 5}

    response = client.get("/fibonacci/10")
    assert response.status_code == 200
    assert response.json() == {"number": 10, "fibonacci": 55}

    assert 10 in fibonacci_cache
    response = client.get("/fibonacci/10")
    assert response.status_code == 200
    assert response.json() == {"number": 10, "fibonacci": 55}

    response = client.get("/fibonacci/0")
    assert response.status_code == 422
    assert response.json() == {"detail": "Fibonacci number must be a positive integer."}

    response = client.get("/fibonacci/-3")
    assert response.status_code == 422
    assert response.json() == {"detail": "Fibonacci number must be a positive integer."}

    blacklist.add(5)
    response = client.get("/fibonacci/5")
    assert response.status_code == 400
    assert response.json() == {"detail": "Number is blacklisted."}
    blacklist.remove(5)

    blacklist.add(10)
    response = client.get("/fibonacci/10")
    assert response.status_code == 400
    assert response.json() == {"detail": "Number is blacklisted."}
    assert 10 in fibonacci_cache

    blacklist.clear()
    fibonacci_cache.clear()


def test_blacklist_number():
    response = client.post("/blacklist", json={"number": 123})
    assert response.status_code == 200
    assert response.json() == {"message": "Number 123 has been blacklisted."}


def test_blacklist_invalid_number():
    response = client.post("/blacklist", json={"number": -1})
    assert response.status_code == 422
    assert response.json() == {"detail": "Only positive integers can be blacklisted."}


def test_remove_from_blacklist():
    response = client.delete("/blacklist", json={"number": 123})
    assert response.status_code == 200
    assert response.json() == {"message": "Number 123 has been removed from the blacklist."}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
