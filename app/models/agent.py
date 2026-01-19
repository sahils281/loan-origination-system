from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Agent(Base):
    __tablename__ = "agents"

    agent_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=False)

    manager_id = Column(Integer, ForeignKey("agents.agent_id"), nullable=True)
    is_available = Column(Boolean, default=True)

    manager = relationship("Agent", remote_side=[agent_id], backref="subordinates")
    assigned_loans = relationship("Loan", back_populates="assigned_agent")
