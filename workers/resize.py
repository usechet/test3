from common import connect_queue, update_status
import json, time

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"[Resize] Processing {data['id']}")
    time.sleep(2) 
    update_status(data['id'], 'resized')
    ch.basic_ack(delivery_tag=method.delivery_tag)
    from common import send_to_queue
    send_to_queue('watermark', data)

connect_queue('resize', callback)
