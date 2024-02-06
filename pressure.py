# SPDX-FileCopyrightText: 2019 Mikey Sklar for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BCM)

DIP_red = 20
DIP_green = 21
GPIO.setup(DIP_red, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(DIP_green, GPIO.OUT, initial = GPIO.LOW)

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)


try:
    curTime = time.time()
    while(time.time() - curTime < 30):
        init_time = time.time()
        out = []
        while ((time.time()-init_time) < 2):
        # read the analog pin
            val = chan0.value
            out.append(val)
            
        avg = sum(out)/len(out)
        if(avg  < 4000):
            read = (' low')
            GPIO.output(DIP_red, GPIO.HIGH)
            GPIO.output(DIP_green, GPIO.LOW)
        elif (avg < 50000):
            read = (' med')
            GPIO.output(DIP_red, GPIO.HIGH)
            GPIO.output(DIP_green, GPIO.HIGH) 
        else:
            read = (' high')
            GPIO.output(DIP_red, GPIO.LOW)
            GPIO.output(DIP_green, GPIO.HIGH)
    
        pct = round(avg / 65472 * 2,2)
        print(str(pct)+"kg")
        os.system("python3 Adafruit_Python_SSD1306/examples/stats.py pressure " + str(pct) + read)
    GPIO.cleanup()
    exit()
except KeyboardInterrupt:
    GPIO.cleanup()        
    


