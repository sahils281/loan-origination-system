from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional
from app.models.loan import LoanType, ApplicationStatus

class LoanCreate(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=200)
    customer_phone: str = Field(..., pattern=r'^\+?[1-9]\d{1,14}$')  # E.164 format
    loan_amount: Decimal = Field(..., gt=0, le=10000000)
    loan_type: LoanType

class LoanResponse(BaseModel):
    loan_id: str
    customer_name: str
    customer_phone: str
    loan_amount: Decimal
    loan_type: LoanType
    application_status: ApplicationStatus
    created_at: datetime
    updated_at: Optional[datetime]
    assigned_agent_id: Optional[int]

    class Config:
        from_attributes = True

class AgentDecision(BaseModel):
    decision: str = Field(..., pattern="^(APPROVE|REJECT)$")

class StatusCount(BaseModel):
    status: ApplicationStatus
    count: int

class LoanStatusCountResponse(BaseModel):
    status_counts: list[StatusCount]
    total_loans: int
