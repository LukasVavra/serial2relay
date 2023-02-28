#! /bin/python3
import sys
import time
import threading
import tkinter as tk
# package pyserial
import serial
from serial.tools import list_ports

# configuration
PORT = '/dev/ttyUSB0'
BAUDRATE = 9600
RELAYCOUNT = 4

# global variables
switch1_var = None
switch2_var = None
switch3_var = None
switch4_var = None
led1 = None
led2 = None
led3 = None
led4 = None
global ser
ser = None

running = True

def trigger_relay(i):
    try:
        ser.write("t".encode())    
        ser.write(str(i).encode())    
        ser.write(" ".encode())
    except:
        print("Serial port write error")

def turnon_relay(i):
    try:
        ser.write("u".encode())    
        ser.write(str(i).encode())    
        ser.write(" ".encode())
    except:
        print("Serial port write error")

def turnoff_relay(i):
    try:
        ser.write("d".encode())    
        ser.write(str(i).encode())    
        ser.write(" ".encode())
    except:
        print("Serial port write error")


def switch1_change():
    if(switch1_var.get() == True):
        turnon_relay(0)
    else:
        turnoff_relay(0)

def switch2_change():
    if(switch2_var.get() == True):
        turnon_relay(1)
    else:
        turnoff_relay(1)

def switch3_change():
    if(switch3_var.get() == True):
        turnon_relay(2)
    else:
        turnoff_relay(2)

def switch4_change():
    if(switch4_var.get() == True):
        turnon_relay(3)
    else:
        turnoff_relay(3)

def button1_click():
    trigger_relay(0)

def button2_click():
    trigger_relay(1)

def button3_click():
    trigger_relay(2)

def button4_click():
    trigger_relay(3)

def ledon(led):
    led.delete()
    led.create_oval(1, 1, 19, 19, fill="green", outline="black")

def ledoff(led):
    led.delete()
    led.create_oval(1, 1, 19, 19, fill="grey", outline="black")

def create_window():
    root = tk.Tk()
    root.title("SwitcherArduino")

    global switch1_var
    switch1_var = tk.BooleanVar()
    global switch2_var
    switch2_var = tk.BooleanVar()
    global switch3_var
    switch3_var = tk.BooleanVar()
    global switch4_var
    switch4_var = tk.BooleanVar()

    switch1 = tk.Checkbutton(root, text="Switch 1", variable=switch1_var, command=switch1_change)
    button1 = tk.Button(root, text="Reboot 1", command=button1_click)
    switch2 = tk.Checkbutton(root, text="Switch 2", variable=switch2_var, command=switch2_change)
    button2 = tk.Button(root, text="Reboot 2", command=button2_click)
    switch3 = tk.Checkbutton(root, text="Switch 3", variable=switch3_var, command=switch3_change)
    button3 = tk.Button(root, text="Reboot 3", command=button3_click)
    switch4 = tk.Checkbutton(root, text="Switch 4", variable=switch4_var, command=switch4_change)
    button4 = tk.Button(root, text="Reboot 4", command=button4_click)

    global led1
    led1 = tk.Canvas(root, width=20, height=20);
    ledoff(led1)
    global led2
    led2 = tk.Canvas(root, width=20, height=20);
    ledoff(led2)
    global led3
    led3 = tk.Canvas(root, width=20, height=20);
    ledoff(led3)
    global led4
    led4 = tk.Canvas(root, width=20, height=20);
    ledoff(led4)
    
    led1.grid(row=0, column=0, padx=2, pady=5)
    switch1.grid(row=1, column=0, padx=2, pady=2)
    button1.grid(row=2, column=0, padx=2, pady=2)
    led2.grid(row=0, column=1, padx=2, pady=5)
    switch2.grid(row=1, column=1, padx=2, pady=2)
    button2.grid(row=2, column=1, padx=2, pady=2)
    led3.grid(row=0, column=2, padx=2, pady=5)
    switch3.grid(row=1, column=2, padx=2, pady=2)
    button3.grid(row=2, column=2, padx=2, pady=2)
    led4.grid(row=0, column=3, padx=2, pady=5)
    switch4.grid(row=1, column=3, padx=2, pady=2)
    button4.grid(row=2, column=3, padx=2, pady=2)
    return root

def read_serial():
    while(True):
        data = ser.readline().decode().strip()
        print(data)
        res = data.split(":")
        if(res[1] == 1):
            ledon(res[0])
        else:
            ledoff(res[0])

if __name__ == "__main__":
    # open port
    try:
        ser = serial.Serial(PORT, BAUDRATE)
        time.sleep(2)

        serial_thread = threading.Thread(target=read_serial)
        serial_thread.daemon = True
        serial_thread.start()

        # open window
        root = create_window()
        root.mainloop()
        # close port
        ser.close();
    
    except:
        print("Serial port error, available ports:")
        ports = list_ports.comports()
        for p in ports:
            print(p)