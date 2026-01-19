from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.loan import AgentDecision, LoanResponse
from app.services.loan_service import LoanService

router = APIRouter()
loan_service = LoanService()

@router.put("/agents/{agent_id}/loans/{loan_id}/decision", response_model=LoanResponse)
def agent_loan_decision(agent_id: int, loan_id: str, decision: AgentDecision, db: Session = Depends(get_db)):
    try:
        return loan_service.agent_decision(db, agent_id, loan_id, decision.decision)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
