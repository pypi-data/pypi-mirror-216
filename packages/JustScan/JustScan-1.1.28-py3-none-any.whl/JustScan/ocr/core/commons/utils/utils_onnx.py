import numpy as np
from fastapi import HTTPException
from JustScan.config.logger import setup_logger

logging = setup_logger(__name__)


def nms(boxes, scores, iou_threshold):
    sorted_indices = np.argsort(scores)[::-1]

    keep_boxes = []
    while sorted_indices.size > 0:
        box_id = sorted_indices[0]
        keep_boxes.append(box_id)
        keep_indices = np.where(compute_iou(boxes[box_id, :], boxes[sorted_indices[1:], :]) < iou_threshold)[0]

        sorted_indices = sorted_indices[keep_indices + 1]

    return keep_boxes


def compute_iou(box, boxes):
    xmin = np.maximum(box[0], boxes[:, 0])
    ymin = np.maximum(box[1], boxes[:, 1])
    xmax = np.minimum(box[2], boxes[:, 2])
    ymax = np.minimum(box[3], boxes[:, 3])
    union_area = (box[2] - box[0]) * (box[3] - box[1]) + (boxes[:, 2] - boxes[:, 0]) * (
            boxes[:, 3] - boxes[:, 1]) - np.maximum(0, xmax - xmin) * np.maximum(0, ymax - ymin)

    return np.maximum(0, xmax - xmin) * np.maximum(0, ymax - ymin) / union_area


def xywh2xyxy(x):
    # Convert bounding box (x, y, w, h) to bounding box (x1, y1, x2, y2)
    y = np.copy(x)
    y[..., 0] = x[..., 0] - x[..., 2] / 2
    y[..., 1] = x[..., 1] - x[..., 3] / 2
    y[..., 2] = x[..., 0] + x[..., 2] / 2
    y[..., 3] = x[..., 1] + x[..., 3] / 2
    return y


def get_label(scores, class_ids, class_names):
    try:
        return np.column_stack((
            np.array(class_names)[class_ids.astype(int)],
            scores.astype(float),
            class_ids.astype(int)
        ))
    except Exception as e:
        logging.error(f'Error running {get_label.__name__}: {e}. Low-quality image. Please try again')
        raise HTTPException(status_code=400,
                            detail={'status': 400, 'code': 'IMAGE_QUALITY_NOT_GOOD_EXCEPTION',
                                    'error': 'Low-quality image. Please try again'})
