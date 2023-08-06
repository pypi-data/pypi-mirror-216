import onnxruntime as ort
import numpy as np
import cv2
import torch
import torchvision.transforms as transforms


CDCNpp_MODEL_PATH = 'app/face_id/modeling/anti_spoof_models/fas_v3.onnx'
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

class LNONNX:
    def __init__(self, model_file):
        assert model_file is not None
        self.model_file = model_file

    def preprocessing(self, image):
        # img = image.transpose(2, 0, 1)
        return np.expand_dims(image, axis=0)

    def predict(self, image):
        img = self.preprocessing(image)
        session = ort.InferenceSession(self.model_file)
        input = session.get_inputs()[0].name
        output = session.get_outputs()
        output_names = [out.name for out in output]

        net = session.run(output_names, {input: img.astype('float32')})[0]
        return net


transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])


def create_binary_mask(predicted_mask, threshold):
    # binary_masks = (binary_mask > threshold).float()
    binary_masks = np.zeros(predicted_mask.shape[:3], dtype=np.float32)
    for i in range(predicted_mask.shape[1]):
        for j in range(predicted_mask.shape[2]):
            if predicted_mask[0, i, j] > threshold:
                binary_masks[0, i, j] = 1.0
            else: 
                binary_masks[0,i,j] = 0
    return torch.from_numpy(binary_masks)


def predict_liveness(image):
    img = image[:,:,::-1]
    # cv2.imshow('a', img)
    # cv2.waitKey(0)
    img = transform(img)
    model = LNONNX(model_file=CDCNpp_MODEL_PATH)
    result = model.predict(img)
    result = torch.from_numpy(result)
    binary_mask = create_binary_mask(result, 0)
    map_score = torch.sum(result) / torch.sum(binary_mask)

    print(f'liveness mapscore: {map_score}')
    if map_score >= 1:
        label = 1
    else:
        label = 0
    # final_label = 'live' if label == 1 else 'Spoof'
    # print(final_label)
    return label