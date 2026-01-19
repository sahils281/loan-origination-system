from fastapi import FastAPI
from contextlib import asynccontextmanager
import threading
import logging

from app.database import Base, engine
from app.api.v1 import loans, agents, customers
from app.services.loan_processor import LoanProcessor
from app.config import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()
processor = LoanProcessor()
processor_thread = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ Create tables automatically (for assignment simplicity)
    Base.metadata.create_all(bind=engine)

    global processor_thread
    processor_thread = threading.Thread(target=processor.start, daemon=True)
    processor_thread.start()

    logger.info("✅ LOS API started")
    yield

    processor.stop()
    logger.info("✅ LOS API stopped")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

app.include_router(loans.router, prefix="/api/v1", tags=["Loans"])
app.include_router(agents.router, prefix="/api/v1", tags=["Agents"])
app.include_router(customers.router, prefix="/api/v1", tags=["Customers"])

@app.get("/")
def root():
    return {"message": "Loan Origination System API", "version": settings.APP_VERSION}

@app.get("/health")
def health():
    return {"status": "healthy"}
