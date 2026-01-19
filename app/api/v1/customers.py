from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.customer import TopCustomer
from app.repositories.loan_repository import LoanRepository

router = APIRouter()

@router.get("/customers/top", response_model=list[TopCustomer])
def get_top_customers(db: Session = Depends(get_db)):
    rows = LoanRepository.get_top_customers(db, limit=3)
    return [
        TopCustomer(
            customer_name=name,
            customer_phone=phone,
            approved_loan_count=count,
            total_approved_amount=float(amount or 0),
        )
        for name, phone, count, amount in rows
    ]
