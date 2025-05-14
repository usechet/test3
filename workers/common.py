import pika, json, os

def connect_queue(queue, callback):
    conn = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = conn.channel()
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)
    channel.start_consuming()

def update_status(img_id, new_status):
    status_path = f"/data/status/{img_id}.json"
    if os.path.exists(status_path):
        with open(status_path) as f:
            data = json.load(f)
        data['status'] = new_status
        with open(status_path, "w") as f:
            json.dump(data, f)
