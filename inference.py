import os
from six import BytesIO
import numpy as np
import tensorflow as tf
from PIL import Image
from helpers import paths, files

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_util

def make_infer(model, image_np):
    output_dict = run_inference_for_single_image(model, image_np)
    boxes = []
    classes = []
    scores = []
    distances = []
    for i, x in enumerate(output_dict["detection_classes"]):
        if x in pool_labels_ids and output_dict["detection_scores"][i] > 0.5:
            _x, _y, _w, _h = output_dict["detection_boxes"][i]
            print("bbox", output_dict["detection_boxes"][i])
            distance_min = int(distance_finder(focus_length, label_id_with_known_width[x][0], _w))
            distance_max = int(distance_finder(focus_length, label_id_with_known_width[x][1], _w))
            distances.append((_x, _y, _w, _h, distance_min))

            classes.append(x)
            boxes.append(output_dict["detection_boxes"][i])
            scores.append(output_dict["detection_scores"][i])
    boxes = np.array(boxes)
    classes = np.array(classes)
    scores = np.array(scores)
    viz_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        boxes,
        classes,
        scores,
        category_index,
        instance_masks=output_dict.get("detection_masks_reframed", None),
        use_normalized_coordinates=True,
        line_thickness=1,
    )
    return distances, classes, scores

def distance_finder(focus_length, real_width, width_in_frame):
    distance = (real_width * focus_length) / width_in_frame

    # return the distance
    return distance

def run_inference_for_single_image(model, image):
    image = np.asarray(image)
    input_tensor = tf.convert_to_tensor(image)
    input_tensor = input_tensor[tf.newaxis, ...]
    output_dict = model(input_tensor)
    num_detections = int(output_dict.pop("num_detections"))
    output_dict = {key: value[0, :num_detections].numpy() for key, value in output_dict.items()}
    output_dict["num_detections"] = num_detections
    output_dict["detection_classes"] = output_dict["detection_classes"].astype(np.int64)

    if "detection_masks" in output_dict:
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            output_dict["detection_masks"], output_dict["detection_boxes"], image.shape[0], image.shape[1]
        )
        detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5, tf.uint8)
        output_dict["detection_masks_reframed"] = detection_masks_reframed.numpy()

    return output_dict

def load_image_into_numpy_array(path):
    img_data = tf.io.gfile.GFile(path, "rb").read()
    image = Image.open(BytesIO(img_data))
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)


category_index = label_map_util.create_category_index_from_labelmap(files["LABELMAP"], use_display_name=True)

# pool_labels = ['person', 'bicycle', 'car','motorcycle','airplane','bus','train','truck','bench','bird','cat','dog','chair', 'toilet', 'tv', 'book']
pool_labels_ids = list(map(lambda item: item["id"], list(category_index.values())))
focus_length = 2  # MP
# centimeter
label_id_with_known_width = {
    1: [45, 46],
    2: [56, 71],
    3: [150, 180],
    4: [60, 90],
    5: [240, 610],
    6: [240, 320],
    7: [340, 430],
    8: [180, 210],
    15: [180, 210],
    16: [25, 76],
    17: [23, 30],
    18: [30, 35],
    62: [41, 46],
    70: [36, 46],
    72: [81, 140],
    84: [10, 15],
}