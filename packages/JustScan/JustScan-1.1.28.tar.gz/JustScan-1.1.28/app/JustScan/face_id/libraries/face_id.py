from collections import defaultdict
from typing import Tuple
from ..tools.modules import *
from ..commons.ArcFace.ArcFace_onnx import ArcFaceONNX
from JustScan.database.crud import QueryData
from .face_detection import get_face_location
from .face_recognition import calculate_embedding, get_feature
from JustScan.config.config import RECOGNITION_INIT
from JustScan.config.logger import setup_logger, timeit

logging = setup_logger(__name__)
db = QueryData()
embedding = ArcFaceONNX()

@timeit(logging)
def detect_user(image: np.array) -> dict:
    result = get_face_location(image)
    return result


# register new image to system
@timeit(logging)
def register_image_id(image: np.array, metadata, face_id=None) -> np.array:
    db_encoder, img = calculate_embedding(image)
    id, created_at, updated_at = db.register_image(
        encoded_input=db_encoder, metadata=metadata)
    return img, id, created_at, updated_at

@timeit(logging)
def matched_images(encoding_dict: dict, encode_image: np.array, recognition_init: float) -> Tuple[dict, list]:
    id_result = []
    result_dict = []
    
    if encoding_dict:
        for db_id, db_encode in encoding_dict.items():

            dist, confidence = embedding.compute_sim(db_encode, encode_image)
            if dist > recognition_init:
                id = db_id
                id_result.append(id)
                result_dict.append({
                    'id': id, 'distance': dist, 'confidence': confidence
                })
    return result_dict, id_result

@timeit(logging)
def matched_info(list_key) -> list:
    return [db.select_imageid(i) for i in list_key]

@timeit(logging)
def get_matched_image(face: np.array):
    # face_nparray = from_base64(face)
    encoded_face = get_feature(face)
    matched, matched_id = matched_images(
        encode_image=encoded_face,
        encoding_dict=db.select_all_images(),
        recognition_init=RECOGNITION_INIT)
    return matched, matched_id

@timeit(logging)
def embedding_image(input_image_1: np.array):
    processed= get_face_location(input_image_1)

    return get_feature(processed[0].get('faces_nparray')), processed[0].get('faces_b64'),

@timeit(logging)
def comparing_faces(input1: np.array, input2: np.array):
    processed_nparray_1, input_b64_1 = embedding_image(input1)
    processed_nparray_2, input_b64_2 = embedding_image(input2)
    distance, confidence = embedding.compute_sim(processed_nparray_1, processed_nparray_2)
    result = {
        'verification_result': {
            'match': True if distance > 0.32 else False,
            'distance': distance,
            'confidence': confidence,
            'toBeReviewed': True if RECOGNITION_INIT <= distance < 0.32 else False
        },
        'input_image_1': input_b64_1,
        'input_image_2': input_b64_2
    }
    return {'result': result}

@timeit(logging)
def get_register(image, metadata):
    result = []
    faces = get_face_location(image)
    for i in faces:
        face = i.get('faces_nparray')
        matched, matched_id = get_matched_image(face)
        img, id, created_at, updated_at = register_image_id(face, metadata=metadata)
        # if there is matched face with new image
        if matched_id:
            matched_imageid = matched_id[0]
            face_id = db.get_matched_faceid(matched_imageid)
            # update images table with face_id
            db.update_faceid(id, face_id)
            db.update_face_updated_time(face_id=face_id, updated_at=created_at)
        else:
            face_id = db.register_face()
            db.update_faceid(id, face_id)

        result.append({
            # 'quality': quality,
            'image_id': id,
            'metadata': metadata,
            'created_at': created_at,
            'updated_at': updated_at,
            'face_id': face_id,
            'image': img,
            'matched_image': matched
        })
    return {'result': result}

@timeit(logging)
def get_recognize(image):
    images_append = []
    result_dict = defaultdict(list)
    result_unrecognize = []
    faces = get_face_location(image)
    for i in faces:
        face = i.get('faces_nparray')
        matched, matched_id = get_matched_image(face)
        if matched_id:
            result_list = matched_info(matched_id)
            # adding confidence to result_dict
            for i, c in zip(result_list, matched):
                image = {
                    'image_id': i.get('image_id'),
                    'face_id': i.get('face_id'),
                    'distance': c.get('distance'),
                    'confidence':c.get('confidence'),
                    'metadata': i.get('metadata'),
                    'created_at': i.get('created_at'),
                    'updated_at': i.get('updated_at'),
                }
                images_append.append(image)
                result_dict[image['face_id']].append(image)
        else:
            unrecognized = {
                'recognized': False,
                'face_id': None,
                'images': i.get('faces_b64')
            }
            result_unrecognize.append(unrecognized)
        result_output = [{'recognized': True, 'face_id': k, 'images': v}
                         for k, v in result_dict.items()]
        result_output.extend(result_unrecognize)
        return {'result': result_output}
