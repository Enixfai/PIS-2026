from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class TicketCreatedEvent:
    ticket_id: str
    client_id: str
    subject: str

@dataclass(frozen=True)
class TicketAssignedEvent:
    ticket_id: str
    agent_id: str

@dataclass(frozen=True)
class MessageAddedEvent:
    ticket_id: str
    message_text: str

class Ticket:
    """Агрегат для записи (строгие инварианты)"""
    def __init__(self, ticket_id: str, client_id: str, subject: str):
        self.id = ticket_id
        self.client_id = client_id
        self.subject = subject
        self.status = "NEW"
        self.agent_id = None
        self.messages = []
        self.events =[]
        
        self.events.append(TicketCreatedEvent(ticket_id, client_id, subject))

    def assign_agent(self, agent_id: str):
        if self.status == "CLOSED":
            raise ValueError("Нельзя назначить закрытый тикет")
        self.agent_id = agent_id
        self.status = "OPEN"
        self.events.append(TicketAssignedEvent(self.id, agent_id))

    def add_message(self, text: str):
        if self.status == "CLOSED":
            raise ValueError("Тикет закрыт")
        self.messages.append(text)
        self.events.append(MessageAddedEvent(self.id, text))