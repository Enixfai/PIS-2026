from src.domain.value_objects import EmailAddress

class Agent:
    def __init__(self, agent_id: str, email: EmailAddress, name: str):
        self._id = agent_id
        self.email = email
        self.name = name

    @property
    def id(self) -> str:
        return self._id

    def __eq__(self, other):
        if not isinstance(other, Agent):
            return False
        return self._id == other._id

    def __hash__(self):
        return hash(self._id)