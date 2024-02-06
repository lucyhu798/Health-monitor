import os
import glob
import time
import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BCM)

DIP_red = 20
DIP_green = 21
GPIO.setup(DIP_red, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(DIP_green, GPIO.OUT, initial = GPIO.LOW)
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f
try:
    curTime = time.time()
    while (time.time() - curTime < 30):
        
        tempRead = str(read_temp())
        print(tempRead)
        os.system("python3 Adafruit_Python_SSD1306/examples/stats.py temp " + tempRead)
        if(read_temp() <= 70 or read_temp() >= 100):
            GPIO.output(DIP_red, GPIO.HIGH)
            GPIO.output(DIP_green, GPIO.LOW)
        else:
            GPIO.output(DIP_green, GPIO.HIGH)
            GPIO.output(DIP_red, GPIO.LOW)

        time.sleep(10)
    GPIO.cleanup()
    exit()
except KeyboardInterrupt:
    GPIO.cleanup()