import pytest
import requests

BASE_URL = "http://localhost:8000"

def test_crud_operations():
    # Create
    response = requests.post(f"{BASE_URL}/items", 
                           json={"name": "test", "description": "test"})
    assert response.status_code == 201
    item_id = response.json()["id"]

    # Read
    response = requests.get(f"{BASE_URL}/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "test"

    # Update
    response = requests.put(f"{BASE_URL}/items/{item_id}", 
                          json={"name": "updated", "description": "updated"})
    assert response.status_code == 200
    assert response.json()["name"] == "updated"

    # Delete
    response = requests.delete(f"{BASE_URL}/items/{item_id}")
    assert response.status_code == 200