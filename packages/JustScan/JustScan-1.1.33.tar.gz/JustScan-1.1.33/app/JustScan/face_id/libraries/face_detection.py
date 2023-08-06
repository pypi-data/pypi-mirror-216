import numpy as np
from ..commons.ScrFd.scrfd import SCRFD
from ..commons.config import config
from ..tools.modules import to_base64, alignment_procedure
from ..commons.FaceMask.face_mask_onnx import FaceMask
from ..commons.AntiSpoof.liveness_check import livenesss_predict
from ..commons.AntiSpoof.liveness_onnx_check import onnx_predict
from ..commons.CloseEyes.close_eyes_v2 import CloseEyes, crop_eye
from ..commons.FaceQuality.face_quality_assessment import QualityCheck
from ..commons.AntiSpoof.CDCN_config import predict_liveness
from fastapi import HTTPException
import base64
from JustScan.config.logger import setup_logger, timeit

logging = setup_logger(__name__)
detector = SCRFD(config['face_detection'])
check_mask = FaceMask()
eyes = CloseEyes()
detector.prepare(0)


@timeit(logging)
def extract_face(img_path):
    bbox, kps = detector.autodetect(img_path)
    resp = {}
    for idx, face in enumerate(bbox):
        label = 'face_' + str(idx + 1)
        landmarks = {
            "right_eye": kps[idx][0].tolist(),
            "left_eye": kps[idx][1].tolist(),
            "nose": kps[idx][2].tolist(),
            "mouth_right": kps[idx][3].tolist(),
            "mouth_left": kps[idx][4].tolist()
        }
        resp[label] = {
            "score": face[4],
            "facial_area": face[0:4].astype(int).tolist(),
            "landmarks": landmarks
        }

    return resp, kps


@timeit(logging)
def analyze_facial(img_path, align=True):
    output = []
    obj, _ = extract_face(img_path)
    # if type(obj) is dict:
    for key in obj:
        identity = obj[key]
        facial_area = identity["facial_area"]
        confidence = identity['score']
        facial_img = img_path[facial_area[1]: facial_area[3],
                     facial_area[0]: facial_area[2]]
        landmarks = identity["landmarks"]
        if confidence > 0.7 and align:
            # if align:
            left_eye = landmarks["left_eye"]
            right_eye = landmarks["right_eye"]
            nose = landmarks["nose"]

            facial_img = alignment_procedure(
                facial_img, right_eye, left_eye, nose)

        result = {
            'facial_area':
                {
                    'startX': float(facial_area[0]),
                    'startY': float(facial_area[1]),
                    'endX': float(facial_area[2]),
                    'endY': float(facial_area[3])
                },
            'confidence': float(confidence),
            'landmarks':
                {
                    'right_eye': landmarks['right_eye'],
                    'left_eye': landmarks['left_eye'],
                    'nose': landmarks['nose'],
                    'mouth_right': landmarks['mouth_right'],
                    'mouth_left': landmarks['mouth_left']
                },
            'faces_b64': to_base64(facial_img),
            'faces_nparray': facial_img
        }

        output.append(result)
    return output


@timeit(logging)
def get_face_location(image):
    result = analyze_facial(image)

    if len(result) == 1:
        return result
    elif len(result) > 1:
        logging.error(f'error at running {get_face_location.__name__}, multiple faces detected')
        raise HTTPException(status_code=400, detail={
            'status': '400', 'code': 'MULTI_FACE_DETECTED', 'error': 'multi face deteted'})
    else:
        logging.error(f'error at running {get_face_location.__name__}, cannot detect face')
        raise HTTPException(status_code=400, detail={
            'status': '400', 'code': 'FACE_NOT_DETECTED', 'error': 'cannot detect face'})


@timeit(logging)
def multi_face_check(image):
    result = analyze_facial(image)
    if len(result) == 1:
        return {'result': {"isMultipleFaces": False}}
    elif len(result) > 1:
        return {'result': {"isMultipleFaces": True}}
    else:
        logging.error(f'error at running {get_face_location.__name__}, cannot detect face')
        raise HTTPException(status_code=400, detail={
            'status': '400', 'code': 'FACE_NOT_DETECTED', 'error': 'cannot detect face'})


@timeit(logging)
def close_eyes_check(face_nparray, left_eye, right_eye):
    left_eyes, right_eyes = crop_eye(face_nparray, left_eye, right_eye)
    labels_left_eyes, confidence_left_eyes = eyes.predict(left_eyes)
    labels_right_eyes, confidence_right_eyes = eyes.predict(right_eyes)
    confidence_eyes = (confidence_left_eyes + confidence_right_eyes) / 2
    eye_check = labels_left_eyes + labels_right_eyes

    eye_check_result = True if eye_check == 2 or eye_check == 1 else False
    return eye_check_result, confidence_eyes


@timeit(logging)
def face_occlusion(face_nparray: np.array, image, left_eye, right_eye):
    occlusion_type = []
    label_eyes, confidence_eyes = close_eyes_check(image, left_eye, right_eye)
    label_mask, confidence_mask = check_mask.predict(face_nparray)
    label_mask = False if label_mask == 1 else True
    isOccluded = True if label_mask == True or label_eyes == True else False
    review = True if confidence_eyes < 0.6 or confidence_mask < 0.6 else False
    if label_mask:
        occlusion_type.append('mask')
    if label_eyes:
        occlusion_type.append('eyes')

    return {
        'occluded': isOccluded,
        'type': occlusion_type,
        'confidence': [confidence_mask, confidence_eyes],
        'toBeReview': review
    }


@timeit(logging)
def liveness_detection(face_nparray: np.array):
    labels_spoof, confidence_spoof = livenesss_predict(face_nparray)
    return {
        'live': True if labels_spoof == 1 else False,
        # 'confidence': confidence_spoof,
        # 'toBeReview': True if confidence_spoof < 0.6 else False
    }


@timeit(logging)
def liveness_detection_cdcn(face_nparray: np.array):
    label = predict_liveness(face_nparray)
    return {
        'live': True if label == 1 else False,
        # 'confidence': 0.1,
        # 'toBeReview': False
    }


@timeit(logging)
def liveness_detection_onnx(face_nparray: np.array):
    labels_spoof, confidence_spoof = onnx_predict(face_nparray)
    return {
        'live': True if labels_spoof == 1 else False,
        'confidence': confidence_spoof,
        'toBeReview': True if confidence_spoof < 0.6 else False
    }


@timeit(logging)
def selfie_face_check(image: base64):
    final_result = []
    faces = get_face_location(image)

    for face in faces:
        face_nparray = face.get('faces_nparray')
        right_eye = face.get('landmarks')['right_eye']
        left_eye = face.get('landmarks')['left_eye']
        occlusion = face_occlusion(face_nparray, image, left_eye, right_eye)
        liveness = liveness_detection_onnx(face_nparray)

        quality_check = {
            'liveness': liveness,
            'occlusion': occlusion
        }
        final_result.append(quality_check)
    return {'result': final_result}


@timeit(logging)
def check_image_quality(image):
    faces = get_face_location(image)
    for face in faces:
        face_array = face.get('faces_nparray')
        result = check_image_qual(face_array, min_blur=120)
    return {'result': result}


@timeit(logging)
def check_image_qual(image, min_blur=100):
    return QualityCheck(min_blur).calculate_quality(image)
