from cqrs.write_model.ticket_aggregate import Ticket
from cqrs.projection.ticket_projection import TicketProjection

def test_cqrs_sync_via_events():
    read_db = {}
    projection = TicketProjection(read_db)

    ticket = Ticket("T-100", "client_1", "Не работает сайт")
    
    for event in ticket.events:
        projection.handle_ticket_created(event)
    ticket.events.clear()

    assert "T-100" in read_db
    assert read_db["T-100"].status == "NEW"
    assert read_db["T-100"].messages_count == 0

    ticket.assign_agent("agent_007")
    ticket.add_message("Попробуйте почистить кэш")

    for event in ticket.events:
        if type(event).__name__ == "TicketAssignedEvent":
            projection.handle_ticket_assigned(event)
        elif type(event).__name__ == "MessageAddedEvent":
            projection.handle_message_added(event)

    view = read_db["T-100"]
    assert view.status == "OPEN"
    assert view.agent_id == "agent_007"
    assert view.messages_count == 1
    assert view.last_message_text == "Попробуйте почистить кэш"

    print(f"\n[Read Model In-Memory] Быстрое чтение по ключу 'T-100':\n{view}")