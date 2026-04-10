import pytest
from src.domain.models.ticket import Ticket
from src.domain.value_objects import Priority, TicketStatus, MessageBody, EmailAddress
from src.domain.exceptions import InvalidTicketStateException, UnassignedTicketException
from src.domain.events import TicketAssignedEvent

class TestTicketAggregate:
    
    def setup_method(self):
        priority = Priority("NORMAL")
        self.ticket = Ticket("T-100", "client-1", "Проблема с входом", priority)

    def test_cannot_add_message_to_closed_ticket(self):
        self.ticket.close()
        
        with pytest.raises(InvalidTicketStateException) as exc:
            self.ticket.add_message("client-1", "Спасибо!")
        assert "закрытый тикет" in str(exc.value)

    def test_cannot_resolve_unassigned_ticket(self):
        with pytest.raises(UnassignedTicketException):
            self.ticket.resolve()

    def test_assign_agent_changes_status_and_registers_event(self):
        self.ticket.assign_agent("agent-42")
        
        assert self.ticket.status == TicketStatus.OPEN
        assert len(self.ticket.events) == 1
        assert isinstance(self.ticket.events[0], TicketAssignedEvent)
        assert self.ticket.events[0].agent_id == "agent-42"
        
    def test_value_object_message_body_validation(self):
        with pytest.raises(ValueError):
            MessageBody("   ") 
    def test_value_object_email_validation(self):
        with pytest.raises(ValueError):
            EmailAddress("invalid-email.com") 