import onnxruntime
import numpy as np
import cv2
from JustScan.face_id.commons.config import config


class FaceMask:
    def __init__(self, model_file=config['face_mask'], session=None):
        assert model_file is not None
        self.model_file = model_file
        self.session = session

    def predict(self, image):
        ort = onnxruntime.InferenceSession(self.model_file, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        input = ort.get_inputs()[0].name
        output = ort.get_outputs()
        output_names = []
        for out in output:
            output_names.append(out.name)
        img = cv2.resize(image, (224, 224))
        img = np.expand_dims(img, axis=0)
        net = ort.run(output_names, {input: img.astype('float32')})[0]
        confidence = np.max(net[0])
        ids = np.argmax(net[0])
        return ids, confidence
