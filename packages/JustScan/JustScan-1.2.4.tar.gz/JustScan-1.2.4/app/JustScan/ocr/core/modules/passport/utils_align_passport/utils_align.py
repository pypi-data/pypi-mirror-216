import numpy as np
import cv2


def non_max_suppression_fast(boxes, labels, overlapThresh):
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
    return final_boxes, final_labels


def four_corner(xmin, ymin, xmax, ymax):
    # top_left = [xmin - xmax / 2, ymin - ymax / 2]
    # top_right = [xmin + xmax / 2, ymin - ymax / 2]
    # bottom_left = [xmin - xmax / 2, ymin + ymax / 2]
    # bottom_right = [xmin + xmax / 2, ymin + ymax / 2]
    top_left = [xmin, ymin]
    top_right = [xmax, ymin]
    bottom_left = [xmin, ymax]
    bottom_right = [xmax, ymax]
    dic = {'top_left': top_left, 'top_right': top_right,
           'bottom_left': bottom_left, 'bottom_right': bottom_right}
    # {'top_right': [619.0, 1059.5], 'bottom_right': [126.0, 1023.0], 'bottom_left': [130.0, 248.5],
    #  'top_left': [628.0, 227.0]}
    return dic


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


def check_label(boxes, label):
    final_boxes, final_labels = non_max_suppression_fast(boxes, label, 0.3)
    # final_points = list(map(four_corner(), final_boxes))
    # label_boxes = dict(zip(final_labels, final_points))
    label_boxes = four_corner(final_boxes[0][0], final_boxes[0][1], final_boxes[0][2], final_boxes[0][3])
    key = ['top_left', 'top_right', 'bottom_left', 'bottom_right']
    return label_boxes, key
