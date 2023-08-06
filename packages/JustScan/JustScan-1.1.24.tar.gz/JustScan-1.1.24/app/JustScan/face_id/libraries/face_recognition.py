from ..commons.ArcFace.ArcFace_onnx import ArcFaceONNX
from typing import Tuple
from ..tools.modules import to_base64
import numpy as np

rec = ArcFaceONNX()
rec.prepare(0)


def get_feature(image: np.array) -> np.array:
    return rec.get(image)


def calculate_embedding(img: np.array) -> Tuple[np.array, str]:
    img_b64 = to_base64(img)
    encode = rec.get(img)
    return encode, img_b64
