import os

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_util

CUSTOM_MODEL_NAME = "my_ssd_mobnet"
PRETRAINED_MODEL_NAME = "ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8"
PRETRAINED_MODEL_URL = "http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.tar.gz"
TF_RECORD_SCRIPT_NAME = "generate_tfrecord.py"
LABEL_MAP_NAME = "label_map.pbtxt"

paths = {
    "WORKSPACE_PATH": os.path.join("Tensorflow", "workspace"),
    "SCRIPTS_PATH": os.path.join("Tensorflow", "scripts"),
    "APIMODEL_PATH": os.path.join("Tensorflow", "models"),
    "ANNOTATION_PATH": os.path.join("Tensorflow", "workspace", "annotations"),
    "IMAGE_PATH": os.path.join("Tensorflow", "workspace", "images"),
    "MODEL_PATH": os.path.join("Tensorflow", "workspace", "models"),
    "PRETRAINED_MODEL_PATH": os.path.join("Tensorflow", "workspace", "pre-trained-models"),
    "CHECKPOINT_PATH": os.path.join("Tensorflow", "workspace", "models", CUSTOM_MODEL_NAME),
    "OUTPUT_PATH": os.path.join("Tensorflow", "workspace", "models", CUSTOM_MODEL_NAME, "export"),
    "TFJS_PATH": os.path.join("Tensorflow", "workspace", "models", CUSTOM_MODEL_NAME, "tfjsexport"),
    "TFLITE_PATH": os.path.join("Tensorflow", "workspace", "models", CUSTOM_MODEL_NAME, "tfliteexport"),
    "PROTOC_PATH": os.path.join("Tensorflow", "protoc"),
    "EXPORT_MODEL": os.path.join("Tensorflow", "workspace", "export_model"),
}

files = {
    "PIPELINE_CONFIG": os.path.join("Tensorflow", "workspace", "models", CUSTOM_MODEL_NAME, "pipeline.config"),
    "TF_RECORD_SCRIPT": os.path.join(paths["SCRIPTS_PATH"], TF_RECORD_SCRIPT_NAME),
    "LABELMAP": os.path.join(paths["ANNOTATION_PATH"], LABEL_MAP_NAME),
}

labels_vi = [
  {
    'id': 1,
    'name': 'người'
  },
  {
    'id': 2,
    'name': 'xe đạp'
  },
  {
    'id': 3,
    'name': 'ô tô'
  },
  {
    'id': 4,
    'name': 'xe máy'
  },
  {
    'id': 5,
    'name': 'máy bay'
  },
  {
    'id': 6,
    'name': 'xe buýt'
  },
  {
    'id': 7,
    'name': 'tàu hoả'
  },
  {
    'id': 8,
    'name': 'xe tải'
  },
  {
    'id': 15,
    'name': 'ghế dài'
  },
  {
    'id': 16,
    'name': 'chim'
  },
  {
    'id': 17,
    'name': 'mèo'
  },
  {
    'id': 18,
    'name': 'chó'
  },
  {
    'id': 62,
    'name': 'ghế đơn'
  },
  {
    'id': 70,
    'name': 'toilet'
  },
  {
    'id': 72,
    'name': 'ti vi'
  },
  {
    'id': 84,
    'name': 'sách'
  }
]