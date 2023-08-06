import cv2
import io
import numpy as np
import base64
from fastapi import HTTPException
from .logger import setup_logger

# Set up the logger
logging = setup_logger(__name__)

# Constant for recognition initialization
RECOGNITION_INIT = 0.2


def process_input_b64(image_b64: base64) -> bytes:
    """
    Decode a Base64-encoded image string into bytes.

    Args:
        image_b64 (base64): Base64-encoded image string.

    Returns:
        bytes: Decoded image in bytes.

    Raises:
        HTTPException: If there is an error during decoding.
    """
    try:
        return base64.b64decode(image_b64)
    except:
        logging.error(f'Error at running {process_input_b64.__name__}: Invalid image format')
        raise HTTPException(status_code=400, detail={'status': 400, 'code': 'INVALID_IMAGE_FORMAT',
                                                     'error': 'Invalid image format'})


def process_input(file: bytes) -> np.array:
    """
    Convert a byte array into a NumPy array.

    Args:
        file (bytes): Input byte array.

    Returns:
        np.array: NumPy array representing the input data.
    """
    return np.asarray(bytearray(io.BytesIO(file).read()), dtype=np.uint8)


def processing_image(file: str) -> np.array:
    """
    Process an image file and return a NumPy array.

    Args:
        file (str): Path or name of the image file.

    Returns:
        np.array: NumPy array representing the processed image.
    """
    return cv2.imdecode(process_input(process_input_b64(file)), cv2.IMREAD_COLOR)
