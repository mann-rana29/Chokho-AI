from roboflow import Roboflow
from dotenv import load_dotenv
import os

load_dotenv()

ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")
rf = Roboflow(api_key = ROBOFLOW_API_KEY)

#1
# project = rf.workspace("azat1").project("intelligentvision")
# version = project.version(7)
# dataset = version.download("yolov11")

#2
# project = rf.workspace("material-identification").project("garbage-classification-3")
# version = project.version(2)
# dataset = version.download("yolov11")

#3
# project = rf.workspace("datacluster-labs-agryi").project("domestic-trash")
# version = project.version(1)
# dataset = version.download("yolov11")


#4
# project = rf.workspace("smart-india-hackathon-2023").project("garbage_best")
# version = project.version(1)
# dataset = version.download("yolov11")
