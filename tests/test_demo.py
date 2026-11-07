import socket
import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient

from app.demo import app


def test_repository_does_not_import_generation_providers():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; import app.repository; assert 'app.responses' not in sys.modules",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_demo_is_isolated_and_read_only(monkeypatch, tmp_path):
    production = tmp_path / "production.sqlite3"
    production.write_bytes(b"do not touch")
    monkeypatch.setenv("HH_CRM_DB_PATH", str(production))

    def reject_network(*args, **kwargs):
        raise AssertionError("Demo attempted a network connection")

    monkeypatch.setattr(socket.socket, "connect", reject_network)

    with TestClient(app) as client:
        demo_path = Path(app.state.repository.db_path)
        assert demo_path != production
        assert demo_path.exists()
        response = client.get("/api/vacancies")
        assert response.status_code == 200
        vacancies = response.json()
        assert {item["decision"] for item in vacancies} == {"hot", "review", "maybe", "archive"}
        assert all(item["external_id"].startswith("demo-") for item in vacancies)
        assert all(item["score_reasons"] or item["score_penalties"] for item in vacancies)
        assert client.get("/").status_code == 200
        assert client.post("/api/agent/run", json={}).status_code in (404, 405)
        assert client.post("/api/vacancies", json={}).status_code == 405

    assert not demo_path.exists()
    assert production.read_bytes() == b"do not touch"
