from typing import List
from datetime import datetime
import uuid

from src.domain.value_objects import Priority, TicketStatus, MessageBody
from src.domain.models.message import Message
from src.domain.exceptions import InvalidTicketStateException, UnassignedTicketException
from src.domain.events import DomainEvent, TicketAssignedEvent, TicketResolvedEvent, MessageAddedEvent, TicketClosedEvent


class Ticket:
    
    def __init__(self, ticket_id: str, client_id: str, subject: str, priority: Priority):
        self._id = ticket_id
        self.client_id = client_id
        self.subject = subject
        self.priority = priority
        
        self._status = TicketStatus.NEW
        self._assigned_agent_id = None
        self._messages: List[Message] = []
        self._events: List[DomainEvent] =[]  
        
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    @property
    def id(self) -> str:
        return self._id

    @property
    def status(self) -> TicketStatus:
        return self._status

    @property
    def messages(self) -> List[Message]:
        return list(self._messages)

    @property
    def events(self) -> List[DomainEvent]:
        return list(self._events)

    def assign_agent(self, agent_id: str) -> None:
        if self._status in (TicketStatus.RESOLVED, TicketStatus.CLOSED):
            raise InvalidTicketStateException(f"Нельзя назначить агента на тикет в статусе {self._status.value}")
        
        self._assigned_agent_id = agent_id
        self._status = TicketStatus.OPEN
        self.updated_at = datetime.now()
        
        self._register_event(TicketAssignedEvent(self._id, agent_id))

    def add_message(self, author_id: str, text: str) -> None:
        if self._status == TicketStatus.CLOSED:
            raise InvalidTicketStateException("Нельзя добавить сообщение в закрытый тикет")
            
        body = MessageBody(text)
        message = Message(str(uuid.uuid4()), author_id, body)
        self._messages.append(message)
        self.updated_at = datetime.now()
        
        self._register_event(MessageAddedEvent(self._id, message.id))

    def resolve(self) -> None:
        if not self._assigned_agent_id:
            raise UnassignedTicketException("Нельзя перевести в RESOLVED тикет без назначенного агента")
            
        self._status = TicketStatus.RESOLVED
        self.updated_at = datetime.now()
        
        self._register_event(TicketResolvedEvent(self._id))

    def close(self) -> None:
        self._status = TicketStatus.CLOSED
        self.updated_at = datetime.now()
        
        self._register_event(TicketClosedEvent(self._id))

    def _register_event(self, event: DomainEvent):
        self._events.append(event)
        
    def clear_events(self):
        self._events.clear()