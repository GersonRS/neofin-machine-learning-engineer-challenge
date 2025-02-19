from __future__ import annotations

from locust import between
from locust import HttpUser
from locust import tag
from locust import task
from locust import TaskSet

"""
Run locus with:
locust -f ./tests/load_test.py
"""


class CardPredict(TaskSet):
    @tag("Predictions")
    @task
    def predict(self):
        request_body = {
            "weight": 1.12,
            "height": 0.53,
            "length": 0.2,
            "seller_id": "magazineluiza",
            "cep": "51240000",
            "width": 0.32,
            "organization": "magazine_luiza",
            "quantity": 1,
            "value": 2599.00,
            "category": "ET",
            "sub_category": "TV4K",
        }
        self.client.post("/free-delivery", json=request_body)

    @tag("Baseline")
    @task
    def health_check(self):
        self.client.get("/")


class CardLoadTest(HttpUser):
    tasks = [CardPredict]
    host = "http://127.0.0.1"
    stop_timeout = 200
    wait_time = between(1, 5)
