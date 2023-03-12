import csv
from time import time

import serial

# Your serial port might be different!
ser = serial.Serial('/dev/cu.usbmodem142401', timeout=1)

f = open("/data/voltages.csv", "a+")
writer = csv.writer(f, delimiter=',')

while True:
    s = ser.readline().decode()
    if s != "":
        rows = [float(x) for x in s.split(',')]
        # Insert local time to list's first position
        rows.insert(0, int(time()))
        print(rows)
        writer.writerow(rows)
        f.flush()