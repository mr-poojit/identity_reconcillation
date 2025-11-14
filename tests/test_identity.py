from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_link():
    # create first contact
    r1 = client.post('/identify', json={"email": "lorraine@hillvalley.edu", "phoneNumber": "123456"})
    assert r1.status_code == 200
    data1 = r1.json()["contact"]
    pid = data1["primaryContatctId"]
    assert "lorraine@hillvalley.edu" in data1["emails"]

    # create second with same phone but different email -> should link
    r2 = client.post('/identify', json={"email": "mcfly@hillvalley.edu", "phoneNumber": "123456"})
    assert r2.status_code == 200    
    data2 = r2.json()["contact"]
    assert data2["primaryContatctId"] == pid
    assert set(data2["emails"]) == {"lorraine@hillvalley.edu","mcfly@hillvalley.edu"}