from __future__ import print_function
import RPi.GPIO as GPIO
import numpy
from RF24 import *
import time
import base64

radio = RF24(22,0)
#pipes = [0xF0F0F0F0E1, 0xF0F0F0F0D2]
pipes = bytearray([11,22,33,44,55,66])
radio.begin();
radio.openReadingPipe(1, pipes);
radio.setDataRate(RF24_250KBPS);
radio.setPALevel(RF24_PA_HIGH);
radio.printDetails()
radio.startListening();


while True:
	if radio.available():
		message=radio.read(32)
		print("received")
		print(message.decode('utf-8','backslashreplace'))	
	time.sleep(1)
