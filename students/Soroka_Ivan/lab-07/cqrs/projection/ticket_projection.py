from cqrs.write_model.ticket_aggregate import TicketCreatedEvent, TicketAssignedEvent, MessageAddedEvent
from cqrs.read_model.ticket_view import TicketView

class TicketProjection:
    """Event Handler: Слушает события и обновляет Read Model"""
    def __init__(self, read_db: dict):
        self.read_db = read_db 

    def handle_ticket_created(self, event: TicketCreatedEvent):
        self.read_db[event.ticket_id] = TicketView(
            ticket_id=event.ticket_id,
            client_id=event.client_id,
            subject=event.subject,
            status="NEW",
            agent_id=None,
            messages_count=0,
            last_message_text=None
        )

    def handle_ticket_assigned(self, event: TicketAssignedEvent):
        view = self.read_db.get(event.ticket_id)
        if view:
            view.agent_id = event.agent_id
            view.status = "OPEN"

    def handle_message_added(self, event: MessageAddedEvent):
        view = self.read_db.get(event.ticket_id)
        if view:
            view.messages_count += 1
            view.last_message_text = event.message_text