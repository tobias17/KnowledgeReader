import pyautogui
import numpy as np
import cv2 as cv
import pytesseract
from os import path
import pickle

def save_zones(obj):
    with open('zones.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_zones():
    with open('zones.pkl', 'rb') as f:
        return pickle.load(f)

grade_to_color = {
    "S":  [26.78947368, 61.97165992, 69.14979757],
    "A+": [77.63157895, 23.77732794, 69.44129555],
    "A":  [40.57894737, 26.29554656, 72.80971660],
    "B":  [79.03238866, 63.08097166, 22.11740891],
    "C":  [24.42510121, 59.95951417, 48.44939271],
    "?":  [84.64372470, 84.40485830, 85.58299595],
}

grade_to_points_rem = {
    "S":  0,
    "A+": 5,
    "A":  8,
    "B":  9,
    "C":  9,
    "?":  10
}

zone_to_points_rem = {}
if path.exists('zones.pkl'):
    print('loading zone data from file')
    zone_to_points_rem = load_zones()
    print(zone_to_points_rem)

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
config = ('-l eng --oem 1 --psm 3')

print('awaiting input...')

while True:
    s = input()
    if 'q' in s:
        break
    print('screenshotting...')
    ss = pyautogui.screenshot()
    ss.save('temp.png')

    img = cv.imread('temp.png')
    img = img[974:1420, 2037:2538]

    name_img = img[:19,20:]
    name = pytesseract.image_to_string(name_img, config=config).strip().split('(I')[0]
    print(name)

    grades = []
    for i in range(1, 22):
        inc_amnt = int(i/7) - (1 if (i >= 18 and i <= 20) else 0)
        small_img = img[i*19+inc_amnt:(i+1)*19+inc_amnt]

        if np.mean(small_img[:,:20], axis=(0, 1))[1] > 42:
            break

        color = np.mean(small_img[:,51:64], axis=(0, 1))
        best_grade = "_"
        best_value = 1000
        for grade in grade_to_color:
            v = 0
            for axis in range(3):
                v += abs(color[axis] - grade_to_color[grade][axis])
            if v < best_value:
                best_value = v
                best_grade = grade
        grades.append(best_grade)
    print(grades)
    points_rem = 0
    for grade in grades:
        points_rem += grade_to_points_rem[grade]
    print(f'points remaining: {points_rem}')
    zone_to_points_rem[name] = points_rem
    save_zones(zone_to_points_rem)
