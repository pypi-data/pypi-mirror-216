from ..commons.config import Config
from ..modules.corner_detection.id_card_aligment import align_image
from ..modules.mrc.utils import mrc_crop_model, mrc_detect_model
from ..modules.passport.passport_detection import passport_detect_model


class MergeIdCardModel(object):
    def __init__(self):
        pass

    @staticmethod
    def detect_corner(image, mrc=False):
        if mrc:
            detection_boxes, detection_scores, detection_classes, df = mrc_crop_model.detect_objects(image)
            return align_image(image, detection_boxes, df)
        else:
            detection_boxes, detection_scores, detection_classes, df = Config().load_all_models(
                crop_mode=True).detect_objects(
                image)
            return align_image(image, detection_boxes, df)

    @staticmethod
    def recognize_fe(image, mrc=False, passport=False):
        if mrc:
            detection_boxes, detection_score, detection_classes, df = mrc_detect_model.detect_objects(image)
            return df, detection_boxes
        elif passport:
            detection_boxes, detection_score, detection_classes, df = passport_detect_model.detect_objects(image)
            return df, detection_boxes
        else:
            detection_boxes, detection_score, detection_classes, df = Config().load_all_models(
                front_side=True).detect_objects(image)
            return df, detection_boxes

    @staticmethod
    def recognize_be(image):
        detection_boxes, detection_score, detection_classes, df = Config().load_all_models(
            back_side=True).detect_objects(image)
        return df, detection_boxes

    @staticmethod
    def classify_card(image):
        return Config().load_all_models(classify_mode=True).predict(image)
