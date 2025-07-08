import argparse
import os
from ultralytics import YOLO

model = YOLO("yolo11n.pt")
# model = YOLO("./sports/best.pt")

# result = model("./data/")
model.predict("data/output.mp4", save=True, show=False, imgsz=1920, conf=0.5)
