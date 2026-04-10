import uuid
from src.application.command.commands import CreateTicketCommand, AssignAgentCommand, AddMessageCommand
from src.application.port.out.ticket_repository import TicketRepository
from src.domain.models.ticket import Ticket
from src.domain.value_objects import Priority

class CreateTicketHandler:
    """Обработчик команды создания тикета"""
    def __init__(self, repository: TicketRepository):
        self.repository = repository

    def handle(self, command: CreateTicketCommand) -> str:
        if not command.subject:
            raise ValueError("Тема тикета не может быть пустой")
            
        ticket_id = f"TKT-{uuid.uuid4().hex[:8]}"
        ticket = Ticket(
            ticket_id=ticket_id,
            client_id=command.client_id,
            subject=command.subject,
            priority=Priority(command.priority)
        )
        
        self.repository.save(ticket)

        
        return ticket_id

class AssignAgentHandler:
    """Обработчик команды назначения агента"""
    def __init__(self, repository: TicketRepository):
        self.repository = repository

    def handle(self, command: AssignAgentCommand) -> None:
        ticket = self.repository.find_by_id(command.ticket_id)
        if not ticket:
            raise ValueError(f"Тикет {command.ticket_id} не найден")
            
        ticket.assign_agent(command.agent_id)
        
        self.repository.save(ticket)