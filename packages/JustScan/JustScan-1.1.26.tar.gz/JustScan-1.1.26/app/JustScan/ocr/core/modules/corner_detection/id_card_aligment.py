from .utils import *
from fastapi import HTTPException
from JustScan.config.logger import setup_logger

logging = setup_logger(__name__)


def align_image(image, boxes_crop, df_crop):
    label_boxes, _ = check_label(boxes_crop, df_crop[:, 0])
    if len(label_boxes) == 3:
        coordinate_dict = calculate_missed_coord_corner(label_boxes)
        source_points = np.float32(
            [coordinate_dict['top_left'], coordinate_dict['top_right'], coordinate_dict['bottom_right'],
             coordinate_dict['bottom_left']])
        return perspective_transform(image, source_points)

    elif len(label_boxes) == 4:
        source_points = np.float32(
            [label_boxes['top_left'], label_boxes['top_right'], label_boxes['bottom_right'],
             label_boxes['bottom_left']])
        return perspective_transform(image, source_points)
    else:
        logging.error(f'error at running {align_image.__name__}, cannot align id card')
        raise HTTPException(status_code=400,
                            detail={'status': 400, 'code': 'ID_CARD_NOT_ALIGN',
                                    'error': 'Cannot align id card'})
