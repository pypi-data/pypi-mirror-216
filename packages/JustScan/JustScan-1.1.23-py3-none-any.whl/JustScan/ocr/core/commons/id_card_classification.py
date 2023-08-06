import numpy as np
import cv2
import onnxruntime


def preprocessing(image):
    return np.expand_dims(cv2.resize(image, (224, 224)), axis=0)


class idcardclassONNX:
    def __init__(self, model_file='model.onnx', session=None):
        assert model_file is not None
        self.model_file = model_file
        self.ort = onnxruntime.InferenceSession(self.model_file, providers=["CUDAExecutionProvider"])

    def predict(self, image):
        input = self.ort.get_inputs()[0].name
        output_names = self.ort.get_outputs()[0].name
        return np.argmax(self.ort.run([output_names], {input: preprocessing(image).astype('float32')})[0]), \
            np.max(self.ort.run([output_names], {input: preprocessing(image).astype('float32')})[0][0])

    # 0: back_cccd , 1: back_cmnd, 2:front_cccd , 3: front_cmnd
