import RPi.GPIO as GPIO
import time

# Definisikan pin GPIO untuk digit dan segmen pada display 7 segment 2x1
segment_pins = [2, 3, 4, 5, 6, 7, 8]
digit_pins = [9, 10]

GPIO.setmode(GPIO.BCM)
GPIO.setup(segment_pins, GPIO.OUT)
GPIO.setup(digit_pins, GPIO.OUT)

patterns = {
    '0': [1, 1, 1, 1, 1, 1, 0],
    '1': [0, 1, 1, 0, 0, 0, 0],
    '2': [1, 1, 0, 1, 1, 0, 1],
    '3': [1, 1, 1, 1, 0, 0, 1],
    '4': [0, 1, 1, 0, 0, 1, 1],
    '5': [1, 0, 1, 1, 0, 1, 1],
    '6': [1, 0, 1, 1, 1, 1, 1],
    '7': [1, 1, 1, 0, 0, 0, 0],
    '8': [1, 1, 1, 1, 1, 1, 1],
    '9': [1, 1, 1, 1, 0, 1, 1]
}
def display_number(number):
    # Ubah angka menjadi string
    number_str = str(number)

    # Tampilkan angka pada display
    for i in range(len(number_str)):
        # Nyalakan digit yang sesuai
        GPIO.output(digit_pins[i], GPIO.HIGH)

        # Tampilkan pola segmen yang sesuai
        for j in range(7):
            GPIO.output(segment_pins[j], patterns[number_str[i]][j])
        
        # Tunggu sebentar agar angka terlihat
        time.sleep(0.001)
        
        # Matikan digit
        GPIO.output(digit_pins[i], GPIO.LOW)

def countdown():
    number = 9  # Angka awal perhitungan mundur
    
    while number >= 0:
        display_number(number)
        time.sleep(1)  # Tunggu 1 detik
        number -= 1

countdown()
GPIO.cleanup()
