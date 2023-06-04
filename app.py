import os.path
import time
import tensorflow as tf
from helpers import paths
from inference import make_infer, category_index
from test import test_make_infer


import numpy as np
from flask import Flask, request, jsonify, send_file
import cv2

tf.keras.backend.clear_session()
model = tf.saved_model.load(os.path.join(paths["EXPORT_MODEL"], "saved_model"))
model = model.signatures["serving_default"]
labels = {i.get("id"): i.get("name") for i in category_index.values()}
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
        for i in range(len(classes)):
            print(labels.get(classes[i]) + " " + str(distances[i]))
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
