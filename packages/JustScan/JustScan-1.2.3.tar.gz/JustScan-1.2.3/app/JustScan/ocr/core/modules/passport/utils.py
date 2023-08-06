from ..text_detection.dictionary import IDcardPreprocessing
from ...commons.merge_model import MergeIdCardModel
from ..passport.utils_detect_passport.utils_detect import non_max_suppression_fast, merge_bboxes
from ...tools.api_json import passport


def get_extracted_field(field_dict, label_con_concate, bbox_json):
    return {key: [d[key] for d in (field_dict, label_con_concate, bbox_json)] for key in field_dict}


def get_feature_passport(image: str):
    df_front, front_boxes_detect = MergeIdCardModel().recognize_fe(image, passport=True)
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


def get_passport(image):
    final_boxes, final_ids, label_con_concate = get_feature_passport(image)
    list_ans, type_boxes, \
        passport_boxes, \
        name_boxes, national_boxes, \
        birth_boxes, place_o_birth_boxes, \
        gender_boxes, id_boxes, date_i_boxes, date_e_boxes, place_i_boxes = IDcardPreprocessing().passport_process(final_boxes, final_ids)
    bbox_passport = {'type_passport': type_boxes[0], 'passport': passport_boxes[0], 'name': merge_bboxes(name_boxes),
                     'national': national_boxes[0],
                     'birth': birth_boxes[0],
                     'place_o_birth': merge_bboxes(place_o_birth_boxes), 'gender': gender_boxes[0], 'id': id_boxes[0],
                     'date_o_issues': date_i_boxes[0], 'date_o_expiry': date_e_boxes[0],
                     'place_o_issues': merge_bboxes(place_i_boxes)}
    extracted_field = get_extracted_field(
        IDcardPreprocessing().passport_dict(image, list_ans, passport_boxes, name_boxes, national_boxes, place_o_birth_boxes),
        label_con_concate,
        bbox_passport)
    return passport(extracted_field=extracted_field, confidence=1.0)
