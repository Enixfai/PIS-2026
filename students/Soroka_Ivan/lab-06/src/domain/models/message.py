from datetime import datetime
from src.domain.value_objects import MessageBody

class Message:
    def __init__(self, message_id: str, author_id: str, body: MessageBody):
        self._id = message_id
        self.author_id = author_id
        self.body = body
        self.created_at = datetime.now()

    @property
    def id(self) -> str:
        return self._id