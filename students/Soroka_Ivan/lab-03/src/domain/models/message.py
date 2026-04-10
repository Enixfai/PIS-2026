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

    def __eq__(self, other):
        if not isinstance(other, Message):
            return False
        return self._id == other._id
        
    def __hash__(self):
        return hash(self._id)