import cv2
import numpy as np
import math
from .dom import DOM

MIN_SHARPNESS = 0.46
MIN_CONTRAST = 0.35
MIN_BRIGHTNESS = 0.3
MIN_BLUR = 100


class QualityCheck(object):
    def __init__(self, min_blur=MIN_BLUR):
        self.min_sharpness = MIN_SHARPNESS
        self.min_contrast = MIN_CONTRAST
        self.min_brightness = MIN_BRIGHTNESS
        self.min_blur = MIN_BLUR

    def calculate_quality(self, image):
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

        return {'sharpness': sharpness,
                'contrast': contrast,
                'brightness': brightness,
                'blur': blur,
                'quality': True if sum_reason == 0 else False,
                'reason': reason}

    def reason(self, compared_sharpness, compared_contrast, compared_brightness, compared_blur):
        reason_dict = {
            'sharpness': compared_sharpness,
            'contrast': compared_contrast,
            'brightness': compared_brightness,
            'blur': compared_blur
        }
        list_quality = [key for key, value in reason_dict.items() if value]
        return list_quality
