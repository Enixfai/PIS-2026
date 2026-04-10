from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.infrastructure.config.database import get_db
from src.infrastructure.adapter.out.postgres_ticket_repository import PostgresTicketRepository
from src.application.service.ticket_facade import TicketApplicationService
from src.application.command.handlers import CreateTicketHandler, AssignAgentHandler
from src.application.query.handlers import GetTicketByIdHandler
from src.application.command.commands import CreateTicketCommand, AssignAgentCommand
from src.application.query.queries import GetTicketByIdQuery
from src.domain.exceptions import DomainException

router = APIRouter(prefix="/api/tickets", tags=["Tickets"])

def get_ticket_service(db: Session = Depends(get_db)) -> TicketApplicationService:
    repo = PostgresTicketRepository(db)
    return TicketApplicationService(
        create_handler=CreateTicketHandler(repo),
        assign_handler=AssignAgentHandler(repo),
        get_handler=GetTicketByIdHandler(repo)
    )

@router.post("/", status_code=201)
def create_ticket(request: dict, service: TicketApplicationService = Depends(get_ticket_service)):
    try:
        command = CreateTicketCommand(**request)
        ticket_id = service.create_ticket(command)
        return {"ticket_id": ticket_id, "message": "Тикет успешно сохранен в PostgreSQL!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{ticket_id}/assign-agent")
def assign_agent(ticket_id: str, request: dict, service: TicketApplicationService = Depends(get_ticket_service)):
    try:
        command = AssignAgentCommand(ticket_id=ticket_id, agent_id=request.get("agent_id"))
        service.assign_agent(command)
        return {"message": "Агент успешно назначен"}
    except DomainException as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/{ticket_id}")
def get_ticket(ticket_id: str, service: TicketApplicationService = Depends(get_ticket_service)):
    query = GetTicketByIdQuery(ticket_id=ticket_id)
    ticket_dto = service.get_ticket(query)
    if not ticket_dto:
        raise HTTPException(status_code=404, detail="Тикет не найден в БД")
    return ticket_dto