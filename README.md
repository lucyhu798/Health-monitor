# Healthcare Monitor

## Overview
Our goal for the healthcare monitor was creating a system that would be easy for individuals to use at home without needing to go to the hospital for extended periods of time. With this monitor system, individuals will be able to get their daily vitals monitored in an accessible way, and go to the doctor if needed (i.e. if there are abnormal readings detected by the system).

## Setup
The following hardware was used:
- KY-001 Temperature sensor 
- RP-C10-ST 0.4mm Pressure sensor 
- HiLetgo MAX30102 Heart rate and pulse oximetry sensor 
- Seeedstudio MR60BHA1 60GHz Wireless Breathing and Heartbeat sensor 
- Adafruit MCP3008 8-channel ADC 
- KY-011 DIP 2- LED sensor 
- GME12864-13 I2C OLED Display 

### Run the code
To run the healthcare monitor:
```
cd Final // Go to the Final folder with main.py
sudo python3 main.py
```
Running **main.py** runs each of the healthcare sensors consecutively in this order: temperature sensor, pressure sensor, pulse oximetry sensor, and wireless heartbeat sensor. The data received from each of these sensors get displayed on the display sensor and displays a warning message if there are abnormal readings.

## Results

We ran several tests to determine the accuracy of the temperature, pressure, pulse oximetry, and wireless heartbeat sensors. More detailed reports can be found on our final report (**Results** and **Result Implications** sections), but we put the general findings below.

The **temperature sensor** works accurately for small objects and warmer temperatures. For cold objects, the sensor is not that accurate, but since this is a healthcare monitor, a human's skin temperature should be no lower than 80-85 deg Fahrehenheit.

The **pressure sensor** works accurately for objects/grip strength up to 2 kg. Although the sensor cannot measure objects larger than 2 kg, this sensor in our healthcare monitor system is intended to measure the grip strength of older individuals.

The **pulse oximetry sensor** is very sensitive and has accurate readings if positioned properly. Otherwise, it may have varied readings if the person's finger is not pressed flat against the sensor, or if the sensor is moved around.

The **wireless heartbeat sensor** is accurate in measuring a person's heartbeat rate. For breath rate, the sensor seems to work properly (i.e. output normal breath rates for individuals), but we had a harder time objectively testing an individual's breath rate.

#

Made by Lucy Hu and Thanh Tong :)