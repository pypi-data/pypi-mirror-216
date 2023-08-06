from functools import wraps

CMND_FRONT_DICT = {'id': 'NO', 'name': 'FULL_NAME', 'birth': 'DATE_OF_BIRTH',
                   'home': 'PLACE_OF_ORIGIN', 'add': 'PLACE_OF_RESIDENCE'}
CMND_BACK_DICT = {'ethnic': 'ETHNIC', 'religion': 'RELIGION', 'personal_iden': 'PERSONAL_IDENTIFICATION',
                  'date_of_issue': 'DATE_OF_ISSUE', 'police_sign': 'APPROVED_BY'}
CCCD_FRONT_DICT = {'id': 'NO', 'name': 'FULL_NAME', 'birth': 'DATE_OF_BIRTH', 'gender': 'GENDER',
                   'country': 'NATIONALITY', 'home': 'PLACE_OF_ORIGIN', 'add': 'PLACE_OF_RESIDENCE',
                   'valid': 'DATE_OF_EXPIRY'}
CCCD_BACK_DICT = {'personal_iden': 'PERSONAL_IDENTIFICATION',
                  'create_date': 'DATE_OF_ISSUE',
                  'police_sign': 'APPROVED_BY'}

MRC_BACK_DICT = {
    'name': 'OWNER_FULL_NAME',
    'add': 'ADDRESS',
    'engine': 'ENGINE',
    'chassis': 'CHASSIS',
    'brand': 'BRAND',
    'model': 'MODEL',
    'date_expiry': 'DATE_OF_EXPIRY',
    'date_first': 'DATE_OF_FIRST',
    'plate': 'LICENSE_PLATE'
}

PASSPORT_FRONT_DICT = {
    'type_passport': 'TYPE',
    'passport': 'PASSPORT_ID',
    'name': 'FULL_NAME',
    'national': 'NATIONAL',
    'birth': 'BIRTH',
    'place_o_birth': 'PLACE_OF_BIRTH',
    'gender': 'GENDER',
    'id': 'ID_CARD_NUMBER',
    'date_o_issues': 'DATE_OF_ISSUES',
    'date_o_expiry': 'DATE_OF_EXPIRY',
    'place_o_issues': 'PLACE_OF_ISSUES'
}


# 'create_date': 'DATE_OF_ISSUE',

def format_decorator(type_id_card: str, side_id_card: str, key_dict: dict, mrc=False, passport=False) -> list:
    def operate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            output_ocr = []
            for field in key_dict.keys():
                type_ = key_dict.get(field)
                if kwargs['extracted_field'].get(field):
                    value, confidence_, (x, y, w, h) = kwargs['extracted_field'][field]
                    location = {'x': x, 'y': y, 'w': w, 'h': h}
                else:
                    value = 'UNKNOWN'
                    confidence_ = 0
                    location = {'x': 0, 'y': 0, 'w': 0, 'h': 0}
                output = {
                    "type": type_,
                    "value": value,
                    "confidence": confidence_,
                    "location": location
                }
                output_ocr.append(output)
                if mrc:
                    header_id_card = [
                        {
                            "type": "MRC_CARD",
                            "value": type_id_card,
                            "confidence": float(kwargs['confidence'])
                        },

                        {
                            "type": "SIDE",
                            "value": side_id_card,
                            "confidence": float(kwargs['confidence'])
                        }]
                elif passport:
                    header_id_card = [
                        {
                            "type": "PASSPORT",
                            "value": type_id_card,
                            "confidence": float(kwargs['confidence'])
                        },

                        {
                            "type": "SIDE",
                            "value": side_id_card,
                            "confidence": float(kwargs['confidence'])
                        }]
                else:
                    header_id_card = [
                        {
                            "type": "ID_CARD_TYPE",
                            "value": type_id_card,
                            "confidence": float(kwargs['confidence'])
                        },

                        {
                            "type": "SIDE",
                            "value": side_id_card,
                            "confidence": float(kwargs['confidence'])
                        }]
            result = header_id_card + output_ocr
            return result

        return wrapper

    return operate


@format_decorator(type_id_card='MRC', side_id_card='BACK', key_dict=MRC_BACK_DICT, mrc=True)
def mrc(extracted_field: dict, confidence: float) -> list:
    return


@format_decorator(type_id_card='PASSPORT', side_id_card='FRONT', key_dict=PASSPORT_FRONT_DICT,mrc=False, passport=True)
def passport(extracted_field: dict, confidence: float) -> list:
    return


@format_decorator(type_id_card='CMND', side_id_card='FRONT', key_dict=CMND_FRONT_DICT)
def cmnd_front(extracted_field: dict, confidence: float) -> list:
    return


@format_decorator(type_id_card='CMND', side_id_card='BACK', key_dict=CMND_BACK_DICT)
def cmnd_back(extracted_field: dict, confidence: float) -> list:
    concat_date_of_issue = "".join(
        [extracted_field['day'][0], '/', extracted_field['month'][0], '/', extracted_field['year'][0]])
    confidence_date_of_issue = ((float(extracted_field['day'][1]) +
                                 float(extracted_field['month'][1]) + float(extracted_field['year'][1])) / 3)

    extracted_field['date_of_issue'] = [concat_date_of_issue,
                                        confidence_date_of_issue, extracted_field['day'][2][0:4]]
    return None


@format_decorator(type_id_card='CCCD', side_id_card='FRONT', key_dict=CCCD_FRONT_DICT)
def cccd_front(extracted_field: dict, confidence: float) -> list:
    return


@format_decorator(type_id_card='CCCD', side_id_card='BACK', key_dict=CCCD_BACK_DICT)
def cccd_back(extracted_field: dict, confidence: float) -> list:
    return
