import numpy as np
import cv2


def non_max_suppression_fast(boxes, labels, overlapThresh):
    if len(boxes) == 0:
        return [0]
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    pick = []

    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        overlap = (w * h) / area[idxs[:last]]

        idxs = np.delete(idxs, np.concatenate(([last],
                                               np.where(overlap > overlapThresh)[0])))

    final_labels = [labels[idx] for idx in pick]
    final_boxes = boxes[pick].astype("int")

    return final_boxes, final_labels


# Tim midpoint cua box
def get_center_point(tensor):
    x_mid = (tensor[0] + tensor[2]) / 2  # (Xmin + Xmax)/2
    y_mid = (tensor[1] + tensor[3]) / 2  # (Ymin + Ymax)/2
    point = [x_mid, y_mid]
    return point


def find_miss_corner(coordinate_dict):
    position_name = ['top_left', 'top_right', 'bottom_left', 'bottom_right']
    position_index = np.array([0, 0, 0, 0])

    for name in coordinate_dict.keys():
        if name in position_name:
            position_index[position_name.index(name)] = 1

    index = np.argmin(position_index)

    return index


# Tim vi tri cua goc bi thieu
def calculate_missed_coord_corner(coordinate_dict):
    thresh = 0

    index = find_miss_corner(coordinate_dict)

    # calculate missed corner coordinate
    # case 1: missed corner is "top_left"
    if index == 0:
        midpoint = np.add(coordinate_dict['top_right'], coordinate_dict['bottom_left']) / 2
        y = 2 * midpoint[1] - coordinate_dict['bottom_right'][1] - thresh
        x = 2 * midpoint[0] - coordinate_dict['bottom_right'][0] - thresh
        coordinate_dict['top_left'] = (x, y)
    elif index == 1:  # "top_right"
        midpoint = np.add(coordinate_dict['top_left'], coordinate_dict['bottom_right']) / 2
        y = 2 * midpoint[1] - coordinate_dict['bottom_left'][1] - thresh
        x = 2 * midpoint[0] - coordinate_dict['bottom_left'][0] - thresh
        coordinate_dict['top_right'] = (x, y)
    elif index == 2:  # "bottom_left"
        midpoint = np.add(coordinate_dict['top_left'], coordinate_dict['bottom_right']) / 2
        y = 2 * midpoint[1] - coordinate_dict['top_right'][1] - thresh
        x = 2 * midpoint[0] - coordinate_dict['top_right'][0] - thresh
        coordinate_dict['bottom_left'] = (x, y)
    elif index == 3:  # "bottom_right"
        midpoint = np.add(coordinate_dict['bottom_left'], coordinate_dict['top_right']) / 2
        y = 2 * midpoint[1] - coordinate_dict['top_left'][1] - thresh
        x = 2 * midpoint[0] - coordinate_dict['top_left'][0] - thresh
        coordinate_dict['bottom_right'] = (x, y)

    return coordinate_dict


def perspective_transform(image, source_points):
    dest_points = np.float32([[0, 0], [640, 0], [640, 480], [0, 480]])
    M = cv2.getPerspectiveTransform(source_points, dest_points)
    return cv2.warpPerspective(image, M, (640, 480))


# def perspective_transform(image, source_points):
#     dest_points = np.float32([[0, 0], [640, 0], [640, 384], [0, 384]])
#     M = cv2.getPerspectiveTransform(source_points, dest_points)
#     return cv2.warpPerspective(image, M, (640, 384))


def check_label(boxes, label):
    final_boxes, final_labels = non_max_suppression_fast(boxes, label, 0.3)
    final_points = list(map(get_center_point, final_boxes))
    label_boxes = dict(zip(final_labels, final_points))
    key = ['top_left', 'top_right', 'bottom_left', 'bottom_right']
    return label_boxes, key
