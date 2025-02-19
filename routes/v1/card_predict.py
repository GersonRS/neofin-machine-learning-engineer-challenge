from __future__ import annotations

import numpy as np
from fastapi import APIRouter
import pandas as pd
import models.ml.classifier as clf
from models.schemas.customer import PaymentRecord
from models.schemas.customer import CustomerPredictionResponse

app_customer_predict_v1 = APIRouter()

output = {
    0: "Novos Pagadores",
    1: "Pagadores Duvidosos",
    2: "Bons Pagadores",
    3: "Pagadores Esquecidos",
    4: "Maus Pagadores",
}


# Função para converter strings em datetime corretamente
def safe_convert_date(date_str):
    if isinstance(date_str, str) and date_str.strip():
        try:
            return pd.to_datetime(date_str, format="%Y-%m-%d")
        except Exception:
            return None
    return None


# Função para calcular as features utilizadas no treinamento do modelo
def calculate_features(payment: PaymentRecord):
    # Converter datas corretamente
    paid_at_date = safe_convert_date(payment.paid_at_dte)
    due_date = safe_convert_date(payment.due_date_dte)
    issue_date = safe_convert_date(payment.issue_date_dte)

    # Calcular número de dias de atraso no pagamento
    delay_days = (paid_at_date - due_date).days if paid_at_date and due_date else 0

    # Calcular taxa de atraso
    late_rate = 1 if delay_days > 0 else 0

    # Calcular tempo para pagamento
    time_to_pay = (paid_at_date - issue_date).days if paid_at_date and issue_date else 0

    # Garantir que `time_to_pay` existe na tabela principal
    if "time_to_pay" not in clf.payments_df.columns:
        clf.payments_df["time_to_pay"] = (
            clf.payments_df["paid_at_dte"] - clf.payments_df["issue_date_dte"]
        ).dt.days
        clf.payments_df["time_to_pay"] = clf.payments_df["time_to_pay"].fillna(0)

    # Converter colunas de data no histórico de pagamentos
    clf.payments_df["due_date_dte"] = pd.to_datetime(
        clf.payments_df["due_date_dte"], errors="coerce"
    )
    clf.payments_df["paid_at_dte"] = pd.to_datetime(clf.payments_df["paid_at_dte"], errors="coerce")
    clf.payments_df["issue_date_dte"] = pd.to_datetime(
        clf.payments_df["issue_date_dte"], errors="coerce"
    )

    # Recuperar histórico de pagamentos do cliente para cálculo de features
    customer_history = clf.payments_df[clf.payments_df["customer_id"] == payment.customer_id]

    # Calcular total de pagamentos do cliente
    total_payments = (
        customer_history.shape[0] + 1
    )  # Consideramos este pagamento como um novo registro

    # Calcular número de pagamentos atrasados
    late_payments = customer_history["delay_days"].apply(lambda x: 1 if x > 0 else 0).sum()

    # Calcular total de pagamentos do cliente (customer_payment_count)
    customer_payment_count = total_payments

    # Calcular média de atraso do cliente
    avg_delay = customer_history["delay_days"].mean() if not customer_history.empty else delay_days

    # Calcular média de tempo para pagar (avg_time_to_pay)
    avg_time_to_pay = (
        customer_history["time_to_pay"].mean() if not customer_history.empty else time_to_pay
    )

    # Criar vetor de entrada com as features exatas utilizadas no modelo treinado
    features = np.array(
        [
            [
                total_payments,
                late_rate,
                late_payments,
                customer_payment_count,
                avg_delay,
                avg_time_to_pay,
                time_to_pay,
                delay_days,
            ]
        ]
    )

    return features


@app_customer_predict_v1.post(
    "/customer/predict",
    tags=["Predictions"],
    response_model=CustomerPredictionResponse,
    description="Get a classification from customer",
)
async def get_prediction(payment: PaymentRecord):
    try:

        # Calcular as features necessárias para inferência
        features = calculate_features(payment)

        # Fazendo a previsão com o modelo
        prediction_encoded = clf.model.predict(features)

        # Converter de array OneHotEncoded de volta para rótulo original
        predicted_category = clf.target_encoder.inverse_transform([prediction_encoded[0]])[0][0]

        return {
            "prediction": output[predicted_category],
        }

    except Exception as e:
        return {"error": f"Erro ao processar a solicitação: {str(e)}"}
