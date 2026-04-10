class DomainException(Exception):
    """Базовый класс для всех бизнес-ошибок домена"""
    pass

class InvalidTicketStateException(DomainException):
    pass

class UnassignedTicketException(DomainException):
    pass