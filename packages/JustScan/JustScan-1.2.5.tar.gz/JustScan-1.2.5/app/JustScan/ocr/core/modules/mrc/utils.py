from ...commons.id_card_onnx import ID_CARD
from ...commons.config import config

class_corner = ['top_left', 'top_right', 'bottom_left', 'bottom_right']
class_mrc = ['name', 'engine', 'add', 'chassis', 'brand', 'model', 'date_expiry', 'date_first', 'plate']

mrc_crop_model = ID_CARD(path=config['mrc_detection']['mrc_crop_model'], conf_thres=0.3,
                         iou_thres=0.45,
                         class_name=class_corner)
mrc_detect_model = ID_CARD(path=config['mrc_detection']['mrc_detect_model'], conf_thres=0.3,
                           iou_thres=0.45,
                           class_name=class_mrc)


