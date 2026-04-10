from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_full_ticket_lifecycle():
    response = client.post("/api/tickets/", json={
        "client_id": "e2e-user",
        "subject": "Всё сломалось!",
        "priority": "URGENT"
    })
    assert response.status_code == 201
    ticket_id = response.json()["ticket_id"]

    response = client.get(f"/api/tickets/{ticket_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "NEW"

    response = client.post(f"/api/tickets/{ticket_id}/assign-agent", json={
        "agent_id": "agent-007"
    })
    assert response.status_code == 200

    response = client.get(f"/api/tickets/{ticket_id}")
    data = response.json()
    assert data["status"] == "OPEN"
    assert data["assigned_agent_id"] == "agent-007"