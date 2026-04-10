from src.infrastructure.adapter.out.in_memory_ticket_repository import InMemoryTicketRepository
from src.application.service.ticket_service import TicketService

class DummyNotificationAdapter:
    """Заглушка для порта уведомлений"""
    def send_ticket_created_event(self, ticket_id: str):
        pass

class DependencyContainer:
    """Контейнер внедрения зависимостей (DI Container)"""
    
    def __init__(self):
        self.ticket_repo = InMemoryTicketRepository()
        self.notification_adapter = DummyNotificationAdapter()
        
        self.ticket_service = TicketService(
            repository=self.ticket_repo,
            notification_port=self.notification_adapter
        )
    
    def get_ticket_service(self) -> TicketService:
        return self.ticket_service