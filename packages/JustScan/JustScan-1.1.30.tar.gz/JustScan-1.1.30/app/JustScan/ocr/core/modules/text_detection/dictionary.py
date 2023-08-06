from ...commons.config import config
from ..text_detection.utils import *
# from ..vietnamese_nlp.nlp_onnx import VietnameseOCR
from ..vietnamese_nlp.nlp_trt import TensorRuntimeOCR
from ..vietnamese_nlp.vietocr.tool.config import Cfg
from ..spell_checking.corrector_v2 import Correction
from ..passport.utils_detect_passport.utils_detect import *


def config_trt():
    configs = Cfg.load_config_from_name('vgg_transformer')
    configs['device'] = 'cuda:0'
    configs['pretrained'] = False
    return configs


class IDcardPreprocessing(object):
    def __init__(self,
                 encode_path='/home/ec2-user/.itc_ocr/trt_model/transformer_encoder_trt.engine',
                 decode_path='/home/ec2-user/.itc_ocr/trt_model/transformer_decoder_trt.engine'):
        self.encode_path = encode_path
        self.decode_path = decode_path

    def recognize_text(self, image):
        return TensorRuntimeOCR(encoder_model=self.encode_path,
                                decoder_model=self.decode_path, config=config_trt()).predict_batch(image)

    def mrc_process(self, final_boxes, final_ids):
        name_boxes, engine_boxes, add_boxes, chassis_boxes, \
            brand_boxes, model_boxes, \
            date_expiry_boxes, date_first_boxes, plate_boxes = sort_mrc_text(final_boxes, final_ids)

        list_ans = list(name_boxes) + engine_boxes + add_boxes + chassis_boxes + brand_boxes + model_boxes + \
                   date_expiry_boxes + date_first_boxes + plate_boxes
        return list_ans, name_boxes, engine_boxes, add_boxes, chassis_boxes, \
            brand_boxes, model_boxes, \
            date_expiry_boxes, date_first_boxes, plate_boxes

    def passport_process(self, final_boxes, final_ids):
        type_boxes, \
            passport_boxes, \
            name_boxes, national_boxes, \
            birth_boxes, place_o_birth_boxes, \
            gender_boxes, id_boxes, date_i_boxes, date_e_boxes, place_i_boxes = sort_passport_text(final_boxes,
                                                                                                   final_ids)
        list_ans = list(
            type_boxes) + passport_boxes + name_boxes + national_boxes + birth_boxes + place_o_birth_boxes + gender_boxes + id_boxes + date_i_boxes + date_e_boxes + place_i_boxes
        return list_ans, type_boxes, \
            passport_boxes, \
            name_boxes, national_boxes, \
            birth_boxes, place_o_birth_boxes, \
            gender_boxes, id_boxes, date_i_boxes, date_e_boxes, place_i_boxes

    def passport_dict(self, image, list_image, passport_boxes, name_boxes, national_boxes, place_birth):
        field_dict = {}
        result = self.recognize_text(crop_recogn_passport(image, list_image))
        field_dict['type_passport'] = 'P'
        field_dict['passport'] = result[1]
        field_dict['name'] = ' '.join(result[len(passport_boxes) + 1:len(name_boxes) + len(national_boxes) + 1]).upper()
        field_dict['national'] = result[len(name_boxes) + len(national_boxes) + 1].title()
        field_dict['birth'] = result[len(name_boxes) + len(national_boxes) + 2]
        field_dict['birth'] = parse_date(field_dict['birth'])
        field_dict['place_o_birth'] = ' '.join(result[len(name_boxes) + len(national_boxes) + 3:len(name_boxes) + len(
            national_boxes) + len(place_birth) + 3]).upper()
        field_dict['gender'] = result[len(name_boxes) + len(national_boxes) + len(place_birth) + 3].capitalize()
        field_dict['id'] = result[len(name_boxes) + len(national_boxes) + len(place_birth) + 4]
        field_dict['date_o_issues'] = result[len(name_boxes) + len(national_boxes) + len(place_birth) + 5]
        field_dict['date_o_issues'] = parse_date(field_dict['date_o_issues'])
        field_dict['date_o_expiry'] = result[len(name_boxes) + len(national_boxes) + len(place_birth) + 6]
        field_dict['date_o_expiry'] = parse_date(field_dict['date_o_expiry'])
        field_dict['place_o_issues'] = ' '.join(
            result[len(name_boxes) + len(national_boxes) + len(place_birth) + 7:]).title()
        return field_dict

    def mrc_dict(self, image, list_image, name, engine, add, chassis, brand, model, expir, plate):
        field_dict = {}
        result = self.recognize_text(crop_recogn(image, list_image))
        field_dict['name'] = ' '.join(result[0:name])
        field_dict['engine'] = ''.join(result[name:engine])
        field_dict['add'] = ' '.join(result[engine:add])
        field_dict['chassis'] = ''.join(result[add:chassis])
        field_dict['brand'] = ' '.join(result[chassis:chassis + brand])
        field_dict['model'] = ' '.join(result[chassis + brand:chassis + brand + model])
        field_dict['date_expiry'] = '/'.join(result[chassis + brand + model:chassis + brand + model + expir])
        field_dict['date_first'] = ''.join(result[-plate - 1])
        field_dict['plate'] = '-'.join(result[-plate:])
        return field_dict

    def cccd_front_process(self, final_boxes, final_ids):
        id_boxes, name_boxes, birth_boxes, gender_boxes, country_boxes, home_boxes, add_boxes, valid_boxes = sort_text_front(
            final_boxes, final_ids)
        list_ans = list(
            id_boxes) + name_boxes + birth_boxes + gender_boxes + country_boxes + home_boxes + add_boxes + valid_boxes
        return list_ans, id_boxes, name_boxes, birth_boxes, gender_boxes, country_boxes, home_boxes, add_boxes, valid_boxes

    def cccd_front_dict(self, image, list_image, name_boxes, add_boxes):
        field_dict = {}
        result = self.recognize_text(crop_recogn(image, list_image))
        field_dict['id'] = result[0]
        field_dict['name'] = ' '.join(result[1:len(name_boxes) + 1]).upper()
        field_dict['birth'] = result[len(name_boxes) + 1]
        field_dict['gender'] = result[len(name_boxes) + 2].capitalize()
        field_dict['country'] = result[len(name_boxes) + 3].title()
        field_dict['home'] = ' '.join(result[len(name_boxes) + 4: -len(add_boxes) - 1]).title()
        field_dict['add'] = ' '.join(result[-len(add_boxes) - 1: -1]).title()
        field_dict['valid'] = result[-1]
        field_dict['valid'] = parse_date(field_dict['valid'])
        field_dict['birth'] = parse_date(field_dict['birth'])
        return field_dict

    def cccd_back_process(self, final_boxes, final_ids):
        personal_iden_boxes, create_date_boxes, police_sign_boxes, mrz_boxes = sort_text_back(
            final_boxes, final_ids)
        list_ans = list(create_date_boxes) + personal_iden_boxes + police_sign_boxes + mrz_boxes
        return list_ans, personal_iden_boxes, create_date_boxes, police_sign_boxes, mrz_boxes

    def cccd_back_dict(self, image, list_image, personal_iden_boxes, mrz_boxes):
        field_dict = {}
        result = self.recognize_text(crop_recogn(image, list_image, back_side=True))
        field_dict['personal_iden'] = ' '.join(
            Correction().retrieval(result[1:len(personal_iden_boxes) + 1])).capitalize()
        field_dict['create_date'] = result[0]
        field_dict['create_date'] = parse_date(field_dict['create_date'])
        field_dict['police_sign'] = ' '.join(result[len(personal_iden_boxes) + 1: -len(mrz_boxes)]).title()
        return field_dict
