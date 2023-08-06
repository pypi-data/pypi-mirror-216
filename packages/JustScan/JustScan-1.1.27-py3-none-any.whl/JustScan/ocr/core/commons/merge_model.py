from ..modules.corner_detection.id_card_aligment import align_image
from ..commons.config import Config
from ..modules.mrc.utils import mrc_crop_model, mrc_detect_model
from ..modules.passport.passport_detection import passport_detect_model

classify, crop, front_side, back_side = Config().load_all_models()


class MergeIdCardModel(object):
    def __init__(self):
        pass

    @staticmethod
    def detect_corner(image, mrc=False):
        if mrc:
            detection_boxes, detection_scores, detection_classes, df = mrc_crop_model.detect_objects(image)
            return align_image(image, detection_boxes, df)
        else:
            detection_boxes, detection_scores, detection_classes, df = crop.detect_objects(
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
            detection_boxes, detection_score, detection_classes, df = front_side.detect_objects(image)
            return df, detection_boxes

    @staticmethod
    def recognize_be(image):
        detection_boxes, detection_score, detection_classes, df = back_side.detect_objects(image)
        return df, detection_boxes

    @staticmethod
    def classify_card(image):
        return classify.predict(image)
