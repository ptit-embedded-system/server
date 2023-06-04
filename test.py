import os
import cv2
import numpy as np
import math
import tensorflow as tf
from helpers import paths, files
from inference import make_infer

def test_make_infer(model):
  cap = cv2.VideoCapture(0)
  width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

  while True:
      ret, frame = cap.read()
      image_np = np.array(frame)
      distances, classes, scores = make_infer(model, image_np)

      if ret == True:
          for _x, _y, _w, _h, distance_min in distances:
              cv2.putText(
                  image_np,
                  str(distance_min),
                  (math.ceil(_x * 100), math.ceil(_y * 100) + int(_h * 100)),
                  cv2.FONT_HERSHEY_COMPLEX,
                  0.6,
                  (0, 255, 0),
                  2,
              )
              print(distance_min)
          cv2.imshow("Frame", image_np)
          # Press Q on keyboard to  exit
          if cv2.waitKey(25) & 0xFF == ord("q"):
              break

  cv2.destroyAllWindows()
  cap.release()