import RPi.GPIO as GPIO
import time
import cv2
from cvlib.object_detection import YOLO
import numpy as np
import threading
import numpy as np

PIR_input = 12
Relay1 = 22
Relay2 = 24
Relay3 = 26
Buzzer = 36
segments = [3, 5, 7, 11, 13, 15, 19]
digits = [8, 10]

digit_patterns = {
    0: [1, 1, 1, 1, 1, 1, 0],
    1: [0, 1, 1, 0, 0, 0, 0],
    2: [1, 1, 0, 1, 1, 0, 1],
    3: [1, 1, 1, 1, 0, 0, 1],
    4: [0, 1, 1, 0, 0, 1, 1],
    5: [1, 0, 1, 1, 0, 1, 1],
    6: [1, 0, 1, 1, 1, 1, 1],
    7: [1, 1, 1, 0, 0, 0, 0],
    8: [1, 1, 1, 1, 1, 1, 1],
    9: [1, 1, 1, 1, 0, 1, 1]
}

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_input, GPIO.IN)
GPIO.setup(Relay1, GPIO.OUT)
GPIO.setup(Relay2, GPIO.OUT)
GPIO.setup(Relay3, GPIO.OUT)
GPIO.setup(Buzzer, GPIO.OUT)
GPIO.setup(segments, GPIO.OUT)
GPIO.setup(digits, GPIO.OUT)

def led_green():
    print("GREEN ON")
    print("GO ")
    GPIO.output (Relay1, GPIO.HIGH)
    GPIO.output (Relay2, GPIO.HIGH)
    GPIO.output (Relay3, GPIO.LOW)
    print("NO Detection")
    GPIO.output(Buzzer, GPIO.LOW)
    print("off buzz")
    time.sleep(4)

def led_yellow():
    print("YELLOW ON")
    print("WAITING \n")
    GPIO.output (Relay1, GPIO.HIGH)
    GPIO.output (Relay2, GPIO.LOW)
    GPIO.output (Relay3, GPIO.HIGH)
    time.sleep(5)

def display_digit(digit, number):
    GPIO.output(digits, GPIO.LOW)  # Turn off all digits
    GPIO.output(segments, GPIO.HIGH)  # Turn off all segments
    GPIO.output(digits[digit], GPIO.HIGH)

    for i, segment in enumerate(segments):
        if digit_patterns[number][i] == 1:
            GPIO.output(segment, GPIO.LOW)

def count_down(number):
    while number >= 0:
        display_digit(0, number // 10)  # Display the tens digit
        time.sleep(0.5)
        display_digit(1, number % 10)  # Display the ones digit
        time.sleep(0.05)
        number -= 1

def led_red():
    print("RED ON")
    print("STOP")
    GPIO.output (Relay1, GPIO.LOW)
    GPIO.output (Relay2, GPIO.HIGH)
    GPIO.output (Relay3, GPIO.HIGH)
    GPIO.output(Buzzer, GPIO.HIGH)
    print("Buzz ON \n ")
    count_down(45)

cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

weights="yolov4-tiny-custom_best.weights"
config="yolov4-tiny-custom.cfg"
labels="obj.names"
count=0

while True:
    if GPIO.input(PIR_input) == GPIO.HIGH:
       print("Object Detection")
        ret,img=cap.read()
        count += 1
        if count % 10 != 0:
            continue
        img=cv2.resize(img,(640,480))
        yolo = YOLO(weights, config,labels)
        bbox, label, conf = yolo.detect_objects(img)
        img1=yolo.draw_bbox(img, bbox, label, conf)
        cv2.imshow("img1",img)
        if cv2.waitKey(1)&0xFF==27:
        break
       led_yellow()
       led_red()

    else:
       print("No Detection")
       led_green() 
