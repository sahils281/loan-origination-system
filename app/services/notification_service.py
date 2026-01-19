from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class NotificationService(ABC):
    @abstractmethod
    def send_push_notification(self, recipient: str, message: str):
        pass

    @abstractmethod
    def send_sms(self, phone: str, message: str):
        pass

class MockNotificationService(NotificationService):
    def send_push_notification(self, recipient: str, message: str):
        logger.info(f"[PUSH] To: {recipient} | {message}")
        return True

    def send_sms(self, phone: str, message: str):
        logger.info(f"[SMS] To: {phone} | {message}")
        return True

def get_notification_service() -> NotificationService:
    return MockNotificationService()
