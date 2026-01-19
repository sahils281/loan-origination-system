from sqlalchemy.orm import Session
from app.models.agent import Agent
from typing import Optional
import threading

_lock = threading.Lock()

class AgentRepository:
    @staticmethod
    def get_available_agent(db: Session) -> Optional[Agent]:
        with _lock:
            return db.query(Agent).filter(Agent.is_available == True).first()

    @staticmethod
    def get_agent_by_id(db: Session, agent_id: int) -> Optional[Agent]:
        return db.query(Agent).filter(Agent.agent_id == agent_id).first()
