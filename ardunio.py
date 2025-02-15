import serial
import time

# Replace 'COM3' with your Arduino's port (e.g., 'COM3' for Windows, '/dev/ttyACM0' for Linux, '/dev/tty.usbmodemXXXX' for Mac)
arduino_port = 'COM9'  
baudrate = 9600
ser = serial.Serial(arduino_port, baudrate)
time.sleep(2)  # Wait for the serial connection to initialize

while True:
    if ser.in_waiting > 0:
        button_no = int(ser.readline().decode('utf-8').rstrip())

        # Do something with the button inputs
        # Example: If Button 1 is pressed, perform some action
        print(f"Button {button_no} is pressed")
