import os
import cv2
import numpy as np
import warnings
from .anti_spoof import AntiSpoofPredict
import glob
warnings.filterwarnings('ignore')

MODELS_PATH = './app/face_id/modeling/anti_spoof_models/*.pth'


def livenesss_predict(image_nparray, model_dir=MODELS_PATH, device_id=1):
    '''check if the face is real or fake'''
    model_test = AntiSpoofPredict(device_id)
    prediction = np.zeros((1, 3))
    image = cv2.resize(image_nparray, (80, 80))
    # sum the prediction from single model's result
    # for model_name in os.listdir(MODELS_PATH):
    for model in glob.glob(MODELS_PATH):
        prediction += model_test.predict(image, model)

    label = np.argmax(prediction)
    value = prediction[0][label] / 2
    '''if label == 1 then it's real face else spoof'''
    return label, value
