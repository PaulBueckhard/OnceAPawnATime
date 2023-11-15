import cv2
import numpy as np

class CaptureImage:
    def capture_and_save_image(filename):
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            raise IOError("Cannot open webcam")

        ret, frame = cap.read()

        if not ret:
            raise IOError("Cannot read from webcam")

        height, width = frame.shape[:2]
        min_dim = min(height, width)
        top = int((height - min_dim) / 2)
        left = int((width - min_dim) / 2)
        square_frame = frame[top:top+min_dim, left:left+min_dim]

        cv2.imwrite(filename, square_frame)
        cap.release()

# CaptureImage.capture_and_save_image('image1.jpg')
# print("First image captured. Type 'x' to capture the second image.")

# while True:
#     if input() == 'x':
#         CaptureImage.capture_and_save_image('image2.jpg')
#         print("Second image captured.")
#         break
