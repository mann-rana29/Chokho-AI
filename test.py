from ultralytics import YOLO

model = YOLO("chokho_ai.pt")

model.predict(source= "11.jpg",show = True , save = True)
