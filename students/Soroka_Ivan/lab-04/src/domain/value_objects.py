from dataclasses import dataclass
from enum import Enum
import re

class TicketStatus(Enum):
    """Value Object (Enum): Статус тикета"""
    NEW = "NEW"
    OPEN = "OPEN"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


@dataclass(frozen=True)
class EmailAddress:
    """Value Object: Email адрес с валидацией"""
    value: str

    def __post_init__(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.value):
            raise ValueError(f"Некорректный email адрес: {self.value}")


@dataclass(frozen=True)
class Priority:
    """Value Object: Приоритет тикета"""
    level: str  

    def __post_init__(self):
        valid_levels = {"LOW", "NORMAL", "HIGH", "URGENT"}
        if self.level not in valid_levels:
            raise ValueError(f"Неизвестный приоритет: {self.level}. Допустимые: {valid_levels}")


@dataclass(frozen=True)
class MessageBody:
    """Value Object: Текст сообщения с ограничениями"""
    text: str

    def __post_init__(self):
        if not self.text or not self.text.strip():
            raise ValueError("Сообщение не может быть пустым")
        if len(self.text) > 4000:
            raise ValueError("Превышена максимальная длина сообщения (4000 символов)")