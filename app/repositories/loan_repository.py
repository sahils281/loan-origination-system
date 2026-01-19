from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.models.loan import Loan, ApplicationStatus
from typing import Optional, List
import threading

_lock = threading.Lock()

class LoanRepository:
    @staticmethod
    def create_loan(db: Session, loan: Loan) -> Loan:
        with _lock:
            db.add(loan)
            db.commit()
            db.refresh(loan)
            return loan

    @staticmethod
    def get_loan_by_id(db: Session, loan_id: str) -> Optional[Loan]:
        return db.query(Loan).filter(Loan.loan_id == loan_id).first()

    @staticmethod
    def get_loans_by_status(db: Session, status: ApplicationStatus, skip: int = 0, limit: int = 10) -> List[Loan]:
        return (
            db.query(Loan)
            .filter(Loan.application_status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_pending_loan_for_processing(db: Session) -> Optional[Loan]:
        """
        Thread-safe: lock row & mark PROCESSING so other threads won't pick it.
        """
        with _lock:
            loan = (
                db.query(Loan)
                .filter(Loan.application_status == ApplicationStatus.APPLIED)
                .with_for_update(skip_locked=True)
                .first()
            )

            if loan:
                loan.application_status = ApplicationStatus.PROCESSING
                db.commit()
                db.refresh(loan)

            return loan

    @staticmethod
    def update_loan_status(db: Session, loan_id: str, status: ApplicationStatus, agent_id: Optional[int] = None) -> Optional[Loan]:
        with _lock:
            loan = db.query(Loan).filter(Loan.loan_id == loan_id).first()
            if loan:
                loan.application_status = status
                if agent_id is not None:
                    loan.assigned_agent_id = agent_id
                db.commit()
                db.refresh(loan)
            return loan

    @staticmethod
    def get_status_counts(db: Session):
        return (
            db.query(Loan.application_status, func.count(Loan.loan_id))
            .group_by(Loan.application_status)
            .all()
        )

    @staticmethod
    def get_top_customers(db: Session, limit: int = 3):
        return (
            db.query(
                Loan.customer_name,
                Loan.customer_phone,
                func.count(Loan.loan_id).label("approved_count"),
                func.sum(Loan.loan_amount).label("total_amount"),
            )
            .filter(
                or_(
                    Loan.application_status == ApplicationStatus.APPROVED_BY_SYSTEM,
                    Loan.application_status == ApplicationStatus.APPROVED_BY_AGENT,
                )
            )
            .group_by(Loan.customer_name, Loan.customer_phone)
            .order_by(func.count(Loan.loan_id).desc())
            .limit(limit)
            .all()
        )
