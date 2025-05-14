from ultralytics import YOLO
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

if __name__ == '__main__':
    model_yaml = r"C:\Users\userone\Desktop\yolov8_ultralytics\yolov8.yaml"
    data_yaml = r"C:\Users\userone\Desktop\yolov8_ultralytics\data.yaml"
    pre_model = r"C:\Users\userone\Desktop\yolov8_ultralytics\runs\detect\train17\weights\best.pt"
    model = YOLO(model_yaml, task='detect').load(pre_model)
    # build from YAML and transfer weights

    metrics = model.val(data=data_yaml)
