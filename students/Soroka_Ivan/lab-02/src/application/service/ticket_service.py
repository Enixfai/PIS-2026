from src.application.port.in_.create_ticket_use_case import CreateTicketUseCase, CreateTicketCommand
from src.application.port.out.ticket_repository import TicketRepository
from src.application.port.out.notification_port import NotificationPort
from src.domain.models.ticket import Ticket
import uuid

class TicketService(CreateTicketUseCase):
    
    def __init__(self, repository: TicketRepository, notification_port: NotificationPort):
        self.repository = repository
        self.notification_port = notification_port
    