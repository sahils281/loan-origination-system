from pydantic import BaseModel

class TopCustomer(BaseModel):
    customer_name: str
    customer_phone: str
    approved_loan_count: int
    total_approved_amount: float
