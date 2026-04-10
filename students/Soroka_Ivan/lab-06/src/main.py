from fastapi import FastAPI
from src.infrastructure.config.database import Base, engine
from src.infrastructure.adapter.in_.ticket_controller import router as ticket_router

Base.metadata.create_all(bind=engine)

#http://127.0.0.1:8000/docs

app = FastAPI(
    title="HelpDesk API",
    description="API для управления тикетами (PostgreSQL)",
    version="1.0.0"
)

app.include_router(ticket_router)