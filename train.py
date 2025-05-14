from ultralytics import YOLO
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

if __name__ == '__main__':
    model_yaml = r"C:\Users\userone\Desktop\yolov8_ultralytics\yolov8.yaml"
    data_yaml = r"C:\Users\userone\Desktop\yolov8_ultralytics\data.yaml"
    pre_model = r"C:\Users\userone\Desktop\yolov8_ultralytics\yolov8x.pt"
    model = YOLO(model_yaml, task='detect').load(pre_model)
    # build from YAML and transfer weights
    # Train the model
    results = model.train(data=data_yaml, epochs=300, imgsz=640, device=0, resume=True, lr0=0.01, batch=16)
