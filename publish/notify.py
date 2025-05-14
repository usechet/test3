import pika, json

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"[Notifier] Imagen {data['id']} procesada completamente.")

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.exchange_declare(exchange='processed_images', exchange_type='fanout')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='processed_images', queue=queue_name)

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print('Esperando notificaciones...')
channel.start_consuming()
