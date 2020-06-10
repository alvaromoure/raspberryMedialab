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

BLACK = 0,0,0
WHITE = 255,255,255
RED = 255,0,0
CODIGO_PELIGRO = 9999
pygame.init()

monitor_size = [pygame.display.Info().current_w,pygame.display.Info().current_h]
screen = pygame.display.set_mode(monitor_size,RESIZABLE)


class displaySignal(object):
    def __init__(self,velocidad):
        self.velocidad = velocidad
    
    def draw(self,screen):
        screen.fill(BLACK)
        if (self.velocidad!=0):
            cx = int(screen.get_width()/2)
            cy = int(screen.get_height()/2)
            font_size = 480
            circle_size = 380
            circle_width = 10
            circulo = circle(screen,RED,(cx,cy),circle_size,circle_width)
            myfont = pygame.font.SysFont("Transport",font_size)
            velocidad = myfont.render(str(self.velocidad),1,WHITE)
            velocidad_rotada = pygame.transform.rotate(velocidad,90)
            velocidad_rect = velocidad_rotada.get_rect(center = circulo.center)
            screen.blit(velocidad_rotada,velocidad_rect)
        pygame.display.update()

def logica_trafico(velocidad_viento,lluvia):
    if(not lluvia):
        if(velocidad_viento<=15 and velocidad_viento>10):
            return 100
        elif(velocidad_viento <=20 and velocidad_viento>15):
            return 90
        elif(velocidad_viento <=25 and velocidad_viento>20):
            return 70
        elif(velocidad_viento >25):
            return CODIGO_PELIGRO
        else:
            return 0
    if(lluvia):
        if(velocidad_viento<=15 and velocidad_viento>10):
            return 90
        elif(velocidad_viento <=20 and velocidad_viento>15):
            return 70
        elif(velocidad_viento <=25 and velocidad_viento>20):
            return CODIGO_PELIGRO
        elif(velocidad_viento >25):
            return CODIGO_PELIGRO
        else:
            return 0
        
def leer_transmisor():
    recibido = False
    while(not recibido):
        if radio.available():
            message=radio.read(32)
            recibido = True
            return(message.decode('utf-8','backslashreplace'))   

def decodificar_datos(datos):
    return (str(datos).split("#"))
    
    
#
array_datos = decodificar_datos(leer_transmisor)
dir_viento_anemometro = array_datos[0]
v_viento_anemometro = array_datos[1]
cantidad_lluvia = array_datos[2]

v = logica_trafico(v_viento_anemometro,False)
signal = displaySignal(v)
signal.draw(screen)
input()
pygame.quit()
datos = leer_transmisor()
print(datos)
        
