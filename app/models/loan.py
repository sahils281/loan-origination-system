from sqlalchemy import Column, String, Numeric, DateTime, Enum as SQLEnum, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class LoanType(str, enum.Enum):
    PERSONAL = "PERSONAL"
    HOME = "HOME"
    AUTO = "AUTO"
    BUSINESS = "BUSINESS"

class ApplicationStatus(str, enum.Enum):
    APPLIED = "APPLIED"
    PROCESSING = "PROCESSING"
    APPROVED_BY_SYSTEM = "APPROVED_BY_SYSTEM"
    REJECTED_BY_SYSTEM = "REJECTED_BY_SYSTEM"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED_BY_AGENT = "APPROVED_BY_AGENT"
    REJECTED_BY_AGENT = "REJECTED_BY_AGENT"

class Loan(Base):
    __tablename__ = "loans"

    loan_id = Column(String, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    loan_amount = Column(Numeric(15, 2), nullable=False)
    loan_type = Column(SQLEnum(LoanType), nullable=False)

    application_status = Column(
        SQLEnum(ApplicationStatus),
        nullable=False,
        default=ApplicationStatus.APPLIED,
        index=True,
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assigned_agent_id = Column(Integer, ForeignKey("agents.agent_id"), nullable=True)
    assigned_agent = relationship("Agent", back_populates="assigned_loans")
