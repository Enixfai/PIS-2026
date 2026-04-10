import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.config.database import Base
from src.infrastructure.adapter.out.postgres_ticket_repository import PostgresTicketRepository
from src.domain.models.ticket import Ticket
from src.domain.value_objects import Priority

@pytest.fixture
def db_session():
    """Создает чистую БД в памяти для каждого теста"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_repository_saves_and_retrieves_ticket(db_session):
    repo = PostgresTicketRepository(db_session)
    ticket = Ticket("T-DB-1", "client-1", "Test DB", Priority("URGENT"))
    
    repo.save(ticket)
    
    saved_ticket = repo.find_by_id("T-DB-1")
    assert saved_ticket is not None
    assert saved_ticket.subject == "Test DB"
    assert saved_ticket.status.value == "NEW"