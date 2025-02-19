from fastapi import FastAPI
import joblib
import pandas as pd
import numpy as np
from pydantic import BaseModel
from datetime import datetime

# Carregando o modelo treinado e o OneHotEncoder
pipeline = joblib.load("./models/customer_classification_pipeline.pkl")
target_encoder = joblib.load("./models/target_encoder.pkl")
output = {
    0: "Novos Pagadores",
    1: "Pagadores Duvidosos",
    2: "Bons Pagadores",
    3: "Pagadores Esquecidos",
    4: "Maus Pagadores",
}

# Carregar histórico de pagamentos para cálculo de features dinâmicas
payments_df = pd.read_csv("./data/payments_mle.csv")

# Converter colunas de data corretamente antes de fazer cálculos
payments_df["due_date_dte"] = pd.to_datetime(payments_df["due_date_dte"], errors="coerce")
payments_df["paid_at_dte"] = pd.to_datetime(payments_df["paid_at_dte"], errors="coerce")
payments_df["issue_date_dte"] = pd.to_datetime(payments_df["issue_date_dte"], errors="coerce")

# Garantir que a coluna `delay_days` foi calculada anteriormente
if "delay_days" not in payments_df.columns:
    payments_df["delay_days"] = (payments_df["paid_at_dte"] - payments_df["due_date_dte"]).dt.days
    payments_df["delay_days"] = payments_df["delay_days"].fillna(0)

# Criando a aplicação FastAPI
app = FastAPI(title="Customer Classification API", version="4.5")


# Definição do schema completo do pagamento
class PaymentRecord(BaseModel):
    company_id: str
    company_name: str
    company_document: str
    company_trade_name: str
    customer_id: str
    customer_name: str
    customer_trade_name: str
    parent_type: str
    parent_id: str
    payment_number: str
    issue_date_dte: str
    original_due_date_dte: str
    due_date_dte: str
    paid_at_dte: str
    issue_at_tsmp: str
    original_due_date_tsmp: str
    due_date_tsmp: str
    paid_at_tsmp: str
    payment_method: str
    payment_status: str
    paid_amount: float
    billing_amount: float
    payment_amount: float
    installment: str
    payment_provider: str
    discount_before_payment: float
    discount_before_payment_due_date: float
    description: str
    qrcode_number: str
    os_code: str
    os_identifier: str
    by_mail: bool
    by_whatsapp: bool
    fees: float
    fine: float
    paid_at: str
    paid_method: str
    manual: str
    billing_number: str


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
    if "time_to_pay" not in payments_df.columns:
        payments_df["time_to_pay"] = (
            payments_df["paid_at_dte"] - payments_df["issue_date_dte"]
        ).dt.days
        payments_df["time_to_pay"] = payments_df["time_to_pay"].fillna(0)

    # Converter colunas de data no histórico de pagamentos
    payments_df["due_date_dte"] = pd.to_datetime(payments_df["due_date_dte"], errors="coerce")
    payments_df["paid_at_dte"] = pd.to_datetime(payments_df["paid_at_dte"], errors="coerce")
    payments_df["issue_date_dte"] = pd.to_datetime(payments_df["issue_date_dte"], errors="coerce")

    # Recuperar histórico de pagamentos do cliente para cálculo de features
    customer_history = payments_df[payments_df["customer_id"] == payment.customer_id]

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


# Endpoint para classificar um cliente com base nos dados de um pagamento
@app.post("/classify_payment/")
def classify_payment(payment: PaymentRecord):
    try:

        # Calcular as features necessárias para inferência
        features = calculate_features(payment)

        # Fazendo a previsão com o modelo
        prediction_encoded = pipeline.predict(features)

        # Converter de array OneHotEncoded de volta para rótulo original
        predicted_category = target_encoder.inverse_transform([prediction_encoded[0]])[0][0]

        return {
            "prediction": output[predicted_category],
        }

    except Exception as e:
        return {"error": f"Erro ao processar a solicitação: {str(e)}"}


# Rota para verificar se a API está rodando
@app.get("/")
def root():
    return {
        "message": "API de Classificação de Clientes está funcionando corretamente com conversão de datas corrigida!"
    }
