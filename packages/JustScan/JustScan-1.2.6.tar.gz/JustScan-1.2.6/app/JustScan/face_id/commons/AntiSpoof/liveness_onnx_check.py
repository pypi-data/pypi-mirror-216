import numpy as np
import onnxruntime as ort
import cv2
from JustScan.face_id.commons.config import config

model_path = config['face_liveness']


def onnx_predict(img, model_paths=model_path):
    img = cv2.resize(img, (112, 112))
    dummy_face = np.expand_dims(np.array(img, dtype=np.float32), axis=0)

    providers = ['CPUExecutionProvider']
    m = ort.InferenceSession(model_paths, providers=providers)
    onnx_pred = m.run(['activation_5'], {"input": dummy_face})
    label = np.argmax(onnx_pred)
    confidence = np.max(onnx_pred[0][0])
    return label, confidence


# def preprocessing(image):
#     # img = image[:,:,::-1]
#     img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     img = cv2.resize(img, (112, 112))
#     return np.expand_dims(img, axis=0)
#
#
# class FaceLivenessCheck:
#     def __init__(self, model_file='app/face_id/modeling/anti_spoof_models/face_liveness.onnx'):
#         assert model_file is not None
#         self.model_file = model_file
#         self.ort = onnxruntime.InferenceSession(self.model_file)
#
#     def predict(self, image):
#         img = preprocessing(image)
#         inputs = self.ort.get_inputs()[0].name
#         output_names = self.ort.get_outputs()[0].name
#         net = self.ort.run([output_names], {inputs: img.astype('float32')})[0]
#         ids = np.argmax(net)
#         confidence = np.max(net[0])
#         return ids, confidence
