from ..commons.id_card_onnx import ID_CARD
# from ..commons.id_card_trt import ID_CARD
from ..commons.id_card_classification import idcardclassONNX
import gdown
from pathlib import Path
import os


def initialize_folder():
    """Initialize the folder for storing weights and models.

    Raises:
        OSError: if the folder cannot be created.
    """
    home = get_model_home()
    OCRHomePath = home + "/.itc_ocr"
    weightsPath = OCRHomePath + "/onnx_model"

    if not os.path.exists(OCRHomePath):
        os.makedirs(OCRHomePath, exist_ok=True)

    if not os.path.exists(weightsPath):
        os.makedirs(weightsPath, exist_ok=True)


def get_model_home():
    """Get the home directory for storing weights and models.

    Returns:
        str: the home directory.
    """
    return str(os.getenv("ITC_AI_HOME", default=str(Path.home())))


def save_dir(url, model_name):
    url_ = url
    initialize_folder()
    home = get_model_home()

    if not os.path.isfile(home + "/.itc_ocr/onnx_model/{}.onnx".format(model_name)):
        output = home + "/.itc_ocr/onnx_model/{}.onnx".format(model_name)
        gdown.download(url_, output, quiet=False)
    if not os.path.isfile(home + "/.itc_ocr/trt_model/{}.engine".format(model_name)):
        output = home + "/.itc_ocr/trt_model/{}.engine".format(model_name)
        gdown.download(url_, output, quiet=False)
    model_path = home + "/.itc_ocr/onnx_model/{}.onnx".format(model_name)
    trt_model_path = home + "/.itc_ocr/trt_model/{}.engine".format(model_name)
    return model_path, trt_model_path


def get_model(url, onnx_mode=True, front_side=False, back_side=False, crop_nid=False, classify=False,
              anti_spoof=False, passport_crop=False, passport_detect=False,
              mrc_crop=False, mrc_detect=False, encoder=False, decoder=False):
    model_mapping = {
        front_side: 'ScanIDcard_640x480',
        back_side: 'FasterScanNIDBackSide',
        crop_nid: 'lightweight_crop_cccd',
        classify: 'idcard_classify_simplified',
        anti_spoof: 'nid_liveness_check',
        passport_crop: 'crop_passport',
        passport_detect: 'detect_passport',
        mrc_crop: 'mrc_corner',
        mrc_detect: 'mrc_detect',
        encoder: 'transformer_encoder',
        decoder: 'transformer_decoder'
    }

    model_name = model_mapping.get(True)
    onnx_path, trt_path = save_dir(url, model_name)
    if not onnx_mode:
        return trt_path
    else:
        return onnx_path


config = {
    'corner_detection': {
        'corner_model': get_model(
            url='https://drive.google.com/u/3/uc?id=1DU25fdrthZx0Iz0wSblk1fFwHbMTeIuu&export=download',
            crop_nid=True),
    },
    'mrc_detection': {
        'mrc_crop_model': get_model(
            url='https://drive.google.com/u/3/uc?id=1jZnS36gLssQ7HfGJJgvARHn3039glBow&export=download',
            mrc_crop=True),
        'mrc_detect_model': get_model(
            url='https://drive.google.com/u/3/uc?id=17cZFLcgt5Ntbr3at1JsJhFc3NX9cyelA&export=download',
            mrc_detect=True)
    },
    'text_detection': {
        'cccd_front_model': get_model(
            url='https://drive.google.com/u/3/uc?id=1IAtd9iLZ0hps9l8XuXeMGcbKHuHxso3j&export=download',
            front_side=True),
        'cccd_back_model': get_model(
            url='https://drive.google.com/u/3/uc?id=1a1y5-lk5PcvbmYXWjcGJ81aZgnYbcZ-d&export=download',
            back_side=True),
    },
    'id_card_classification': {
        'classify_model': get_model(
            url='https://drive.google.com/u/3/uc?id=142eCovyWamP6Li_GDE5InzvGgolY7nSJ&export=download',
            classify=True)
    },
    'nid_spoofing': get_model(
        url='https://drive.google.com/u/3/uc?id=1-iEcuaBBPvziy1nySIWPRftOhiSRUHpj&export=download',
        anti_spoof=True),

    'passport': {
        'passport_crop': get_model(
            url='https://drive.google.com/u/3/uc?id=1fi5SeM3awCcA78pStEVxyCXDDWS1axHE&export=download',
            passport_crop=True),
        'passport_detect': get_model(
            url='https://drive.google.com/u/3/uc?id=1bzVxtkZJElSRFp5oDeZi_ueYBGxzLD8B&export=download',
            passport_detect=True)
    },
    'vietnamese_nlp':
        {
            'encoder': get_model(
                url='https://drive.google.com/u/3/uc?id=159JfNNVcHDKrV_00eM_Ve2Elui5nonIc&export=download',
                encoder=True),
            'decoder': get_model(
                url='https://drive.google.com/u/3/uc?id=1PUmuoD77dntBT1IWByO6TLNkVLcfH5Db&export=download',
                decoder=True)
        },
    'tensorrt_nlp':
        {
            'encoder': get_model(
                url='https://drive.google.com/u/3/uc?id=1iDPkpKDlauRkEZ3TjOjzEGIOLEMcwJc4&export=download',
                onnx_mode=False,
                encoder=True),
            'decoder': get_model(
                url='https://drive.google.com/u/3/uc?id=1gCkrx-s7joOQvBi-kvhnpJuOJY4fxe9H&export=download',
                onnx_mode=False,
                decoder=True)
        }
}


class Config(object):
    def __init__(self,
                 crop_model=config['corner_detection']['corner_model'],
                 classify_model=config['id_card_classification']['classify_model'],
                 back_side_model=config['text_detection']['cccd_back_model'],
                 front_side_model=config['text_detection']['cccd_front_model']
                 ):
        self.crop_model = crop_model
        self.classify_model = classify_model
        self.back_side_model = back_side_model
        self.front_side_model = front_side_model

    def load_all_models(self):
        classify = idcardclassONNX(
            model_file=self.classify_model
        )
        crop = ID_CARD(
            path=self.crop_model,
            class_name=['top_left', 'top_right', 'bottom_left', 'bottom_right'],
            yolov5=True
        )
        front_side = ID_CARD(
            path=self.front_side_model,
            class_name=[
                'qr', 'id', 'name', 'birth', 'gender', 'country',
                'home', 'add', 'valid'
            ],
            yolov5=True)
        back_side = ID_CARD(
            path=self.back_side_model,
            class_name=[
                'qr', 'id', 'name', 'birth', 'gender', 'country',
                'home', 'add', 'valid', 'personal_iden',
                'create_date', 'police_sign', 'left_finger', 'right_finger', 'mrz'
            ],
            yolov5=True
        )
        return classify, crop, front_side, back_side
