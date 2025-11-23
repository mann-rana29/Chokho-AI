from ultralytics import YOLO

model = YOLO("chokho_ai.pt")

model.predict(source= "images/212.jpg",show = True , save = True)
