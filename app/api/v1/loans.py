from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.loan import LoanCreate, LoanResponse, LoanStatusCountResponse, StatusCount
from app.services.loan_service import LoanService
from app.repositories.loan_repository import LoanRepository
from app.models.loan import ApplicationStatus

router = APIRouter()
loan_service = LoanService()

@router.post("/loans", response_model=LoanResponse, status_code=201)
def create_loan(loan_data: LoanCreate, db: Session = Depends(get_db)):
    return loan_service.create_loan(db, loan_data.dict())

@router.get("/loans/status-count", response_model=LoanStatusCountResponse)
def get_status_count(db: Session = Depends(get_db)):
    counts = LoanRepository.get_status_counts(db)
    status_counts = [StatusCount(status=s, count=c) for s, c in counts]
    total = sum(c for _, c in counts)
    return LoanStatusCountResponse(status_counts=status_counts, total_loans=total)

@router.get("/loans", response_model=list[LoanResponse])
def get_loans_by_status(
    status: ApplicationStatus,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * size
    return LoanRepository.get_loans_by_status(db, status, skip, size)
