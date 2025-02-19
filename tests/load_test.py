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
        request_body = {"id": 1234}
        self.client.post("/v1/card/predict", json=request_body)

    @tag("Baseline")
    @task
    def health_check(self):
        self.client.get("/")


class CardLoadTest(HttpUser):
    tasks = [CardPredict]
    host = "http://127.0.0.1"
    stop_timeout = 200
    wait_time = between(1, 5)
