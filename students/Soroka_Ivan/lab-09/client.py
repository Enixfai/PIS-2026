import grpc
import ticket_pb2
import ticket_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ticket_pb2_grpc.TicketServiceStub(channel)
        
        print("--- Вызов CreateTicket ---")
        response = stub.CreateTicket(ticket_pb2.CreateTicketRequest(
            client_id="ivan_001", subject="Помогите!", priority="HIGH"
        ))
        print(f"Ответ сервера: {response.ticket_id}, статус: {response.status}")

        print("\n--- Подписка на поток StreamTickets ---")
        responses = stub.StreamTickets(ticket_pb2.StreamRequest(agent_id="agent_42"))
        for res in responses:
            print(f"[Stream] Новый тикет для обработки: {res.ticket_id} ({res.subject})")

if __name__ == '__main__':
    run()