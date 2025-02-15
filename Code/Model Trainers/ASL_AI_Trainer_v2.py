import os
import mediapipe_model_maker
import tensorflow as tf
import os
from mediapipe_model_maker import gesture_recognizer
import matplotlib.pyplot as plt

DATASET_PATH = "Dataset\\Test_Alphabet"

def TrainModel(path):
  data = gesture_recognizer.Dataset.from_folder(
      dirname=path,
      hparams=gesture_recognizer.HandDataPreprocessingParams()
  )

  train_data, rest_data = data.split(0.8)
  validation_data, test_data = rest_data.split(0.5)

  hparams = gesture_recognizer.HParams(export_dir="/content/ASL_model_v1", epochs=10)
  options = gesture_recognizer.GestureRecognizerOptions(hparams=hparams)
  model = gesture_recognizer.GestureRecognizer.create(
      train_data=train_data,
      validation_data=validation_data,
      options=options,
  )

  loss, acc = model.evaluate(test_data, batch_size=1)
  print(f"Test loss:{loss}, Test accuracy:{acc}")

  model.export_model("ASL_Model_v3.task")

TrainModel(DATASET_PATH)