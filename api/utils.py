import pika, json, os

def save_file(image, path):
    image.save(path)

def send_to_queue(queue, body):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps(body),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()

def get_status(img_id):
    path = f"/data/status/{img_id}.json"
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {'error': 'not found'}
