import supervision as sv
import torch
from autodistill.detection import DetectionTargetModel
from yolov5 import load, train

device = "cuda" if torch.cuda.is_available() else "cpu"


class YOLOv5(DetectionTargetModel):
    def __init__(self, model_name):
        self.yolo = load(model_name + ".pt", device=device)

        self.yolo.conf = 0.25  # NMS confidence threshold
        self.yolo.iou = 0.45  # NMS IoU threshold
        self.yolo.agnostic = False  # NMS class-agnostic
        self.yolo.multi_label = False  # NMS multiple labels per box
        self.yolo.max_det = 1000  # maximum number of detections per image

    def predict(self, input: str, confidence=0.5) -> sv.Detections:
        return sv.Detections.from_yolov5(self.yolo(input, conf=confidence))

    def train(self, dataset_yaml, epochs=300, image_size=640):
        train.run(data=dataset_yaml, epochs=epochs, imgsz=image_size)
