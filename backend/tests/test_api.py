import pytest
from fastapi.testclient import TestClient

from backend.main import app, _todos


@pytest.fixture(autouse=True)
def reset_store() -> None:
    _todos.clear()
    import backend.main as main

    main._next_id = 1


client = TestClient(app)


def test_get_todos_starts_empty() -> None:
    response = client.get("/todos")

    assert response.status_code == 200
    assert response.json() == []


def test_create_and_list_todos() -> None:
    create_response = client.post("/todos", json={"title": "Buy milk"})

    assert create_response.status_code == 201
    assert create_response.json() == {
        "id": 1,
        "title": "Buy milk",
        "completed": False,
    }

    list_response = client.get("/todos")
    assert list_response.status_code == 200
    assert list_response.json() == [create_response.json()]


def test_get_todo() -> None:
    created = client.post("/todos", json={"title": "Read a book", "completed": True}).json()

    response = client.get(f"/todos/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_update_todo() -> None:
    created = client.post("/todos", json={"title": "Draft plan"}).json()

    response = client.put(
        f"/todos/{created['id']}",
        json={"title": "Finish plan", "completed": True},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": created["id"],
        "title": "Finish plan",
        "completed": True,
    }


def test_delete_todo() -> None:
    created = client.post("/todos", json={"title": "Temporary task"}).json()

    response = client.delete(f"/todos/{created['id']}")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/todos/{created['id']}").status_code == 404


@pytest.mark.parametrize("method", ["get", "put", "delete"])
def test_missing_todo_returns_not_found(method: str) -> None:
    if method == "put":
        response = client.put("/todos/999", json={"title": "Missing"})
    else:
        response = getattr(client, method)("/todos/999")

    assert response.status_code == 404
