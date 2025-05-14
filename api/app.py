from flask import Flask, request, jsonify
import uuid, os, json
import pika
from utils import save_file, send_to_queue, get_status

app = Flask(__name__)
UPLOAD_FOLDER = "/data/images"
STATUS_FOLDER = "/data/status"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATUS_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files['image']
    uid = str(uuid.uuid4())
    path = f"{UPLOAD_FOLDER}/{uid}.jpg"
    save_file(image, path)

    initial_status = {'id': uid, 'status': 'uploaded'}
    with open(f"{STATUS_FOLDER}/{uid}.json", "w") as f:
        json.dump(initial_status, f)

    send_to_queue('resize', {'id': uid, 'path': path})
    return jsonify({'id': uid}), 202

@app.route('/status/<img_id>', methods=['GET'])
def status(img_id):
    return jsonify(get_status(img_id))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
