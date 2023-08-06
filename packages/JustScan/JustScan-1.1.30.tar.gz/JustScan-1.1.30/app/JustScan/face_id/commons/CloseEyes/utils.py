from fastapi import HTTPException
import numpy as np
from JustScan.config.logger import setup_logger, timeit

logging = setup_logger(__name__)


def extract_eye(image: np.array, left_eye_point, right_eye_point, rectangle_size=55) -> np.array:
    try:
        left_eye_rect = (
        left_eye_point[0] - rectangle_size, left_eye_point[1] - rectangle_size, left_eye_point[0] + rectangle_size,
        left_eye_point[1] + rectangle_size)
        right_eye_rect = (
        right_eye_point[0] - rectangle_size, right_eye_point[1] - rectangle_size, right_eye_point[0] + rectangle_size,
        right_eye_point[1] + rectangle_size)

        # Extract the eye images from the face image using the rectangle coordinates
        left_eye_img = image[int(left_eye_rect[1]):int(left_eye_rect[3]), int(left_eye_rect[0]):int(left_eye_rect[2])]
        right_eye_img = image[int(right_eye_rect[1]):int(right_eye_rect[3]),
                        int(right_eye_rect[0]):int(right_eye_rect[2])]
        return left_eye_img, right_eye_img
    except:
        logging.error(f'error at running {extract_eye.__name__}, cannot detect eye')
        raise HTTPException(status_code=400,
                            detail={'status': 400, 'code': 'CANNOT_DETECT_EYE',
                                    'error': 'Cannot detect eyes'})
