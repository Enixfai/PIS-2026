from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class CreateTicketCommand:
    title: str
    description: str
    category: str
    idempotency_key: str

class CreateTicketUseCase(ABC):
    
    @abstractmethod
    def create_ticket(self, command: CreateTicketCommand) -> str:
        pass