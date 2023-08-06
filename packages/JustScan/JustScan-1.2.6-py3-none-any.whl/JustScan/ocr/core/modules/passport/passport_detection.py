from ...commons.id_card_onnx import ID_CARD
from ...commons.config import config
class_passport = ['type_passport', 'passport', 'name', 'national', 'birth', 'place_o_birth', 'gender', 'id',
                  'date_o_issues',
                  'date_o_expiry', 'place_o_issues']
passport_detect_model = ID_CARD(path=config['passport']['passport_detect'],
                                conf_thres=0.35,
                                iou_thres=0.45,
                                class_name=class_passport)
