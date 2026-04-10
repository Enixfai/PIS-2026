from src.infrastructure.adapter.out.in_memory_ticket_repository import InMemoryTicketRepository
from src.application.command.handlers import CreateTicketHandler, AssignAgentHandler
from src.application.query.handlers import GetTicketByIdHandler
from src.application.service.ticket_facade import TicketApplicationService

class DependencyContainer:
    """Контейнер для сборки приложения (DI)"""
    
    def __init__(self):
        self.repository = InMemoryTicketRepository()

        self.create_ticket_handler = CreateTicketHandler(repository=self.repository)
        self.assign_agent_handler = AssignAgentHandler(repository=self.repository)
        self.get_ticket_handler = GetTicketByIdHandler(repository=self.repository)

        self.ticket_service = TicketApplicationService(
            create_handler=self.create_ticket_handler,
            assign_handler=self.assign_agent_handler,
            get_handler=self.get_ticket_handler
        )

    def get_ticket_service(self) -> TicketApplicationService:
        """Метод для получения готового сервиса контроллерами"""
        return self.ticket_service