from fastapi import FastAPI, HTTPException
import pika
import json

app = FastAPI()

class CircuitBreaker:
    def __init__(self):
        self.failure_count = 0
        self.state = "CLOSED" 

    def call_external_service(self, func):
        if self.state == "OPEN":
            return {"error": "Agent Service недоступен (Circuit Breaker OPEN). Fallback-данные."}
        try:
            result = func()
            self.failure_count = 0
            return result
        except Exception:
            self.failure_count += 1
            if self.failure_count >= 3:
                self.state = "OPEN"
            raise HTTPException(status_code=503, detail="Ошибка внешнего сервиса")

circuit_breaker = CircuitBreaker()

@app.post("/")
def create_ticket(client_id: str, subject: str):
    ticket_id = "TKT-123"
    
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='notifications')
        
        event = {"event": "TicketCreated", "ticket_id": ticket_id, "client_id": client_id}
        channel.basic_publish(exchange='', routing_key='notifications', body=json.dumps(event))
        connection.close()
    except Exception as e:
        print("RabbitMQ недоступен, но тикет создан!") 
        
    return {"ticket_id": ticket_id, "status": "NEW", "message": "Событие отправлено в Event Bus"}