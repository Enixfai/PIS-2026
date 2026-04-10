from unittest.mock import Mock
from src.application.command.commands import CreateTicketCommand
from src.application.command.handlers import CreateTicketHandler

def test_create_ticket_handler_saves_to_repo():
    mock_repo = Mock()
    handler = CreateTicketHandler(repository=mock_repo)
    cmd = CreateTicketCommand(client_id="c-1", subject="Bug", priority="HIGH")
    
    ticket_id = handler.handle(cmd)
    
    assert ticket_id.startswith("TKT-")
    mock_repo.save.assert_called_once()