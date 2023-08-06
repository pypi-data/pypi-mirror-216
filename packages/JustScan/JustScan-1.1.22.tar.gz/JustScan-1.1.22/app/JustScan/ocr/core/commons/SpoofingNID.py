from ..commons.config import config
import numpy as np
import cv2
import onnxruntime


def preprocessing(image):
    # img = image[:,:,::-1]
    img = cv2.resize(image, (224, 224))
    return np.expand_dims(img, axis=0)


class SpoofingNIDModel:
    def __init__(self, model_file=config['nid_spoofing'], session=None):
        assert model_file is not None
        self.model_file = model_file
        self.ort = onnxruntime.InferenceSession(self.model_file, providers=["CUDAExecutionProvider"])

    def predict(self, image):
        img = preprocessing(image)
        input = self.ort.get_inputs()[0].name
        output_names = self.ort.get_outputs()[0].name
        net = self.ort.run([output_names], {input: img.astype('float32')})[0]
        return np.argmax(net), np.max(net[0])

    # 0: back_cccd , 1: back_cmnd, 2:front_cccd , 3: front_cmnd
