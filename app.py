import os.path
import time
import tensorflow as tf

import noti
import sound
from helpers import paths
from inference import make_infer, category_index
from test import test_make_infer
from helpers import labels_vi


import numpy as np
from flask import Flask, request, jsonify, send_file
import cv2

tf.keras.backend.clear_session()
model = tf.saved_model.load(os.path.join(paths["EXPORT_MODEL"], "saved_model"))
model = model.signatures["serving_default"]
labels = {i.get("id"): i.get("name") for i in labels_vi.values()}
# pool_labels_ids = list(map(lambda item: item["id"], list(category_index.values())))

app = Flask(__name__)


def save_image(img):
    img_dir = "uploads"
    if not os.path.isdir(img_dir):
        os.mkdir(img_dir)
    t = time.time()
    t_ms = int(t * 1000)
    cv2.imwrite("./{}/{}.jpg".format(img_dir, t_ms), img)


@app.route("/upload", methods=["POST"])
def upload_file():
    received = request
    if received.files:
        # print(received.files["imageFile"])
        file = received.files["imageFile"]
        nparr = np.fromstring(file.read(), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image_np = np.array(img)
        distances, classes, scores = make_infer(model, image_np)
        print(distances)
        print(classes)
        vat_can = ""
        min_dis = 1000000
        if len(classes) == 0:
            return "[SUCCESS] Image Received", 201
        for i in range(len(classes)):
            vat_can += labels.get(classes[i]) + ", " if i != len(classes) - 1 else ""
            min_dis = min(min_dis, distances[i])
            print(labels.get(classes[i]) + " " + str(distances[i]))
        alert_str = f'phía trước có {len(classes)} vật cản là {vat_can}. Vật cản gần nhất cách bạn {min_dis} centimet'
        sound_name = sound.convert_text_to_speech(alert_str)
        if sound_name == "":
            return "[FAILED] Image not received", 204
        firebase = noti.Firebase()
        firebase.push_all_device("sound_name", sound_name)
        return "[SUCCESS] Image Received", 201
    else:
        return "[FAILED] Image not received", 204


@app.route("/get-alert_sound", methods=["GET"])
def get_alert_sound():
    sound_name = request.args.get('sound_name')
    return sound.get_sound_path(sound_name)


@app.route('/')
def hello_world():  # put application's code here
    return jsonify(message="Hello World")


@app.route('/test-model-with-webcam')
def test_model_with_webcam():
    test_make_infer(model)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
