import pytest
from unittest.mock import Mock

from src.application.command.commands import CreateTicketCommand, AssignAgentCommand
from src.application.command.handlers import CreateTicketHandler, AssignAgentHandler
from src.application.query.queries import GetTicketByIdQuery
from src.application.query.handlers import GetTicketByIdHandler
from src.domain.models.ticket import Ticket
from src.domain.value_objects import Priority

class TestCommandHandlers:
    
    def test_create_ticket_handler_saves_to_repo(self):
        # 1. Подготовка (Arrange)
        mock_repo = Mock()
        handler = CreateTicketHandler(repository=mock_repo)
        cmd = CreateTicketCommand(client_id="c-1", subject="Bug", priority="HIGH")
        
        # 2. Действие (Act)
        ticket_id = handler.handle(cmd)
        
        # 3. Проверка (Assert)
        assert ticket_id.startswith("TKT-")
        mock_repo.save.assert_called_once()
        
        # Проверяем, что в save передали правильный Ticket
        saved_ticket = mock_repo.save.call_args[0][0]
        assert saved_ticket.client_id == "c-1"
        assert saved_ticket.subject == "Bug"

    def test_assign_agent_handler_calls_domain_method(self):
        # 1. Подготовка
        mock_repo = Mock()
        ticket = Ticket("T-1", "c-1", "Bug", Priority("LOW"))
        mock_repo.find_by_id.return_value = ticket
        
        handler = AssignAgentHandler(repository=mock_repo)
        cmd = AssignAgentCommand(ticket_id="T-1", agent_id="a-99")
        
        # 2. Действие
        handler.handle(cmd)
        
        # 3. Проверка
        mock_repo.find_by_id.assert_called_with("T-1")
        assert ticket._assigned_agent_id == "a-99"  # Доменная логика отработала
        mock_repo.save.assert_called_once_with(ticket)

class TestQueryHandlers:

    def test_get_ticket_by_id_handler_returns_dto(self):
        # 1. Подготовка
        mock_repo = Mock()
        ticket = Ticket("T-2", "c-2", "Help", Priority("NORMAL"))
        mock_repo.find_by_id.return_value = ticket
        
        handler = GetTicketByIdHandler(repository=mock_repo)
        query = GetTicketByIdQuery(ticket_id="T-2")
        
        # 2. Действие
        dto = handler.handle(query)
        
        # 3. Проверка
        assert dto is not None
        assert dto.id == "T-2"
        assert dto.subject == "Help"
        assert dto.status == "NEW"
        # DTO не должно иметь доменных методов (например, assign_agent)
        assert not hasattr(dto, "assign_agent")