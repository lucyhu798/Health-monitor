import time 
import os 

# Run healthcare monitor
try:
    os.system("sudo python3 temp.py")
    os.system("sudo python3 pressure.py")
    os.system("sudo python3 max30102/main.py")
    os.system("python3 ENLACE2022-main/Radar_Sensor/heart_breath.py")

except KeyboardInterrupt:
    print("done")