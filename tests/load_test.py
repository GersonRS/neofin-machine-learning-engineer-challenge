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


json_test = {
    "company_id": "83 0b f4 f3 45 67 54 39 74 c5 43 31 ae 73 a3 09 23 3e b4 47 5b 47 9d 11 e5 1d e8 c7 90 cb 92 fd",
    "company_name": "40 f9 0d a5 a9 d9 29 33 ac 84 f2 9b 3f 86 b0 05 69 48 dd 6d 83 52 0e d2 8a 80 de 20 8c 49 71 da",
    "company_document": "37 2a 52 fa 18 60 9c 5c 72 47 98 27 bd 58 45 83 11 25 69 3b a0 3f 45 3c d9 9a 60 67 49 bb c1 2e",
    "company_trade_name": "40 f9 0d a5 a9 d9 29 33 ac 84 f2 9b 3f 86 b0 05 69 48 dd 6d 83 52 0e d2 8a 80 de 20 8c 49 71 da",
    "customer_id": "02 60 80 35 3c d3 09 5f be 20 e5 8d ed 3d 2e fe bd f6 ce 88 18 80 6e 71 ef 32 6a 63 f0 22 18 bf",
    "customer_name": "c4 52 91 30 34 b0 96 83 05 98 61 da 5c 3b a1 12 6f 34 07 c0 50 af 1f 29 c0 17 bb 62 e3 bf 9b da",
    "customer_trade_name": "c4 52 91 30 34 b0 96 83 05 98 61 da 5c 3b a1 12 6f 34 07 c0 50 af 1f 29 c0 17 bb 62 e3 bf 9b da",
    "parent_type": "billing",
    "parent_id": "f02f0294-ce57-431c-b008-483d92dce72a",
    "payment_number": "e5 fa 90 b0 7e 55 6e 80 20 06 2b f0 f8 30 cc 55 84 fa eb e1 eb 48 20 76 4b 1a d6 bf ae ae 59 74",
    "issue_date_dte": "2024-12-30",
    "original_due_date_dte": "2025-01-10",
    "due_date_dte": "2025-01-10",
    "paid_at_dte": "2025-01-05",
    "issue_at_tsmp": "2024-12-30 03:04:27.000",
    "original_due_date_tsmp": "2025-01-10 23:59:59.000",
    "due_date_tsmp": "2025-01-10 23:59:59.000",
    "paid_at_tsmp": "2025-01-05 15:04:28.000",
    "payment_method": "generic",
    "payment_status": "paid",
    "paid_amount": 99.5,
    "billing_amount": 99.5,
    "payment_amount": 99.5,
    "installment": "1/1",
    "payment_provider": "",
    "discount_before_payment": 0.0,
    "discount_before_payment_due_date": 0,
    "description": "22 d0 50 cc 66 fb 05 10 a3 12 0e b8 9b a3 8c d2 9c 0b 29 cd 65 77 f0 74 f4 ea cd bb 35 73 12 74",
    "qrcode_number": "",
    "os_code": "e3 b0 c4 42 98 fc 1c 14 9a fb f4 c8 99 6f b9 24 27 ae 41 e4 64 9b 93 4c a4 95 99 1b 78 52 b8 55",
    "os_identifier": "e3 b0 c4 42 98 fc 1c 14 9a fb f4 c8 99 6f b9 24 27 ae 41 e4 64 9b 93 4c a4 95 99 1b 78 52 b8 55",
    "by_mail": True,
    "by_whatsapp": True,
    "fees": 0,
    "fine": 0,
    "paid_at": "2025-01-05 15:04:28.000",
    "paid_method": "generic",
    "manual": "",
    "billing_number": "44 b5 2b 63 14 51 4a 9e be e1 19 c0 39 ad af 26 6e a5 d2 c8 be 1e 70 1d 6f d9 37 9b a6 62 4a 13",
}


class CardPredict(TaskSet):
    @tag("Predictions")
    @task
    def predict(self):
        request_body = json_test
        self.client.post("/v1/customer/predict", json=request_body)

    @tag("Baseline")
    @task
    def health_check(self):
        self.client.get("/")


class CardLoadTest(HttpUser):
    tasks = [CardPredict]
    host = "http://127.0.0.1"
    stop_timeout = 200
    wait_time = between(1, 5)
