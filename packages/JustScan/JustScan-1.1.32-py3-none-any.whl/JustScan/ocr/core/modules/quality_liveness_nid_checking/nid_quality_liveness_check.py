import cv2
import numpy as np
import math
from JustScan.face_id.commons.FaceQuality.dom import DOM
from ...commons.SpoofingNID import SpoofingNIDModel
from fastapi import HTTPException
from JustScan.config.logger import setup_logger

logging = setup_logger(__name__)

MIN_SHARPNESS = 0.46
MIN_CONTRAST = 0.35
MIN_BRIGHTNESS = 0.3
MIN_BLUR = 100


class NIDQualityLivenessCheck(object):
    def __init__(self, min_blur=MIN_BLUR):
        self.min_sharpness = MIN_SHARPNESS
        self.min_contrast = MIN_CONTRAST
        self.min_brightness = MIN_BRIGHTNESS
        self.min_blur = MIN_BLUR

    def nid_spoof_quality_check(self, image):
        try:
            label_spoof, confidence_spoof = SpoofingNIDModel().predict(image)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            sharpness = DOM().get_sharpness(gray) / math.sqrt(2)
            # mean, std = cv2.meanStdDev(gray)
            # contrast = float(std[0][0] / mean[0][0])
            contrast = DOM().get_contrast(gray)
            brightness = np.mean(gray) / 255
            blur = DOM().get_blur(gray)
            compared_sharpness = sharpness < self.min_sharpness
            compared_contrast = contrast < self.min_contrast
            compared_brightness = brightness < self.min_brightness
            compared_blur = blur < self.min_blur
            sum_reason = compared_brightness + compared_contrast + \
                         compared_sharpness + compared_blur
            reason = self.reason(
                compared_sharpness, compared_contrast, compared_brightness, compared_blur)
            return {'liveness': True if label_spoof == 0 else False,
                    'confidence': confidence_spoof,
                    'toBeReview': True if confidence_spoof < 0.5 else False,
                    'sharpness': sharpness,
                    'contrast': contrast,
                    'brightness': brightness,
                    'blur': blur,
                    'quality': False if sum_reason == 0 else True,
                    'reason': reason}
        except:
            logging.error(f'error at running {self.nid_spoof_quality_check.__name__}, ID card not found')
            raise HTTPException(status_code=404,
                                detail={
                                    'status': 404,
                                    'code': 'ID_CARD_NOT_FOUND',
                                    'error': 'ID card not found. Please try again'
                                }
                                )

    def reason(self, compared_sharpness, compared_contrast, compared_brightness, compared_blur):
        reason_dict = {
            'sharpness': compared_sharpness,
            'contrast': compared_contrast,
            'brightness': compared_brightness,
            'blur': compared_blur
        }
        list_quality = [key for key, value in reason_dict.items() if value]
        return list_quality
