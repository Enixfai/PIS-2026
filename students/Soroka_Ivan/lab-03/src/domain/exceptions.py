class DomainException(Exception):
    pass

class InvalidTicketStateException(DomainException):
    pass

class UnassignedTicketException(DomainException):
    pass