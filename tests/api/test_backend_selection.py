from fastapi.testclient import TestClient
from app.main import create_app


def test_explicit_path_keeps_sqlite_when_mysql_selected(monkeypatch, tmp_path):
    monkeypatch.setenv("CARS_DB_BACKEND", "mysql")
    monkeypatch.delenv("MYSQL_USER", raising=False)
    db_path = tmp_path / "explicit.db"
    with TestClient(create_app(db_path)) as client:
        response = client.post("/api/cars", json={"make": "Toyota", "model": "Yaris", "year": 2024})
        assert response.status_code == 201
        assert client.get("/api/cars").json()[0]["id"] == response.json()["id"]
    assert db_path.read_bytes().startswith(b"SQLite format 3")
