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