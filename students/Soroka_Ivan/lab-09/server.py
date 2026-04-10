import grpc
from concurrent import futures
import time
import ticket_pb2
import ticket_pb2_grpc

class TicketService(ticket_pb2_grpc.TicketServiceServicer):
    def CreateTicket(self, request, context):
        print(f"[gRPC] Создание тикета: {request.subject}")
        return ticket_pb2.TicketResponse(
            ticket_id="TKT-777",
            status="NEW",
            subject=request.subject
        )

    def GetTicket(self, request, context):
        return ticket_pb2.TicketResponse(
            ticket_id=request.ticket_id,
            status="OPEN",
            subject="Проблема с сетью"
        )

    def StreamTickets(self, request, context):
        """Server-side streaming: отправляем новые тикеты агенту в реальном времени"""
        print(f"[gRPC] Агент {request.agent_id} подписался на поток.")
        tickets = [
            ("TKT-1", "Ошибка входа"),
            ("TKT-2", "Доступ к базе"),
            ("TKT-3", "Обновление ПО")
        ]
        for t_id, subj in tickets:
            time.sleep(2)
            yield ticket_pb2.TicketResponse(ticket_id=t_id, status="NEW", subject=subj)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ticket_pb2_grpc.add_TicketServiceServicer_to_server(TicketService(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC Сервер запущен на порту 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()