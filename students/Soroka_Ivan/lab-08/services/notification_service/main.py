import pika
import json
import time

def callback(ch, method, properties, body):
    event = json.loads(body)
    print(f"[x] Получено событие: {event['event']} для тикета {event['ticket_id']}")
    print(f"Отправка email клиенту {event['client_id']}...")

def start_consuming():
    time.sleep(10)
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='notifications')
    
    print(' [*] Ожидание сообщений...')
    channel.basic_consume(queue='notifications', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    start_consuming()