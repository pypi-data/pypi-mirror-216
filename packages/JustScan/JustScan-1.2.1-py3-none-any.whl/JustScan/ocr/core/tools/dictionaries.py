from ..modules.text_detection.dictionary import IDcardPreprocessing
from ..modules.text_detection.utils import *
from ..commons.merge_model import MergeIdCardModel
from .api_json import *
from fastapi import HTTPException


class DictionaryCCCD(object):
    def __init__(self):
        pass

    def get_result(self, image: str, label_classify: int, confidence: float) -> list:

        if label_classify == 2:
            final_boxes, final_ids, label_con_concate = self.get_feature_front(image)
            list_ans, id_boxes, name_boxes, birth_boxes, gender_boxes, country_boxes, home_boxes, add_boxes, valid_boxes = IDcardPreprocessing().cccd_front_process(
                final_boxes=final_boxes, final_ids=final_ids)
            bbox_front_json = {'id': id_boxes[0], 'name': merge_bboxes(name_boxes), 'birth': birth_boxes[0],
                               'gender': gender_boxes[0], 'country': country_boxes[0],
                               'home': merge_bboxes(home_boxes), 'add': merge_bboxes(add_boxes),
                               'valid': valid_boxes[0]}
            return cccd_front(extracted_field=self.get_extracted_field(
                IDcardPreprocessing().cccd_front_dict(image, list_ans, name_boxes, add_boxes),
                label_con_concate, bbox_front_json), confidence=confidence)

        elif label_classify == 0:
            final_boxes, final_ids, label_con_concate = self.get_feature_back(image)
            list_ans, personal_iden_boxes, create_date_boxes, police_sign_boxes, mrz_boxes = IDcardPreprocessing().cccd_back_process(
                final_boxes=final_boxes,
                final_ids=final_ids)
            bbox_back_json = {'personal_iden': merge_bboxes(personal_iden_boxes),
                              'create_date': create_date_boxes[0],
                              'police_sign': merge_bboxes(police_sign_boxes)}
            return cccd_back(extracted_field=self.get_extracted_field(
                IDcardPreprocessing().cccd_back_dict(image, list_ans, personal_iden_boxes, mrz_boxes),
                label_con_concate, bbox_back_json), confidence=confidence)
        else:
            raise HTTPException(status_code=400,
                                detail={'status': 400, 'code': 'ID_CARD_NOT_FOUND',
                                        'error': 'ID card not found. Please try again'})

    @staticmethod
    def get_extracted_field(field_dict, label_con_concate, bbox_json):
        return {key: [d[key] for d in (field_dict, label_con_concate, bbox_json)] for key in field_dict}

    @staticmethod
    def get_feature_front(image: str):
        df_front, front_boxes_detect = MergeIdCardModel().recognize_fe(image)
        if len(front_boxes_detect) == 0:
            return None
        # final_boxes, final_labels, final_confidence, final_ids = non_max_suppression_fast(front_boxes_detect,
        #                                                                                   df_front['class_name'],
        #                                                                                   df_front['confidence'],
        #                                                                                   df_front['class_id'],
        #                                                                                   overlapThresh=0.3)
        final_boxes, final_labels, final_confidence, final_ids = non_max_suppression_fast(front_boxes_detect,
                                                                                          df_front[:, 0],
                                                                                          df_front[:, 1],
                                                                                          df_front[:, 2],
                                                                                          overlapThresh=0.3)
        return final_boxes, final_ids, dict(zip(final_labels, final_confidence))

    @staticmethod
    def get_feature_back(image: str):
        df_back, back_boxes_detect = MergeIdCardModel().recognize_be(image)
        if len(back_boxes_detect) == 0:
            raise HTTPException(status_code=400,
                                detail={'status': 400, 'code': 'IMAGE_QUALITY_NOT_GOOD_EXCEPTION',
                                        'error': 'Low-quality image. Please try again.'})
        # final_boxes, final_labels, final_confidence, final_ids = non_max_suppression_fast(back_boxes_detect,
        #                                                                                   df_back['class_name'],
        #                                                                                   df_back['confidence'],
        #                                                                                   df_back['class_id'],
        #                                                                                   overlapThresh=0.3)
        final_boxes, final_labels, final_confidence, final_ids = non_max_suppression_fast(back_boxes_detect,
                                                                                          df_back[:, 0],
                                                                                          df_back[:, 1],
                                                                                          df_back[:, 2],
                                                                                          overlapThresh=0.3)
        return final_boxes, final_ids, dict(zip(final_labels, final_confidence))
