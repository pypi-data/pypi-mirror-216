from .dictionaries import DictionaryCCCD
from fastapi import HTTPException
from typing import Tuple
from scipy.ndimage import interpolation as inter
from ..commons.merge_model import MergeIdCardModel
from JustScan.config.logger import setup_logger
import numpy as np
import cv2

logging = setup_logger(__name__)


def correct_skew(image, delta=1, limit=5):
    def determine_score(arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1, dtype=float)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2, dtype=float)
        return score

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    for angle in angles:
        score = determine_score(thresh, angle)
        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
    corrected = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, \
            borderMode=cv2.BORDER_REPLICATE)

    return corrected


def hdr(image):
    l, a, b = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2LAB))
    return cv2.cvtColor(cv2.merge([cv2.createCLAHE(clipLimit=1., tileGridSize=(8, 8)).apply(l), a, b]), cv2.COLOR_LAB2BGR)


def get_alignment_image(image: np.array) -> Tuple[np.array, dict]:
    try:
        crop_model = MergeIdCardModel().detect_corner(image)
        return hdr(correct_skew(crop_model))
    except:
        logging.error(f'error at running {get_alignment_image.__name__}, cannot align id card')
        raise HTTPException(status_code=400,
                            detail={'status': 400, 'code': 'ID_CARD_NOT_ALIGN',
                                    'error': 'Cannot align id card'})


def get_result_id_card(image_alignment, label_classify, confidence):
    dict = DictionaryCCCD().get_result(image=image_alignment,
                                       label_classify=label_classify, confidence=confidence)
    if dict is not None:
        return dict
    else:
        logging.error(f'error at running {get_result_id_card.__name__}, low quality image')
        raise HTTPException(status_code=400,
                            detail={'status': 400, 'code': 'IMAGE_QUALITY_NOT_GOOD_EXCEPTION',
                                    'error': 'Low-quality image. Please try again.'})

