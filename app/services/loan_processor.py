from concurrent.futures import ThreadPoolExecutor
import time
import random
import logging
from app.database import SessionLocal
from app.repositories.loan_repository import LoanRepository
from app.services.loan_service import LoanService
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class LoanProcessor:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=settings.PROCESSOR_THREAD_POOL_SIZE)
        self.loan_service = LoanService()
        self.is_running = False

    def process_single_loan(self):
        db = SessionLocal()
        try:
            loan = LoanRepository.get_pending_loan_for_processing(db)
            if not loan:
                return

            logger.info(f"Processing loan: {loan.loan_id}")

            delay = random.uniform(settings.PROCESSING_DELAY_MIN, settings.PROCESSING_DELAY_MAX)
            time.sleep(delay)

            self.loan_service.process_loan_decision(db, loan)
            logger.info(f"Completed loan: {loan.loan_id}")

        except Exception as e:
            logger.error(f"Error processing loan: {str(e)}")
            db.rollback()
        finally:
            db.close()

    def start(self):
        self.is_running = True
        logger.info("Loan processor started ✅")

        while self.is_running:
            self.executor.submit(self.process_single_loan)
            time.sleep(1)

    def stop(self):
        self.is_running = False
        self.executor.shutdown(wait=True)
        logger.info("Loan processor stopped ✅")
