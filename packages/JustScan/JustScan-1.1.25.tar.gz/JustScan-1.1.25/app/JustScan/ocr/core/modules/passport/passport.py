import math
import time
import onnxruntime
from fastapi import HTTPException
from ...commons.config import config
from ..passport.utils_align_passport.utils_align import *
from ..passport.utils_align_passport.passport_utils import xywh2xyxy, nms, sigmoid, \
    get_label
from JustScan.config.logger import setup_logger
from scipy.ndimage import interpolation as inter

logging = setup_logger(__name__)


class Passport:

    def __init__(self, path, conf_thres=0.3, iou_thres=0.45, num_masks=32, class_name=None):
        self.conf_threshold = conf_thres
        self.iou_threshold = iou_thres
        self.num_masks = num_masks
        self.class_name = class_name

        # Initialize model
        self.initialize_model(path)

    def __call__(self, image):
        return self.segment_objects(image)

    def initialize_model(self, path):
        self.session = onnxruntime.InferenceSession(path,
                                                    providers=['CUDAExecutionProvider',
                                                               'CPUExecutionProvider'])
        # Get model info
        self.get_input_details()
        self.get_output_details()

    def segment_objects(self, image):
        input_tensor = self.prepare_input(image)

        # Perform inference on the image
        outputs = self.inference(input_tensor)

        self.boxes, self.scores, self.class_ids, mask_pred = self.process_box_output(outputs[0])
        self.mask_maps = self.process_mask_output(mask_pred, outputs[1])

        return self.boxes, self.scores, self.class_ids, self.mask_maps

    def prepare_input(self, image):
        self.img_height, self.img_width = image.shape[:2]

        input_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Resize input image
        input_img = cv2.resize(input_img, (self.input_width, self.input_height))

        # Scale input pixel values to 0 to 1
        input_img = input_img / 255.0
        input_img = input_img.transpose(2, 0, 1)
        input_tensor = input_img[np.newaxis, :, :, :].astype(np.float32)

        return input_tensor

    def inference(self, input_tensor):
        start = time.perf_counter()
        outputs = self.session.run(self.output_names, {self.input_names[0]: input_tensor})

        # print(f"Inference time: {(time.perf_counter() - start)*1000:.2f} ms")
        return outputs

    def process_box_output(self, box_output):
        box_output = np.squeeze(box_output)

        num_classes = box_output.shape[1] - self.num_masks - 5

        # Filter out predictions with low confidence
        box_output = box_output[box_output[:, 4] > self.conf_threshold]

        # Filter based on class confidence
        conf = box_output[..., [4]] * box_output[..., 5:]
        class_scores = np.max(conf[:, :num_classes], axis=1)
        box_output = box_output[class_scores > self.conf_threshold]
        class_scores = class_scores[class_scores > self.conf_threshold]

        if len(class_scores) == 0:
            return [], [], [], None

        # Extract box and mask predictions (:num_classes+5 is box, the rest is mask)
        box_predictions = box_output[..., :num_classes + 5]
        mask_predictions = box_output[..., num_classes + 5:]

        boxes = self.extract_boxes(box_predictions)
        class_ids = np.argmax(box_predictions[..., 5:], axis=1)

        # Apply nms filtering
        indices = nms(boxes, class_scores, self.iou_threshold)
        return boxes[indices], class_scores[indices], class_ids[indices], mask_predictions[indices]

    def process_mask_output(self, mask_predictions, mask_output):

        if mask_predictions is None:
            return []

        mask_output = np.squeeze(mask_output)

        # Calculate the mask maps for each box
        num_mask, mask_height, mask_width = mask_output.shape  # CHW
        masks = sigmoid(mask_predictions @ mask_output.reshape((num_mask, -1)))
        masks = masks.reshape((-1, mask_height, mask_width))

        # Downscale the boxes to match the mask size
        scale_boxes = self.rescale_boxes(self.boxes,
                                         (self.img_height, self.img_width),
                                         (mask_height, mask_width))

        # For every box/mask pair, get the mask map
        mask_maps = np.zeros((len(scale_boxes), self.img_height, self.img_width))
        blur_size = (int(self.img_width / mask_width), int(self.img_height / mask_height))
        for i in range(len(scale_boxes)):
            scale_x1 = int(math.floor(scale_boxes[i][0]))
            scale_y1 = int(math.floor(scale_boxes[i][1]))
            scale_x2 = int(math.ceil(scale_boxes[i][2]))
            scale_y2 = int(math.ceil(scale_boxes[i][3]))

            x1 = int(math.floor(self.boxes[i][0]))
            y1 = int(math.floor(self.boxes[i][1]))
            x2 = int(math.ceil(self.boxes[i][2]))
            y2 = int(math.ceil(self.boxes[i][3]))

            scale_crop_mask = masks[i][scale_y1:scale_y2, scale_x1:scale_x2]
            crop_mask = cv2.resize(scale_crop_mask,
                                   (x2 - x1, y2 - y1),
                                   interpolation=cv2.INTER_CUBIC)

            crop_mask = cv2.blur(crop_mask, blur_size)

            crop_mask = (crop_mask > 0.5).astype(np.uint8)
            mask_maps[i, y1:y2, x1:x2] = crop_mask

        return mask_maps

    def extract_boxes(self, box_predictions):
        # Extract boxes from predictions
        boxes = box_predictions[:, :4]

        # Scale boxes to original image dimensions
        boxes = self.rescale_boxes(boxes,
                                   (self.input_height, self.input_width),
                                   (self.img_height, self.img_width))

        # Convert boxes to xyxy format
        boxes = xywh2xyxy(boxes)

        # Check the boxes are within the image
        boxes[:, 0] = np.clip(boxes[:, 0], 0, self.img_width)
        boxes[:, 1] = np.clip(boxes[:, 1], 0, self.img_height)
        boxes[:, 2] = np.clip(boxes[:, 2], 0, self.img_width)
        boxes[:, 3] = np.clip(boxes[:, 3], 0, self.img_height)

        return boxes

    def get_label(self):
        return get_label(self.scores,
                         self.class_ids, self.class_name)

    def get_input_details(self):
        model_inputs = self.session.get_inputs()
        self.input_names = [model_inputs[i].name for i in range(len(model_inputs))]

        self.input_shape = model_inputs[0].shape
        self.input_height = self.input_shape[2]
        self.input_width = self.input_shape[3]

    def get_output_details(self):
        model_outputs = self.session.get_outputs()
        self.output_names = [model_outputs[i].name for i in range(len(model_outputs))]

    @staticmethod
    def rescale_boxes(boxes, input_shape, image_shape):
        # Rescale boxes to original image dimensions
        input_shape = np.array([input_shape[1], input_shape[0], input_shape[1], input_shape[0]])
        boxes = np.divide(boxes, input_shape, dtype=np.float32)
        boxes *= np.array([image_shape[1], image_shape[0], image_shape[1], image_shape[0]])

        return boxes


def correct_skew(image, delta=1, limit=5):
    def determine_score(arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1, dtype=float)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2, dtype=float)
        return histogram, score

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    for angle in angles:
        histogram, score = determine_score(thresh, angle)
        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
    corrected = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return best_angle, corrected


def PassportAutoAlign(image):
    try:
        class_name = ['passport']
        model = Passport(path=config['passport']['passport_crop'],
                         class_name=class_name)
        boxes, score, class_id, mask = model.segment_objects(image)
        df = model.get_label()
        label_boxes, _ = check_label(boxes, df['class_name'])
        source_points = np.float32(
            [label_boxes['top_left'], label_boxes['top_right'], label_boxes['bottom_right'],
             label_boxes['bottom_left']])
        result_img = perspective_transform(image, source_points)
        _, result_img = correct_skew(result_img)
        return result_img
    except:
        logging.error(f'error at running {PassportAutoAlign.__name__}, cannot process mrc')
        raise HTTPException(status_code=400,
                            detail={'status': 400, 'code': 'PASSPORT_CANNOT_ALIGN',
                                    'error': 'cannot process passport'})


if __name__ == '__main__':
    pass
