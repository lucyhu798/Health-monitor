
from max30102 import MAX30102
import hrcalc
import threading
import os
import time
import numpy as np
import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BCM)

DIP_red = 20
DIP_green = 21
GPIO.setup(DIP_red, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(DIP_green, GPIO.OUT, initial = GPIO.LOW)


class HeartRateMonitor(object):

    LOOP_TIME = 1

    def __init__(self, print_raw=False, print_result=False):
        self.bpm = 0
        if print_raw is True:
            print('IR, Red')
        self.print_raw = print_raw
        self.print_result = print_result

    def run_sensor(self):
        sensor = MAX30102()
        ir_data = []
        red_data = []
        bpms = []
        avg_spo2 = []
        spo22 = []

        # run until told to stop
        while not self._thread.stopped:
            # check if any data is available
            num_bytes = sensor.get_data_present()
            if num_bytes > 0:
                # grab all the data and stash it into arrays
                while num_bytes > 0:
                    red, ir = sensor.read_fifo()
                    num_bytes -= 1
                    ir_data.append(ir)
                    red_data.append(red)
                    if self.print_raw:
                        print("{0}, {1}".format(ir, red))

                while len(ir_data) > 100:
                    ir_data.pop(0)
                    red_data.pop(0)

                if len(ir_data) == 100:
                    bpm, valid_bpm, spo2, valid_spo2 = hrcalc.calc_hr_and_spo2(ir_data, red_data)
                    if valid_bpm:
                        bpms.append(bpm)
                        while len(bpms) > 4:
                            bpms.pop(0)
                        self.bpm = np.mean(bpms)
                        if (np.mean(ir_data) < 50000 and np.mean(red_data) < 50000):
                            self.bpm = 0
                            if self.print_result:
                                print("Finger not detected")
                        if self.print_result:
                            if(spo2 > 0):
                                spo22.append(spo2)
                            avg_spo2 = sum(spo22)/len(spo22)
                            
                            print('Sensor is running {0}' .format(spo2))

            time.sleep(self.LOOP_TIME)
        if(avg_spo2 < 96):
            GPIO.output(DIP_red, GPIO.HIGH)
            GPIO.output(DIP_green, GPIO.LOW)
        else:
            GPIO.output(DIP_red, GPIO.LOW)
            GPIO.output(DIP_green, GPIO.HIGH)
        print("SpO2: {0}".format( avg_spo2))
        avg_spo2 = round(avg_spo2,2)
        os.system("python3 Adafruit_Python_SSD1306/examples/stats.py pulse " + str(avg_spo2))
        
        sensor.shutdown()
        time.sleep(5)
        GPIO.cleanup()
        

    def start_sensor(self):
        self._thread = threading.Thread(target=self.run_sensor)
        self._thread.stopped = False
        self._thread.start()

    def stop_sensor(self, timeout=2.0):
        self._thread.stopped = True
        self.bpm = 0
        self._thread.join(timeout)
