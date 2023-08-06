import cv2
import numpy as np
import onnxruntime
from .utils.utils_onnx import xywh2xyxy, nms, get_label


class ID_CARD:
    def __init__(self, path, conf_thres=0.4, iou_thres=0.5, class_name=None, yolov5=False, official_nms=False):
        self.conf_threshold = conf_thres
        self.iou_threshold = iou_thres
        self.class_name = class_name
        self.yolov5 = yolov5
        self.official_nms = official_nms
        self.initialize_model(path)

    def __call__(self, image):
        return self.detect_objects(image)

    def initialize_model(self, path):
        options = onnxruntime.SessionOptions()
        options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
        options.intra_op_num_threads = 1
        options.execution_mode = onnxruntime.ExecutionMode.ORT_SEQUENTIAL
        self.session = onnxruntime.InferenceSession(path, options=options, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        self.get_input_details()
        self.get_output_details()
        self.has_postprocess = 'score' in self.output_names or self.official_nms

    def detect_objects(self, image):
        input_tensor = self.prepare_input(image)
        outputs = self.inference(input_tensor)
        if self.has_postprocess:
            self.boxes, self.scores, self.class_ids = self.parse_processed_output(outputs)
        else:
            self.boxes, self.scores, self.class_ids = self.process_output(outputs)
        df = get_label(self.scores, self.class_ids, self.class_name)
        return self.boxes, self.scores, self.class_ids, df

    def prepare_input(self, image):
        self.img_height, self.img_width = image.shape[:2]
        resized_image = cv2.resize(image, (self.input_width, self.input_height))
        normalized_image = resized_image / 255.0
        return normalized_image.transpose(2, 0, 1)[np.newaxis, :, :, :].astype(np.float32)

    def inference(self, input_tensor):
        # import time
        # ti = time.time()
        # print(self.session.run(self.output_names, {self.input_names[0]: input_tensor}))
        # ts = time.time()
        # tf = ts - ti
        # print(tf)
        return self.session.run(self.output_names, {self.input_names[0]: input_tensor})

    def process_output(self, output):
        if self.yolov5:
            predictions = np.squeeze(output[0])
            obj_conf = predictions[:, 4]
            mask = obj_conf > self.conf_threshold
            predictions = predictions[mask]
            if len(predictions) == 0:
                return [], [], []

            obj_conf = obj_conf[mask]
            predictions[:, 5:] *= obj_conf[:, np.newaxis]
            mask = np.max(predictions[:, 5:], axis=1) > self.conf_threshold
            predictions = predictions[mask]
            if len(predictions) == 0:
                return [], [], []

            indices = nms(self.extract_boxes(predictions), np.max(predictions[:, 5:], axis=1), self.iou_threshold)
            boxes = self.extract_boxes(predictions)[indices]
            scores = np.max(predictions[:, 5:], axis=1)[indices]
            class_ids = np.argmax(predictions[:, 5:], axis=1)[indices]
            return boxes, scores, class_ids
        else:
            predictions = np.squeeze(output[0]).T
            scores = np.max(predictions[:, 4:], axis=1)
            predictions = predictions[scores > self.conf_threshold, :]
            scores = scores[scores > self.conf_threshold]

            if len(scores) == 0:
                return [], [], []

            class_ids = np.argmax(predictions[:, 4:], axis=1)
            boxes = self.extract_boxes(predictions)
            indices = nms(boxes, scores, self.iou_threshold)
            return boxes[indices], scores[indices], class_ids[indices]

    def parse_processed_output(self, outputs):
        if self.official_nms:
            scores = outputs[0][:, -1]
            predictions = outputs[0][:, [0, 5, 1, 2, 3, 4]]
        else:
            scores = np.squeeze(outputs[0], axis=1)
            predictions = outputs[1]

        valid_scores = scores > self.conf_threshold
        predictions = predictions[valid_scores, :]
        scores = scores[valid_scores]

        if len(scores) == 0:
            return [], [], []

        batch_number = predictions[:, 0]
        class_ids = predictions[:, 1].astype(int)
        boxes = predictions[:, 2:]

        if not self.official_nms:
            boxes = boxes[:, [1, 0, 3, 2]]

        boxes = self.rescale_boxes(boxes)

        return boxes, scores, class_ids

    def extract_boxes(self, predictions):
        return xywh2xyxy(self.rescale_boxes(predictions[:, :4]))

    def rescale_boxes(self, boxes):
        boxes = boxes / np.array([self.input_width, self.input_height, self.input_width, self.input_height],
                                 dtype=np.float32)
        boxes *= np.array([self.img_width, self.img_height, self.img_width, self.img_height])
        return boxes

    def get_input_details(self):
        self.input_names = [self.session.get_inputs()[i].name for i in range(len(self.session.get_inputs()))]
        self.input_shape = self.session.get_inputs()[0].shape
        self.input_height = self.input_shape[2]
        self.input_width = self.input_shape[3]

    def get_output_details(self):
        self.output_names = [self.session.get_outputs()[i].name for i in range(len(self.session.get_outputs()))]

