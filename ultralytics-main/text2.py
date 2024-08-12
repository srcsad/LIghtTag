from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
from ultralytics import YOLO

# Load a pretrained YOLOv8n model
# model = YOLO("yolov8n.pt")
# img1 = cv2.imread("012bef554b0b4c00000115a8edf508.jpg@1280w_1l_2o_100sh.jpg")
# # Run inference on an image
# results = model(img1, max_det=1)  # results list

# # View results
# path = results[0].boxes.xyxy
# # print(path)

# c = path.cpu().numpy()
# print(c)
# a = list(map(int, c))
# print(a[0])

# # print the Boxes object containing the detection bounding boxes
# cv2.rectangle(img1, (a[0], a[1]), (a[2], a[3]), (0, 0, 255), 2)
# cv2.imshow("face", img1)
# cv2.waitKey(0)  # 让用户按下键盘任意一个键来退出此图片显示窗口(若没有图像会闪退)


# results = model.predict(
#     source="folder", show=True
# )  # Display preds. Accepts all YOLO predict arguments

# from PIL
# im1 = Image.open("zidane.jpg")
# results = model.predict(source=im1, save=True)  # save plotted images

# # from ndarray
# im2 = cv2.imread("zidane.jpg")
# results = model.predict(
#     source=im2, save=True, save_txt=True
# )  # save predictions as labels

# from list of PIL/ndarray
# results = model.predict(source=[im1, im2])
