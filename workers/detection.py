# watermark_worker.py

import json
import time
from common import connect_queue, update_status, send_to_queue

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        image_id = data['id']
        print(f"[Watermark Worker] Procesando imagen {image_id}...")

        time.sleep(2)

        update_status(image_id, 'watermarked')
        print(f"[Watermark Worker] Marca de agua aplicada a {image_id}.")

        send_to_queue('detection', data)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"[Watermark Worker] Error: {e}")

connect_queue('watermark', callback)
