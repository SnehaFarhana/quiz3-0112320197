import pytest
from fastapi.testclient import TestClient
from main import app, books

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset():
    books.clear()
    import main
    main.next_id = 1
    yield

def test_create_book():
    response = client.post("/books", json={
        "title":"Clean Code","author":"Robert Martin","price":29.99
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Clean Code"

def test_delete_book():
    client.post("/books", json={
        "title":"Test","author":"Author","price":9.99})
    response = client.delete("/books/1")
    assert response.status_code == 200
    check = client.get("/books")
    assert len(check.json()) == 0

def test_get_all_books():
    client.post("/books", json={"title":"A","author":"X","price":10.0})
    client.post("/books", json={"title":"B","author":"Y","price":20.0})
    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_update_book():
    client.post("/books", json={"title":"Old","author":"Z","price":10.0})
    response = client.put("/books/1", json={"price": 99.0})
    assert response.status_code == 200
    assert response.json()["price"] == 99.0
    assert response.json()["title"] == "Old"