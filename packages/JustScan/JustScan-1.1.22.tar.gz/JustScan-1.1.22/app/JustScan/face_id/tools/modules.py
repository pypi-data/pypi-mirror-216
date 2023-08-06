from PIL import Image
import cv2
import math
import base64
import numpy as np
import onnxruntime as ort
from fastapi import HTTPException
from JustScan.config.logger import setup_logger, timeit

logging = setup_logger(__name__)


def image_bgr(image) -> np.array:
    img_BGR = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return img_BGR


def image_bgr2rgb(image) -> np.array:
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return img_rgb


# convert cv2 to base64
def to_base64(img: np.array) -> base64:
    _, buf = cv2.imencode(".png", img)
    return base64.b64encode(buf)


# convert base64 cv2
def from_base64(buf: base64) -> np.array:
    buf_decode = base64.b64decode(buf)
    buf_arr = np.frombuffer(buf_decode, dtype=np.uint8)
    return cv2.imdecode(buf_arr, cv2.IMREAD_COLOR)


# convert byte to np.array
def byte2array(byte, dtype=np.float32) -> np.array:
    array_return = np.frombuffer(byte, dtype=dtype)
    return array_return


def findEuclideanDistance(source_representation, test_representation):
    euclidean_distance = source_representation - test_representation
    euclidean_distance = np.sum(np.multiply(euclidean_distance, euclidean_distance))
    euclidean_distance = np.sqrt(euclidean_distance)
    return euclidean_distance


def alignment_procedure(img, left_eye, right_eye, nose):
    # this function aligns given face in img based on left and right eye coordinates

    # left eye is the eye appearing on the left (right eye of the person)
    # left top point is (0, 0)
    try: 
        left_eye_x, left_eye_y = left_eye
        right_eye_x, right_eye_y = right_eye

        # -----------------------
        # decide the image is inverse

        center_eyes = (int((left_eye_x + right_eye_x) / 2), int((left_eye_y + right_eye_y) / 2))

        # if False:
        #     img = cv2.circle(img, (int(left_eye[0]), int(left_eye[1])), 2, (0, 255, 255), 2)
        #     img = cv2.circle(img, (int(right_eye[0]), int(right_eye[1])), 2, (255, 0, 0), 2)
        #     img = cv2.circle(img, center_eyes, 2, (0, 0, 255), 2)
        #     img = cv2.circle(img, (int(nose[0]), int(nose[1])), 2, (255, 255, 255), 2)

        # -----------------------
        # find rotation direction

        if left_eye_y > right_eye_y:
            point_3rd = (right_eye_x, left_eye_y)
            direction = -1  # rotate same direction to clock
        else:
            point_3rd = (left_eye_x, right_eye_y)
            direction = 1  # rotate inverse direction of clock

        # -----------------------
        # find length of triangle edges

        a = findEuclideanDistance(np.array(left_eye), np.array(point_3rd))
        b = findEuclideanDistance(np.array(right_eye), np.array(point_3rd))
        c = findEuclideanDistance(np.array(right_eye), np.array(left_eye))

        # -----------------------

        # apply cosine rule

        if b != 0 and c != 0:  # this multiplication causes division by zero in cos_a calculation

            cos_a = (b * b + c * c - a * a) / (2 * b * c)

            cos_a = min(1.0, max(-1.0, cos_a))

            angle = np.arccos(cos_a)  # angle in radian
            angle = (angle * 180) / math.pi  # radian to degree

            # -----------------------
            # rotate base image

            if direction == -1:
                angle = 90 - angle

            img = Image.fromarray(img)
            img = np.array(img.rotate(direction * angle))

        # -----------------------

        return img  # return img anyway
    except:
        logging.error(f'error at running {alignment_procedure.__name__}, cannot extract face')
        raise HTTPException(status_code=400, detail={
            'status': '400', 'code': 'CANT_EXTRACT_FACE', 'error': 'cannot extract face'})


def load_model_ort(model_path):
    ort_session = ort.InferenceSession(model_path)

    return ort_session


def get_image(img_path):
    img = cv2.imdecode(img_path, cv2.IMREAD_COLOR)
    return img

