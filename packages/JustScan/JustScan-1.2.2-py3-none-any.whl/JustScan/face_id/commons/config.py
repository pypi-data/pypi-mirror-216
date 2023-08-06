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
    model_path = home + "/.itc_ocr/onnx_model/{}.onnx".format(model_name)
    return model_path


def get_model(url, face_detection=False, face_recognition=False, face_liveness=False, face_mask=False, oce=False):
    model_mapping = {
        face_detection: 'det_10g',
        face_recognition: 'w600k_r50',
        face_liveness: 'face_liveness',
        face_mask: 'face_mask',
        oce: 'oce'
    }

    model_name = model_mapping.get(True)
    return save_dir(url, model_name)


config = {
    'face_detection': get_model(
        url='https://drive.google.com/u/3/uc?id=1rx36SrN5fnjOrWe9pzICUf8CrJ5MKJz3&export=download',
        face_detection=True),
    'face_recognition': get_model(
        url='https://drive.google.com/u/3/uc?id=15E7InoVailY1FxxIuliucOFrRKzY0dkL&export=download',
        face_recognition=True),
    'face_liveness': get_model(
        url='https://drive.google.com/u/3/uc?id=1bsOOUUElO8qXLDLQBb4OnA66lc-pDJ25&export=download',
        face_liveness=True),
    'face_mask': get_model(
        url='https://drive.google.com/u/3/uc?id=1Gg-PUSYkvDGyowDZWOQK0Dg2XGg_yznQ&export=download',
        face_mask=True),
    'oce': get_model(
        url='https://drive.google.com/u/3/uc?id=1PnWAf8phX38h-wvVdiNooI-nM8Els_TJ&export=download',
        oce=True)
}