from ..text_detection.dictionary import IDcardPreprocessing
from ...commons.merge_model import MergeIdCardModel
from ..text_detection.utils import *
from ...tools.api_json import *
from typing import Tuple
from JustScan.config.logger import setup_logger
logging = setup_logger(__name__)


def get_mrc_alignment(image: np.array) -> Tuple[np.array, dict]:
    try:
        crop_model = MergeIdCardModel().detect_corner(image, mrc=True)
        return crop_model
    except:
        logging.error(f'error at running {get_mrc_alignment.__name__}, cannot process mrc')
        raise HTTPException(status_code=400,
                            detail={'status': 400, 'code': 'MRC_CANNOT_ALIGN',
                                    'error': 'cannot process mrc'})


def get_extracted_field(field_dict, label_con_concate, bbox_json):
    return {key: [d[key] for d in (field_dict, label_con_concate, bbox_json)] for key in field_dict}


def get_feature_mrc(image: str):
    df_front, front_boxes_detect = MergeIdCardModel().recognize_fe(image, mrc=True)
    if len(front_boxes_detect) == 0:
        return None
    label = df_front[:, 0]
    confidence = df_front[:, 1]
    ids = df_front[:, 2]
    final_boxes, final_labels, final_confidence, final_ids = non_max_suppression_fast(front_boxes_detect, label,
                                                                                      confidence, ids,
                                                                                      overlapThresh=0.3)

    label_con_concate = dict(zip(final_labels, final_confidence))
    return final_boxes, final_ids, label_con_concate


def get_mrc(image):
    final_boxes, final_ids, label_con_concate = get_feature_mrc(image)
    list_ans, name_boxes, engine_boxes, add_boxes, chassis_boxes, brand_boxes, model_boxes, date_expiry_boxes, date_first_boxes, plate_boxes = IDcardPreprocessing().mrc_process(
        final_boxes, final_ids)
    bbox_mrc = {'name': merge_bboxes(name_boxes), 'add': merge_bboxes(add_boxes),
                'engine': merge_bboxes(engine_boxes),
                'chassis': merge_bboxes(chassis_boxes), 'brand': brand_boxes[0],
                'model': model_boxes[0], 'date_expiry': merge_bboxes(date_expiry_boxes),
                'date_first': date_first_boxes[0], 'plate': merge_bboxes(plate_boxes)}
    name = len(name_boxes)
    engine = len(name_boxes) + len(engine_boxes)
    add = len(engine_boxes) + len(name_boxes) + len(add_boxes)
    chassis = len(engine_boxes) + len(name_boxes) + len(add_boxes) + len(chassis_boxes)
    brand = len(brand_boxes)
    model = len(model_boxes)
    plate = len(plate_boxes)
    expir = len(date_expiry_boxes)
    extracted_field = get_extracted_field(
        IDcardPreprocessing().mrc_dict(image, list_ans, name, engine, add, chassis, brand, model, expir, plate),
        label_con_concate,
        bbox_mrc)

    return mrc(extracted_field=extracted_field, confidence=1.0)
