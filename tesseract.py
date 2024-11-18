import cv2
import os
import pytesseract
import sys

directory_path = "captcha"

def captcha_solver(filename):
    image = cv2.imread(filename)
    pyr = cv2.pyrMeanShiftFiltering(src = image, sp = 5, sr = 70, maxLevel = 1)

    #gray = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    medianBlur = cv2.medianBlur(gray, 3)
    gaussianBlur = cv2.GaussianBlur(medianBlur, (3,3), 0)

    th, img = cv2.threshold(gaussianBlur, 190, 255, cv2.THRESH_BINARY)
    dilate = cv2.erode(img, (3, 3), iterations = 1)

    txt = pytesseract.image_to_string(gaussianBlur, config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789 --dpi 70')

    """
    # Display the image
    cv2.imshow('pyr', pyr)
    cv2.imshow('medianBlur', medianBlur)
    cv2.imshow('gaussian blur', gaussianBlur)
    cv2.imshow('dilate', dilate)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    fname = filename.split('.')[0]
    cv2.imwrite(fname + 'pyr.png', pyr)
    cv2.imwrite(fname + 'medianBlur.png', medianBlur)
    cv2.imwrite(fname + 'gaussianBlur.png', gaussianBlur)
    cv2.imwrite(fname + 'dilate.png', dilate)
    """
    return txt.strip()


for filename in os.listdir(directory_path):
    if filename.endswith(".png"):
        file_path = os.path.join(directory_path, filename)
        print(f"--- {filename} ---")
        ans = captcha_solver(file_path)
        print(f"Captcha solution: {ans} ")
        if filename.split('.')[0] == ans:
            print("Captcha solution is correct!")
        else:
            print("Captcha solution is wrong!")
