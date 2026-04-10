from dataclasses import dataclass
from typing import Optional

@dataclass
class TicketView:
    """Read Model: Денормализованная проекция тикета для быстрого чтения"""
    ticket_id: str
    client_id: str
    subject: str
    status: str
    agent_id: Optional[str]
    messages_count: int
    last_message_text: Optional[str]