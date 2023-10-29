from ultralytics import YOLO
import os


class CVModel:
    def __init__(self, threshold=0.6):
        self.model_path = os.path.join(".", "v14best.pt")
        self.model = YOLO(self.model_path)
        self.threshold = threshold
