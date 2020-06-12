import pygame
import math
import RPi.GPIO as GPIO
import numpy
import time
import base64
from pygame.locals import *
from pygame.draw import *
from RF24 import *
radio = RF24(22,0)
#pipes = [0xF0F0F0F0E1, 0xF0F0F0F0D2]
pipes = bytearray([11,22,33,44,55,66])
radio.begin();
radio.openReadingPipe(1, pipes);
radio.setDataRate(RF24_250KBPS);
radio.setPALevel(RF24_PA_LOW);
radio.printDetails()
radio.startListening();

def leer_transmisor():
    recibido = False
    while(not recibido):
        if radio.available():
            message=radio.read(32)
            recibido = True
            return(message.decode('utf-8'))
    
    
datos = str(leer_transmisor())
l = datos.split("#")
print(l[0])
print(l[1])
print(l[2])