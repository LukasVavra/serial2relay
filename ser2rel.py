#! /bin/python3
import sys
import time
# package pyserial
import serial
from serial.tools import list_ports

# configuration
PORT = '/dev/ttyACM0'
BAUDRATE = 9600
RELAY_COUNT = 4

def print_ports():
    # print list of serial ports
    print("---------- PORTS ----------")
    ports = list_ports.comports()
    for p in ports:
        print(p) 

def trigger_relay(ser, i):
    ser.write("t ".encode())
    ser.write(str(i).encode())
    ser.write(" ".encode())

if __name__ == "__main__":
    # get arguments
    args = sys.argv

    if "list" in args:
        print_ports()

    # open port
    ser = serial.Serial(PORT, BAUDRATE)
    time.sleep(1)

    # send trigger message if index is given
    for i in range(RELAY_COUNT):
        if str(i) in args:
            trigger_relay(ser, i)

    # close port
    ser.close();