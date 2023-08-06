from fastapi import HTTPException
from typing import Tuple
from ...commons.merge_model import MergeIdCardModel
import numpy as np
from JustScan.config.logger import setup_logger
logging = setup_logger(__name__)


def process_classification(image: np.array) -> Tuple[np.ndarray, list, float]:
    # return label, confidence
    label, confidence = MergeIdCardModel().classify_card(image)
    if label is None or label in [1, 3] or confidence < 0.8:
        logging.error(f'error at running {process_classification.__name__}, ID card not found')
        raise HTTPException(status_code=404,
                            detail={
                                'status': 404,
                                'code': 'ID_CARD_NOT_FOUND',
                                'error': 'ID card not found. Please try again'
                            }
                            )
    else:
        return label, confidence, image
