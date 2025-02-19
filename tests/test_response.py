from __future__ import annotations

from fastapi.testclient import TestClient

from main import app


def test_success_prediction():
    endpoint = "/v1/card/predict"
    body = {"id": 1118}

    with TestClient(app) as client:
        response = client.post(endpoint, json=body)
        response_json = response.json()
        assert response.status_code == 200
        assert "prediction" in response_json


def test_bad_request():
    endpoint = "/v1/card/predict"
    body = {"id": "asd"}

    with TestClient(app) as client:
        response = client.post(endpoint, json=body)
        assert response.status_code == 422


def test_id_not_found():
    endpoint = "/v1/card/predict"
    body = {"id": 0}

    with TestClient(app) as client:
        response = client.post(endpoint, json=body)
        assert response.status_code == 404
