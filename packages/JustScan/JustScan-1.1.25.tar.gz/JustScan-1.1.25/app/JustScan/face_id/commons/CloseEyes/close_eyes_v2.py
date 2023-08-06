import numpy as np
import cv2
import onnxruntime
from .utils import extract_eye
from JustScan.face_id.commons.config import config


# 0: Close 1: Open

def preprocessing(image):
    # img = image[:,:,::-1]
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    return np.expand_dims(img, axis=0)


def crop_eye(image, left_eye, right_eye):
    left_eyes, right_eyes = extract_eye(image, left_eye, right_eye)
    return left_eyes, right_eyes


class CloseEyes:
    def __init__(self, model_file=config['oce']):
        assert model_file is not None
        self.model_file = model_file
        self.ort = onnxruntime.InferenceSession(self.model_file, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])

    def predict(self, image):
        img = preprocessing(image)
        inputs = self.ort.get_inputs()[0].name
        output_names = self.ort.get_outputs()[0].name
        net = self.ort.run([output_names], {inputs: img.astype('float32')})[0]
        ids = np.argmax(net)
        confidence = np.max(net[0])
        if confidence > 0.9:
            ids = True if ids == 0 else False
        return ids, confidence
