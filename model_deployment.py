from ultralytics import YOLO

model = YOLO(r".\best.pt")

model.predict(source="", classes=[0, 1, 2], show=True)