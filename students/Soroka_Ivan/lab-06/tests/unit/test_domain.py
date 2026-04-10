import pytest
from src.domain.models.ticket import Ticket
from src.domain.value_objects import Priority, TicketStatus, MessageBody
from src.domain.exceptions import InvalidTicketStateException, UnassignedTicketException

def test_ticket_invariants():
    ticket = Ticket("T-1", "client-1", "Help", Priority("NORMAL"))
    assert ticket.status == TicketStatus.NEW
    
    with pytest.raises(UnassignedTicketException):
        ticket.resolve()
        
    ticket.assign_agent("agent-007")
    assert ticket.status == TicketStatus.OPEN
    
    ticket.close()
    with pytest.raises(InvalidTicketStateException):
        ticket.add_message("client-1", "Сообщение в закрытый тикет")