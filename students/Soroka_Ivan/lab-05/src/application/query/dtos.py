from dataclasses import dataclass
from typing import List

@dataclass
class MessageDto:
    """Read DTO для сообщения"""
    id: str
    author_id: str
    text: str
    created_at: str

@dataclass
class TicketDto:
    """Read DTO для тикета"""
    id: str
    client_id: str
    subject: str
    status: str
    priority: str
    assigned_agent_id: str
    messages: List[MessageDto]