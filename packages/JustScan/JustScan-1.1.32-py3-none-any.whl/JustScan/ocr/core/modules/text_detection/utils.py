from fastapi import HTTPException
from JustScan.config.logger import setup_logger
from datetime import datetime
import numpy as np
import cv2
import re

logging = setup_logger(__name__)


def non_max_suppression_fast(boxes, labels, confidence, ids, overlapThresh):
    outs = dict()
    if len(boxes) == 0:
        out = {
            'result': 'error'
        }
        outs.update(out)
        return outs

    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    # x1 = boxes[:, 0]
    # y1 = boxes[:, 1]
    # x2 = boxes[:, 2]
    # y2 = boxes[:, 3]
    # area = (boxes[:, 2] - boxes[:, 0] + 1) * (boxes[:, 3] - boxes[:, 1] + 1)

    # compute the overlaps using numpy functions
    # overlaps = np.zeros((len(boxes), len(boxes)))
    # mask = np.ones(len(boxes), dtype=bool)
    for i in range(len(boxes)):
        xx1 = np.maximum(boxes[:, 0][i], boxes[:, 0])
        yy1 = np.maximum(boxes[:, 1][i], boxes[:, 1])
        xx2 = np.minimum(boxes[:, 2][i], boxes[:, 2])
        yy2 = np.minimum(boxes[:, 3][i], boxes[:, 3])

        # w = np.maximum(0, xx2 - xx1 + 1)
        # h = np.maximum(0, yy2 - yy1 + 1)

        np.zeros((len(boxes), len(boxes)))[i, :] = (np.maximum(0, xx2 - xx1 + 1) * np.maximum(0, yy2 - yy1 + 1)) / (
                    boxes[:, 2] - boxes[:, 0] + 1) * (boxes[:, 3] - boxes[:, 1] + 1)
        if np.ones(len(boxes), dtype=bool)[i]:
            overlap_indices = np.where(np.zeros((len(boxes), len(boxes)))[i] > overlapThresh)[0]
            np.ones(len(boxes), dtype=bool)[overlap_indices] = False
            np.ones(len(boxes), dtype=bool)[i] = True

    final_labels = labels[np.ones(len(boxes), dtype=bool)]
    final_boxes = boxes[np.ones(len(boxes), dtype=bool)].astype("int")
    final_confidence = confidence[np.ones(len(boxes), dtype=bool)].astype("float")
    final_ids = ids[np.ones(len(boxes), dtype=bool)].astype('int')
    return final_boxes, final_labels, final_confidence, final_ids


def perspective_transoform(image, source_points, point):
    # x = point[0]
    # y = point[1]
    dest_points = np.float32([[0, 0], [point[0], 0], [0, point[1]], [point[0], point[1]]])
    # M = cv2.getPerspectiveTransform(source_points, dest_points)
    return cv2.warpPerspective(image, cv2.getPerspectiveTransform(source_points, dest_points), (point[0], point[1]))


def automatic_brightness_and_contrast(gray, clip_hist_percent) -> tuple:
    hist, _ = np.histogram(gray.flatten(), 256, [0, 256])
    clip_hist_percent *= (np.cumsum(hist)[-1] / 100.0)
    clip_hist_percent /= 2.0

    minimum_gray = np.argmax(np.cumsum(hist) > clip_hist_percent)
    maximum_gray = np.argmax(np.cumsum(hist) >= (np.cumsum(hist)[-1] - clip_hist_percent)) - 1

    return cv2.convertScaleAbs(gray, alpha=255 / (maximum_gray - minimum_gray),
                               beta=-minimum_gray * 255 / (maximum_gray - minimum_gray))


def remove_noise(image, back_side=False):
    if back_side:
        diff_img = 255 - cv2.absdiff(
            cv2.cvtColor(
                cv2.resize(image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC), cv2.COLOR_BGR2GRAY),
            cv2.medianBlur(cv2.dilate(cv2.cvtColor(
                cv2.resize(image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC), cv2.COLOR_BGR2GRAY),
                np.ones((7, 7), np.uint8)), 29))
        return automatic_brightness_and_contrast(
            cv2.bilateralFilter(
                cv2.morphologyEx(cv2.merge([diff_img, diff_img, diff_img]), cv2.MORPH_CLOSE, cv2.getStructuringElement(
                    cv2.MORPH_RECT, (1, 1))), 5, 75, 75), 3)
    else:
        diff_img = 255 - cv2.absdiff(cv2.cvtColor(
            cv2.resize(image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC), cv2.COLOR_BGR2GRAY),
            cv2.medianBlur(
                cv2.dilate(
                    cv2.cvtColor(
                        cv2.resize(image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC), cv2.COLOR_BGR2GRAY),
                    np.ones((7, 7), np.uint8)), 29))
        return automatic_brightness_and_contrast(
            cv2.GaussianBlur(
                cv2.bilateralFilter(
                    cv2.morphologyEx(
                        cv2.merge([diff_img, diff_img, diff_img]), cv2.MORPH_CLOSE,
                        cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))), 5, 75, 75), (5, 5), 0), 4)


def sort_text_front(detection_boxes, detection_ids):
    try:
        # detection_ids = np.array(detection_ids)
        return tuple(
            [sort_each_category(detection_boxes[np.array(detection_ids) == category]) for category in range(1, 9)])
    except (TypeError, ValueError):
        logging.error(f'error at running {sort_text_front.__name__}, image quality not good')
        raise HTTPException(status_code=400,
                            detail={
                                'status': 400,
                                'code': 'IMAGE_QUALITY_NOT_GOOD',
                                'error': 'image quality not good'
                            }
                            )


def sort_text_back(detection_boxes, detection_labels):
    try:
        # detection_labels = np.array(detection_labels)
        category_boxes = {}
        for label in [9, 10, 11, 14]:
            category_boxes[label] = sort_each_category(detection_boxes[np.array(detection_labels) == label],
                                                       back_side=True if label == 14 else False)
        return tuple(category_boxes.values())
    except:
        logging.error(f'error at running {sort_text_back.__name__}, image quality not good')
        raise HTTPException(status_code=400,
                            detail={
                                'status': 400,
                                'code': 'IMAGE_QUALITY_NOT_GOOD',
                                'error': 'image quality not good'
                            }
                            )


def get_y1(x):
    return x[1]


def get_x1(x):
    return x[0]


def sort_mrc_text(detection_boxes, detection_ids):
    try:
        detection_ids = np.array(detection_ids)
        return tuple([sort_each_category(detection_boxes[detection_ids == category]) for category in range(0, 9)])
    except (TypeError, ValueError):
        logging.error(f'error at running {sort_mrc_text.__name__}, mrc card image quality not good')
        raise HTTPException(status_code=400,
                            detail={
                                'status': 400,
                                'code': 'IMAGE_QUALITY_NOT_GOOD',
                                'error': 'mrc card image quality not good'
                            }
                            )


def sort_mrc_category(category_text_boxes):
    min_y1 = min(category_text_boxes, key=get_y1)[1]
    category_text_boxes = np.stack(category_text_boxes)
    mask = np.where(category_text_boxes[:, 1] < min_y1 + 10, True, False)
    line1_text_boxes = category_text_boxes[mask]
    return line1_text_boxes


def sort_each_category(category_text_boxes, back_side=False):
    # min_y1 = min(category_text_boxes, key=get_y1)[1]
    # max_y1 = max(category_text_boxes, key=get_y1)[1]
    mean_y1 = int((min(category_text_boxes, key=get_y1)[1] + max(category_text_boxes, key=get_y1)[1]) / 2)
    category_text_boxes = np.stack(category_text_boxes)
    if back_side:
        line1_text_boxes = category_text_boxes[
            np.where(category_text_boxes[:, 1] < min(category_text_boxes, key=get_y1)[1] + 10, True, False)]
        line3_text_boxes = category_text_boxes[
            np.where(category_text_boxes[:, 1] > max(category_text_boxes, key=get_y1)[1] - 10, True, False)]
        line2_text_boxes = category_text_boxes[
            np.where((category_text_boxes[:, 1] < mean_y1 + 10) & (category_text_boxes[:, 1] > mean_y1 - 10), True,
                     False)]

        line1_text_boxes = sorted(line1_text_boxes, key=get_x1)
        line2_text_boxes = sorted(line2_text_boxes, key=get_x1)
        line3_text_boxes = sorted(line3_text_boxes, key=get_x1)
        merged_text_boxes = [*line1_text_boxes, *line2_text_boxes, *line3_text_boxes]
    else:
        mask = np.where(category_text_boxes[:, 1] < min(category_text_boxes, key=get_y1)[1] + 10, True, False)
        line1_text_boxes = category_text_boxes[mask]
        line2_text_boxes = category_text_boxes[np.invert(mask)]

        line1_text_boxes = sorted(line1_text_boxes, key=get_x1)
        line2_text_boxes = sorted(line2_text_boxes, key=get_x1)

        merged_text_boxes = [*line1_text_boxes, *line2_text_boxes] if len(line2_text_boxes) else line1_text_boxes
    return merged_text_boxes


def crop_recogn(img, boxes, back_side=False):
    if len(boxes) == 0:
        return [0]
    detect_image = []
    for i in range(len(boxes)):
        # xmin = boxes[i][0]
        # ymin = boxes[i][1]
        # xmax = boxes[i][2]
        # ymax = boxes[i][3]

        new_img = perspective_transoform(img, np.float32([[boxes[i][0], boxes[i][1]],
                                                          [boxes[i][2], boxes[i][1]],
                                                          [boxes[i][0], boxes[i][3]],
                                                          [boxes[i][2], boxes[i][3]]]),
                                         [boxes[i][2] - boxes[i][0], boxes[i][3] - boxes[i][1]])  # Cat anh cua tung box
        if new_img is None:
            continue
        detect_image.append(remove_noise(new_img, back_side=back_side))
    return detect_image


def merge_bboxes(bboxes, delta_x=0.1, delta_y=0.1):
    def is_in_bbox(point, bbox):
        return bbox[0] <= point[0] <= bbox[2] and bbox[1] <= point[1] <= bbox[3]

    def intersect(bbox, bbox_):
        for i in range(int(len(bbox) / 2)):
            for j in range(int(len(bbox) / 2)):
                if is_in_bbox([bbox[2 * i], bbox[2 * j + 1]], bbox_):
                    return True
        return False

    while True:
        nb_merge = 0
        used = []
        new_bboxes = []
        for i, b in enumerate(bboxes):
            tmp_bbox = None
            for j, b_ in enumerate(bboxes[i + 1:]):
                j += i + 1
                if j in used:
                    continue
                bmargin = [b[0] - (b[2] - b[0]) * delta_x, b[1] - (b[3] - b[1]) * delta_y,
                           b[2] + (b[2] - b[0]) * delta_x, b[3] + (b[3] - b[1]) * delta_y]
                b_margin = [b_[0] - (b_[2] - b_[0]) * delta_x, b_[1] - (b_[3] - b_[1]) * delta_y,
                            b_[2] + (b_[2] - b_[0]) * delta_x, b_[3] + (b_[3] - b_[1]) * delta_y]

                if intersect(bmargin, b_margin) or intersect(b_margin, bmargin):
                    tmp_bbox = [min(b[0], b_[0]), min(b[1], b_[1]), max(b_[2], b[2]), max(b[3], b_[3])]
                    used.append(j)
                    nb_merge += 1
            if tmp_bbox:
                new_bboxes.append(tmp_bbox)
            elif i not in used:
                new_bboxes.append(b)
            used.append(i)
        if nb_merge == 0:
            break
        bboxes = new_bboxes

    return new_bboxes[0]


def parse_date(date_str):
    matches = [re.match(r'(\d{2})(\d{2})/(\d{4})', date_str), re.match(r'(\d{2})(\d{2})(\d{4})', date_str),
               re.match(r'(\d{2})/(\d{2})(\d{4})', date_str)]

    for match in matches:
        if match:
            day = match.group(1)
            month = match.group(2)
            year = match.group(3)
            date_format = f'{day}-{month}-{year}'
            return datetime.strptime(date_format, '%d-%m-%Y').strftime('%d/%m/%Y')

    return date_str
