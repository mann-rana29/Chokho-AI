from ultralytics import YOLO

model = YOLO("chokho_ai.pt")

model.predict(source= "images/101.jpg",show = True , save = True)
