from dataclasses import dataclass

@dataclass(frozen=True)
class CreateTicketCommand: 
    """Команда: Создать новый тикет"""
    client_id: str
    subject: str
    priority: str

@dataclass(frozen=True)
class AssignAgentCommand:
    """Команда: Назначить агента на тикет"""
    ticket_id: str
    agent_id: str

@dataclass(frozen=True)
class AddMessageCommand:
    """Команда: Добавить сообщение в тикет"""
    ticket_id: str
    author_id: str
    text: str