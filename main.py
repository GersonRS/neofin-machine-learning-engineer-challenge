from __future__ import annotations

import joblib
from pathlib import Path
import pandas as pd
from fastapi import FastAPI

import models.ml.classifier as clf
from routes.home import app_home
from routes.v1.customer_predict import app_customer_predict_v1

PATH_MODELS = Path(Path(__file__).parent, "models")
PATH_DATA = Path(Path(__file__).parent, "data")

app = FastAPI(
    title="Customer ML API",
    description="API para classificar Customer",
    version="1.0",
)


@app.on_event("startup")
async def load_model():
    with open(Path(PATH_MODELS, "customer_classification_pipeline.pkl"), "rb") as f:
        clf.model = joblib.load(f)
    with open(Path(PATH_MODELS, "target_encoder.pkl"), "rb") as f:
        clf.target_encoder = joblib.load(f)

    # Carregar histórico de pagamentos para cálculo de features dinâmicas
    payments_df = pd.read_csv(Path(PATH_DATA, "payments_mle.csv"))

    # Converter colunas de data corretamente antes de fazer cálculos
    payments_df["due_date_dte"] = pd.to_datetime(payments_df["due_date_dte"], errors="coerce")
    payments_df["paid_at_dte"] = pd.to_datetime(payments_df["paid_at_dte"], errors="coerce")
    payments_df["issue_date_dte"] = pd.to_datetime(payments_df["issue_date_dte"], errors="coerce")

    # Garantir que a coluna `delay_days` foi calculada anteriormente
    if "delay_days" not in payments_df.columns:
        payments_df["delay_days"] = (
            payments_df["paid_at_dte"] - payments_df["due_date_dte"]
        ).dt.days
        payments_df["delay_days"] = payments_df["delay_days"].fillna(0)
    clf.payments_df = payments_df.copy()


app.include_router(app_home)
app.include_router(app_customer_predict_v1, prefix="/v1")
