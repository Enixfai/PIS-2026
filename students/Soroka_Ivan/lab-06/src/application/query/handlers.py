from src.application.query.queries import GetTicketByIdQuery
from src.application.query.dtos import TicketDto, MessageDto
from src.application.port.out.ticket_repository import TicketRepository

class GetTicketByIdHandler:
    """Обработчик запроса получения тикета"""
    def __init__(self, repository: TicketRepository):
        self.repository = repository

    def handle(self, query: GetTicketByIdQuery) -> TicketDto:
        ticket = self.repository.find_by_id(query.ticket_id)
        if not ticket:
            return None
            
        messages_dto =[
            MessageDto(
                id=msg.id,
                author_id=msg.author_id,
                text=msg.body.text,
                created_at=msg.created_at.isoformat()
            ) for msg in ticket.messages
        ]
        
        return TicketDto(
            id=ticket.id,
            client_id=ticket.client_id,
            subject=ticket.subject,
            status=ticket.status.value,
            priority=ticket.priority.level,
            assigned_agent_id=ticket._assigned_agent_id,
            messages=messages_dto
        )