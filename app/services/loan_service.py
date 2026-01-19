from sqlalchemy.orm import Session
from app.models.loan import Loan, ApplicationStatus
from app.repositories.loan_repository import LoanRepository
from app.repositories.agent_repository import AgentRepository
from app.services.notification_service import get_notification_service
import uuid

class LoanService:
    def __init__(self):
        self.notification_service = get_notification_service()

    def create_loan(self, db: Session, loan_data: dict) -> Loan:
        loan = Loan(
            loan_id=str(uuid.uuid4()),
            customer_name=loan_data["customer_name"],
            customer_phone=loan_data["customer_phone"],
            loan_amount=loan_data["loan_amount"],
            loan_type=loan_data["loan_type"],
            application_status=ApplicationStatus.APPLIED,
        )
        return LoanRepository.create_loan(db, loan)

    def process_loan_decision(self, db: Session, loan: Loan):
        amount = float(loan.loan_amount)

        if amount < 10000:
            LoanRepository.update_loan_status(db, loan.loan_id, ApplicationStatus.APPROVED_BY_SYSTEM)
            self.notification_service.send_sms(loan.customer_phone, f"Your loan {loan.loan_id} is approved ✅")
            return

        if amount > 500000:
            LoanRepository.update_loan_status(db, loan.loan_id, ApplicationStatus.REJECTED_BY_SYSTEM)
            self.notification_service.send_sms(loan.customer_phone, f"Your loan {loan.loan_id} is rejected ❌")
            return

        # Under review
        agent = AgentRepository.get_available_agent(db)
        if agent:
            LoanRepository.update_loan_status(db, loan.loan_id, ApplicationStatus.UNDER_REVIEW, agent.agent_id)

            self.notification_service.send_push_notification(
                agent.email,
                f"Loan {loan.loan_id} assigned to you for review. Amount={amount}",
            )

            if agent.manager:
                self.notification_service.send_push_notification(
                    agent.manager.email,
                    f"Loan {loan.loan_id} assigned to your agent {agent.name}. Amount={amount}",
                )
        else:
            # If no agent available, keep it UNDER_REVIEW without assignment
            LoanRepository.update_loan_status(db, loan.loan_id, ApplicationStatus.UNDER_REVIEW)

    def agent_decision(self, db: Session, agent_id: int, loan_id: str, decision: str) -> Loan:
        loan = LoanRepository.get_loan_by_id(db, loan_id)
        if not loan:
            raise ValueError("Loan not found")

        if loan.application_status != ApplicationStatus.UNDER_REVIEW:
            raise ValueError("Loan is not under review")

        if loan.assigned_agent_id != agent_id:
            raise ValueError("Loan is not assigned to this agent")

        new_status = ApplicationStatus.APPROVED_BY_AGENT if decision == "APPROVE" else ApplicationStatus.REJECTED_BY_AGENT
        loan = LoanRepository.update_loan_status(db, loan_id, new_status)

        status_text = "approved ✅" if decision == "APPROVE" else "rejected ❌"
        self.notification_service.send_sms(
            loan.customer_phone,
            f"Your loan application {loan_id} has been {status_text}.",
        )

        return loan
