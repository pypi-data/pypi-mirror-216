from fastapi import HTTPException
import numpy as np
import cv2
from JustScan.config.logger import setup_logger
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

    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    area = (x2 - x1 + 1) * (y2 - y1 + 1)

    # compute the overlaps using numpy functions
    overlaps = np.zeros((len(boxes), len(boxes)))
    mask = np.ones(len(boxes), dtype=bool)
    for i in range(len(boxes)):
        xx1 = np.maximum(x1[i], x1)
        yy1 = np.maximum(y1[i], y1)
        xx2 = np.minimum(x2[i], x2)
        yy2 = np.minimum(y2[i], y2)

        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        overlaps[i, :] = (w * h) / area
        if mask[i]:
            overlap_indices = np.where(overlaps[i] > overlapThresh)[0]
            mask[overlap_indices] = False
            mask[i] = True

    final_labels = labels[mask]
    final_boxes = boxes[mask].astype("int")
    final_confidence = confidence[mask].astype("float")
    final_ids = ids[mask].astype('int')
    return final_boxes, final_labels, final_confidence, final_ids


def perspective_transoform(image, source_points, point):
    x = point[0]
    y = point[1]
    dest_points = np.float32([[0, 0], [x, 0], [0, y], [x, y]])
    M = cv2.getPerspectiveTransform(source_points, dest_points)
    return cv2.warpPerspective(image, M, (x, y))


def automatic_brightness_and_contrast(gray, clip_hist_percent) -> tuple:
    hist, _ = np.histogram(gray.flatten(), 256, [0, 256])

    accumulator = np.cumsum(hist)
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum / 100.0)
    clip_hist_percent /= 2.0

    minimum_gray = np.argmax(accumulator > clip_hist_percent)
    maximum_gray = np.argmax(accumulator >= (maximum - clip_hist_percent)) - 1

    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha
    return cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)


def rotate_text(image):
    angle = 0
    center = (image.shape[1] // 2, image.shape[0] // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1)
    rotated = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    return rotated


def remove_noise(image):
    img = cv2.resize(image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dilated_img = cv2.dilate(gray, np.ones((7, 7), np.uint8))
    bg_img = cv2.medianBlur(dilated_img, 25)
    diff_img = 255 - cv2.absdiff(gray, bg_img)
    img_merge = cv2.merge([diff_img, diff_img, diff_img])
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    img_final = cv2.morphologyEx(img_merge, cv2.MORPH_CLOSE, kernel)
    img_final = cv2.GaussianBlur(img_final, (5, 5), 0)
    img_final = cv2.bilateralFilter(img_final, 5, 45, 45)
    img_final = cv2.convertScaleAbs(img_final, alpha=1.12, beta=0)
    return automatic_brightness_and_contrast(img_final, 3)


def sort_text_front(detection_boxes, detection_ids):
    try:
        detection_ids = np.array(detection_ids)
        return tuple([sort_each_category(detection_boxes[detection_ids == category]) for category in range(1, 9)])
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
        detection_labels = np.array(detection_labels)
        category_boxes = {}
        for label in [9, 10, 11, 14]:
            category_boxes[label] = sort_each_category(detection_boxes[detection_labels == label],
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


def sort_passport_text(detection_boxes, detection_ids):
    try:
        detection_ids = np.array(detection_ids)
        return tuple([sort_each_category(detection_boxes[detection_ids == category]) for category in range(0, 11)])
    except (TypeError, ValueError):
        logging.error(f'error at running {sort_passport_text.__name__}, passport card image quality not good')
        raise HTTPException(status_code=400,
                            detail={
                                'status': 400,
                                'code': 'IMAGE_QUALITY_NOT_GOOD',
                                'error': 'passport image quality not good'
                            }
                            )


def sort_passport_category(category_text_boxes):
    min_y1 = min(category_text_boxes, key=get_y1)[1]
    category_text_boxes = np.stack(category_text_boxes)
    mask = np.where(category_text_boxes[:, 1] < min_y1 + 10, True, False)
    line1_text_boxes = category_text_boxes[mask]
    return line1_text_boxes


def sort_each_category(category_text_boxes, back_side=False):
    min_y1 = min(category_text_boxes, key=get_y1)[1]
    max_y1 = max(category_text_boxes, key=get_y1)[1]
    mean_y1 = int((min_y1 + max_y1) / 2)
    category_text_boxes = np.stack(category_text_boxes)
    if back_side:
        line1_text_boxes = category_text_boxes[np.where(category_text_boxes[:, 1] < min_y1 + 10, True, False)]
        line3_text_boxes = category_text_boxes[np.where(category_text_boxes[:, 1] > max_y1 - 10, True, False)]
        line2_text_boxes = category_text_boxes[
            np.where((category_text_boxes[:, 1] < mean_y1 + 10) & (category_text_boxes[:, 1] > mean_y1 - 10), True,
                     False)]

        line1_text_boxes = sorted(line1_text_boxes, key=get_x1)
        line2_text_boxes = sorted(line2_text_boxes, key=get_x1)
        line3_text_boxes = sorted(line3_text_boxes, key=get_x1)
        merged_text_boxes = [*line1_text_boxes, *line2_text_boxes, *line3_text_boxes]
    else:
        mask = np.where(category_text_boxes[:, 1] < min_y1 + 10, True, False)
        line1_text_boxes = category_text_boxes[mask]
        line2_text_boxes = category_text_boxes[np.invert(mask)]

        line1_text_boxes = sorted(line1_text_boxes, key=get_x1)
        line2_text_boxes = sorted(line2_text_boxes, key=get_x1)

        merged_text_boxes = [*line1_text_boxes, *line2_text_boxes] if len(line2_text_boxes) else line1_text_boxes
    return merged_text_boxes


def crop_recogn_passport(img, boxes):
    if len(boxes) == 0:
        return [0]
    detect_image = []
    for i in range(len(boxes)):
        xmin = boxes[i][0]
        ymin = boxes[i][1]
        xmax = boxes[i][2]
        ymax = boxes[i][3]

        point = [xmax - xmin, ymax - ymin]
        source_points = np.float32([[xmin, ymin],  # [[xmin,ymin] [xmax,ymin], [xmin,ymax],[xmax,ymax]]
                                    [xmax, ymin],
                                    [xmin, ymax],
                                    [xmax, ymax]])

        new_img = perspective_transoform(img, source_points, point)  # Cat anh cua tung box
        if new_img is None:
            continue

        new_img = remove_noise(new_img)
        detect_image.append(new_img)
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
