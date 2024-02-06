# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
# Revised by Lucy & Thanh 3/6/23
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time
import sys

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0


# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    if(sys.argv[1] == "temp"):
        if(float(sys.argv[2]) > 100 or float(sys.argv[2]) < 70):
            draw.text((x, top),  "   Warning !!!!   " ,  font=font, fill=255)
            draw.text((x, top + 8),       "Abnormal value found",  font=font, fill=255)
            draw.text((x, top + 16),       " Check with a doctor",  font=font, fill=255)
            disp.image(image)
            disp.display()
            time.sleep(7)
            draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top),       "Temp(F) =  " + sys.argv[2],  font=font, fill=255)
    if(sys.argv[1] == "pressure"):
        draw.text((x, top+8), sys.argv[2] +  "kg " + sys.argv[3] + " pressure"  , font=font, fill=255)
    if(sys.argv[1] == "pulse"):
        if(float(sys.argv[2]) < 96):
            draw.text((x, top),  "   Warning !!!!   " ,  font=font, fill=255)
            draw.text((x, top + 8),       "Abnormal value found",  font=font, fill=255)
            draw.text((x, top + 16),       " Check with a doctor",  font=font, fill=255)
            disp.image(image)
            disp.display()
            time.sleep(7)
            draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top+16), "Spo2 = " + sys.argv[2],  font=font, fill=255)
    if(sys.argv[1] == "heartbeat" or sys.argv[1] == "breath"):
        if(float(sys.argv[2]) < 60 or float(sys.argv[2]) > 100 or int(sys.argv[3])  < 12 or int(sys.argv[3]) > 16):
            if(sys.argv[2] != "0" and sys.argv[3] != "0"):
                draw.text((x, top),  "   Warning !!!!   " ,  font=font, fill=255)
                draw.text((x, top + 8),       "Abnormal value found",  font=font, fill=255)
                draw.text((x, top + 16),       " Check with a doctor",  font=font, fill=255)
                disp.image(image)
                disp.display()
                time.sleep(7)
                draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top+25),   "BPM = " + sys.argv[2] + " BR = " + sys.argv[3],  font=font, fill=255)
        
    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)
    exit()
