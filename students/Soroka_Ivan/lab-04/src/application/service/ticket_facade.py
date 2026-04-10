from src.application.command.commands import CreateTicketCommand, AssignAgentCommand
from src.application.command.handlers import CreateTicketHandler, AssignAgentHandler
from src.application.query.queries import GetTicketByIdQuery
from src.application.query.handlers import GetTicketByIdHandler
from src.application.query.dtos import TicketDto

class TicketApplicationService:
    """Фасад прикладного слоя (Оркестратор CQRS)"""
    
    def __init__(
        self, 
        create_handler: CreateTicketHandler, 
        assign_handler: AssignAgentHandler,
        get_handler: GetTicketByIdHandler
    ):
        self.create_handler = create_handler
        self.assign_handler = assign_handler
        self.get_handler = get_handler

    def create_ticket(self, command: CreateTicketCommand) -> str:
        return self.create_handler.handle(command)

    def assign_agent(self, command: AssignAgentCommand) -> None:
        self.assign_handler.handle(command)

    def get_ticket(self, query: GetTicketByIdQuery) -> TicketDto:
        return self.get_handler.handle(query)