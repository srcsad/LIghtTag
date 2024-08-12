import json
import serial.tools.list_ports
import time
from ultralytics import YOLO
from PIL import Image
import cv2
import torch
import threading
import river
from river.naive_bayes import MultinomialNB
from river.feature_extraction import BagOfWords, TFIDF
from river.compose import Pipeline

import pandas as pd
from river import metrics
from time1 import map_rectangles

resend = 1
plist = list(serial.tools.list_ports.comports())
model = YOLO("yolov8n.pt")
j = 0
cishu = 0
df = pd.read_csv("123.csv")
# Convert to Format
df.to_dict()

# Convert to Tuple
data = df.to_records(index=False)

pipe_nb = Pipeline(("vectorizer", BagOfWords(lowercase=True)), ("nb", MultinomialNB()))
pipe_nb.steps
for text, label in data:
    pipe_nb = pipe_nb.learn_one(text, label)

cv2.destroyAllWindows()
cap = cv2.VideoCapture(0)

# global resend
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
    if success:
        cishu += 1
        # Run YOLOv8 inference on the frame
        results = model(frame, max_det=1)
        annotated_frame = results[0].plot()
        cv2.imshow("YOLOv8 Inference", annotated_frame)
        path = results[0].boxes.xyxy
        if path.numel() != 0:
            path = results[0].boxes.xyxy[0]

            c = path.cpu().numpy()
            name = results[0].boxes.cls[0]
            inname = int(name.item())
            global zuobiao
            global finname
            zuobiao = list(map(int, c))
            finname = results[0].names[inname]
            print(zuobiao)
            print(finname)
        if cv2.waitKey(1) & cishu == 120:
            #  if cv2.waitKey(1) & 0xFF == ord("q"):
            cishu = 0
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()
pred = pipe_nb.predict_one(finname)
zuobiao.append(pred)
rect1 = (380, 449, 1870, 834)  # 大矩形
rect2 = (0, 0, 31, 7)  # 小矩形
map_func = map_rectangles(rect1, rect2)
a, b = map_func(zuobiao[0], zuobiao[1])
c, d = map_func(zuobiao[2], zuobiao[3])
yinshezuobiao = [a, b, c - a, d - b, pred]


if zuobiao != 0:
    post = str(yinshezuobiao).replace("[", "").replace("]", "")

if len(plist) <= 0:
    print("没有发现端口!")
else:
    plist_0 = list(plist[0])
    serialName = plist_0[0]
    serialFd = serial.Serial(serialName, 9600, timeout=1)
    print("可用端口名>>>", serialFd.name)
i = 0
print(post)

while i < 2:
    time.sleep(1)
    serialFd.write(post.encode())
    # time.sleep(1)
    #     print("1")
    i = i + 1
i = 0
if pred == 1:
    while True:
        resend = serialFd.readline().decode("utf-8").replace("\r\n", "")
        print(resend)
        if resend == "1":
            intresend = int(resend)

            break
        if resend == "0":
            intresend = int(resend)
            break
    df.loc[len(df.index)] = [finname, intresend]

    # resend = serialFd.readline().decode("utf-8")
    # serialFd.close()
    # print(resend)
    # print("ok")
    df.to_csv("123.csv", index=False)
cap.release()
cv2.destroyAllWindows()
