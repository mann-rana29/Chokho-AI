from ultralytics import YOLO

model = YOLO("chokho_ai.pt")

model.predict(source= "34.webp",show = True , save = True)
