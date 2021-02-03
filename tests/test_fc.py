# from mylibtest import colorized_img
from mylibtest.colorization.colorizeImage import colorized_img
import cv2

img = cv2.imread("C:/Users/Aime/Desktop/learn/pylib/files/greyscaleImage.png")

colorized = colorized_img(src=img)
cv2.imshow("colorized", colorized)
cv2.waitKey()
