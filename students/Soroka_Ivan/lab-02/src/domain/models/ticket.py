class Ticket:
    
    def __init__(self, ticket_id: str, title: str, description: str, category: str):
        self.id = ticket_id
        self.title = title
        self.description = description
        self.category = category
        self.status = "NEW"
        self.queue_id = None
    
    def assign_queue(self, queue_id: str):
        self.queue_id = queue_id
        self.status = "ASSIGNED"

    def close_ticket(self):
        self.status = "CLOSED"