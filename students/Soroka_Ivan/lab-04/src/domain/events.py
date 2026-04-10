from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime

class DomainEvent(ABC):
    pass

@dataclass(frozen=True)
class TicketAssignedEvent(DomainEvent):
    ticket_id: str
    agent_id: str
    occurred_on: datetime = field(default_factory=datetime.now)

@dataclass(frozen=True)
class TicketResolvedEvent(DomainEvent):
    ticket_id: str
    occurred_on: datetime = field(default_factory=datetime.now)

@dataclass(frozen=True)
class MessageAddedEvent(DomainEvent):
    ticket_id: str
    message_id: str
    occurred_on: datetime = field(default_factory=datetime.now)

@dataclass(frozen=True)
class TicketClosedEvent(DomainEvent):
    ticket_id: str
    occurred_on: datetime = field(default_factory=datetime.now)