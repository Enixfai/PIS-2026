from dataclasses import dataclass

@dataclass(frozen=True)
class GetTicketByIdQuery:
    """Запрос: Получить тикет по ID"""
    ticket_id: str