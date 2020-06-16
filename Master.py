import threading
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
YELLOW = 255,254,84
ROTACION_PANTALLA = 90
PERIODO_ACTUALIZACION = 5

pygame.init()
pygame.display.set_caption("minimal program")
monitor_width = pygame.display.Info().current_w
monitor_height = pygame.display.Info().current_h
monitor_size = [monitor_width,monitor_height]
screen = pygame.display.set_mode(monitor_size,FULLSCREEN)

arrow_surface = pygame.Surface((int(monitor_width/2),monitor_height),pygame.SRCALPHA)
fullscreen = False
running = True
rad = math.pi/180
centro_circulo = [int(monitor_width-monitor_width/2),int(monitor_height/2)]
# arrow_start = [int(monitor_width/2),int(monitor_height/2)]
# arrow_end = [int(monitor_width-monitor_width/3.5),int(monitor_height/2)]
# longitud_flecha = math.sqrt(math.pow((arrow_end[0]-arrow_start[0]),2) + math.pow((arrow_end[1]-arrow_start[1]),2)) 
# centro_flecha = [int((arrow_end[0]+arrow_start[0])/2),int((arrow_end[1]+arrow_start [1])/2)]

centro_cono = (int(monitor_width/8),int(monitor_height/2))
aviso1_centro = [int(monitor_width-monitor_width/6),int(monitor_height/2)]
aviso2_centro = [int(monitor_width-monitor_width/11),int(monitor_height/2)]
aviso_font_size = 120
velocidad_viento_centro = [int(monitor_width/2),int(monitor_height/2)]

def clean_screen(screen):
    screen.fill(BLACK)

def draw_cono(screen):
    cono = pygame.image.load("Cono.png")
    cono_escalado = pygame.transform.scale(cono,(int(monitor_width/2),int(monitor_height/3)))
    cono_rotado = pygame.transform.rotate(cono_escalado,ROTACION_PANTALLA)
    cono_rect = cono_rotado.get_rect(center = centro_cono)
    screen.blit(cono_rotado,cono_rect)
    font_size = 180
    myfont = pygame.font.SysFont("Transport",font_size)
    aviso1 = myfont.render("PRECAUCION",1,WHITE)
    aviso1_rotado = pygame.transform.rotate(aviso1,ROTACION_PANTALLA)
    aviso1_rect = aviso1_rotado.get_rect(center=aviso1_centro)
    screen.blit(aviso1_rotado,aviso1_rect)
    
    aviso2 = myfont.render("VIENTO",1,WHITE)
    aviso2_rotado = pygame.transform.rotate(aviso2,ROTACION_PANTALLA)
    aviso2_rect = aviso2_rotado.get_rect(center=aviso2_centro)
    screen.blit(aviso2_rotado,aviso2_rect)
    pygame.display.update()
        
def draw_velocidad(screen,velocidad):
    if (velocidad!=0):
        font_size = 480
        circle_size = 400
        circle_width = 30
        circulo = circle(screen,RED,centro_circulo,circle_size,circle_width)
        myfont = pygame.font.SysFont("Transport",font_size)
        velocidad = myfont.render(str(velocidad),1,WHITE)
        velocidad_rotada = pygame.transform.rotate(velocidad,90)
        velocidad_rect = velocidad_rotada.get_rect(center = circulo.center)
        screen.blit(velocidad_rotada,velocidad_rect)
    pygame.display.update()

def draw_rosa_viento(screen,direccion,velocidad = 0):
    screen.fill(BLACK)
    draw_cono(screen)
    imagen = pygame.image.load(direccion)
    imagen_escalada = pygame.transform.scale(imagen,(int(monitor_width/1.7),int(monitor_height)))
    imagen_rotada = pygame.transform.rotate(imagen_escalada,90)
    imagen_rect = imagen_rotada.get_rect(center=centro_circulo)
    screen.blit(imagen_rotada,imagen_rect)
    
#     rosa_font_size = 150
#     rosa_font = pygame.font.SysFont("Transport",rosa_font_size)
#     velocidad_viento = rosa_font.render("50",1,YELLOW)
#     velocidad_viento_rotada = pygame.transform.rotate(velocidad_viento,ROTACION_PANTALLA)
#     velocidad_viento_rect = velocidad_viento_rotada.get_rect(center=velocidad_viento_centro)
#     screen.blit(velocidad_viento_rotada,velocidad_viento_rect)
#     pygame.display.update()
    pygame.display.update()

def draw_all(screen,velocidad,direccion):
    draw_velocidad(screen,velocidad)
    draw_rosa_viento(screen,direccion)

def arrow(screen, lcolor, tricolor, start, end, trirad, thickness=20):
    pygame.draw.line(screen, lcolor, start, end, thickness)
    rotation = (math.atan2(start[1] - end[1], end[0] - start[0])) + math.pi/2
    pygame.draw.polygon(screen, tricolor, ((end[0] + trirad * math.sin(rotation),
                                        end[1] + trirad * math.cos(rotation)),
                                       (end[0] + trirad * math.sin(rotation - 120*rad),
                                        end[1] + trirad * math.cos(rotation - 120*rad)),
                                       (end[0] + trirad * math.sin(rotation + 120*rad),
                                        end[1] + trirad * math.cos(rotation + 120*rad))))

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
def wait():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit();
                sys.exit()
            if event.type == KEYDOWN:
                return
            
def leer_transmisor():
    recibido = False
    while(not recibido):
        if radio.available():
            message=radio.read(32)
            recibido = True
            return(message.decode('utf-8','backslashreplace'))   

def decodificar_datos(datos):
    l = str(datos).split("#")
    return l
    
    
def actualizar_display(array_datos):
    dir_viento_anemometro = array_datos[0]
    v_viento_anemometro = array_datos[1]
    cantidad_lluvia = array_datos[2]
    




first_time = time.time()
while true:
    second_time = time.time()
    if(second_time-first_time >= PERIODO_ACTUALIZACION):
        actualizar_display(array_datos)
    array_datos = decodificar_datos(leer_transmisor())
    
    
    
    
    
    
    
     
        
