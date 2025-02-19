from pydantic import BaseModel


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


class CustomerPredictionResponse(BaseModel):
    prediction: str
