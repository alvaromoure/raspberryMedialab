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
radio.setPALevel(RF24_PA_HIGH);
radio.printDetails()
radio.startListening();


BLACK = 0,0,0
WHITE = 255,255,255
RED = 255,0,0
YELLOW = 255,254,84
ROTACION_PANTALLA = 90

PERIODO_ACTUALIZACION = 5
PERIODO_PARPADEO = 5
PERIODO_PERSISTENCIA_LLUVIA = 10
CODIGO_PELIGRO = 9999

VELOCIDAD = 0
VELOCIDAD_VIENTO = ""
DIRECCION_VIENTO = ""
CANTIDAD_LLUVIA = "0"
rosa_dibujada = True
temporizador_lluvia = time.time()

pygame.init()
pygame.display.set_caption("minimal program")
monitor_width = pygame.display.Info().current_w
monitor_height = pygame.display.Info().current_h
monitor_size = [monitor_width,monitor_height]
screen = pygame.display.set_mode(monitor_size,RESIZABLE)

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
    aviso1 = myfont.render("PRECAUCIÓN",1,WHITE)
    aviso1_rotado = pygame.transform.rotate(aviso1,ROTACION_PANTALLA)
    aviso1_rect = aviso1_rotado.get_rect(center=aviso1_centro)
    screen.blit(aviso1_rotado,aviso1_rect)
    
    aviso2 = myfont.render("VIENTO",1,WHITE)
    aviso2_rotado = pygame.transform.rotate(aviso2,ROTACION_PANTALLA)
    aviso2_rect = aviso2_rotado.get_rect(center=aviso2_centro)
    screen.blit(aviso2_rotado,aviso2_rect)
    pygame.display.update()
        
def draw_velocidad(screen,velocidad):
    if (velocidad!=0 and velocidad != CODIGO_PELIGRO):
        font_size = 480
        circle_size = 400
        circle_width = 30
        circulo = circle(screen,RED,centro_circulo,circle_size,circle_width)
        myfont = pygame.font.SysFont("Transport",font_size)
        velocidad = myfont.render(str(velocidad),1,WHITE)
        velocidad_rotada = pygame.transform.rotate(velocidad,90)
        velocidad_rect = velocidad_rotada.get_rect(center = circulo.center)
        screen.blit(velocidad_rotada,velocidad_rect)
    elif(velocidad == CODIGO_PELIGRO):
        draw_peligro(screen)
    pygame.display.update()

def draw_rosa_viento(screen,direccion,velocidad = 0):
    direccion =direccion + ".png"
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
    
def draw_peligro(screen):
    peligro = pygame.image.load("peligro.png")
    peligro_escalado = pygame.transform.scale(peligro,(int(monitor_width/2.7),int(monitor_height/1.3)))
    peligro_rect = peligro_escalado.get_rect(center=centro_circulo)
    screen.blit(peligro_escalado,peligro_rect)
    pygame.display.update()
    
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
    if radio.available():
        message=radio.read(32)
        return(message.decode('utf-8','backslashreplace'))   

def decodificar_datos(datos):
    if (datos is None):
        return [0]
    l = str(datos).split("#")
    print (datos)
    return l

def lluvia_handler(cantidadLluvia):
    global temporizador_lluvia
    
    lluvia_actual = float(cantidadLluvia)
    if(lluvia_actual > 0):
        temporizador_lluvia = time.time()
        return True
    if(time.time()-temporizador_lluvia > PERIODO_PERSISTENCIA_LLUVIA):
        return False
    
    
    
def actualizar_variables(array_datos):
    global DIRECCION_VIENTO
    global VELOCIDAD_VIENTO
    global CANTIDAD_LLUVIA
    global VELOCIDAD
    
    DIRECCION_VIENTO = array_datos[0]
    VELOCIDAD_VIENTO = array_datos[1]
    CANTIDAD_LLUVIA = array_datos[2]
    bool_lluvia = lluvia_handler(CANTIDAD_LLUVIA)
    VELOCIDAD = logica_trafico(float(VELOCIDAD_VIENTO),bool_lluvia)
    
def parpadeo_display():
    global rosa_dibujada
    clean_screen(screen)
    draw_cono(screen)
    if (rosa_dibujada):
        draw_velocidad(screen,VELOCIDAD)
        rosa_dibujada = False
    elif(not rosa_dibujada):
        draw_rosa_viento(screen,DIRECCION_VIENTO)
        rosa_dibujada = True
    

primer_temporizador_actualizacion = time.time()
primer_temporizador_parpadeo = time.time()
primera_vez = True
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            pygame.quit()
            exit()
    segundo_temporizador_actualizacion = time.time()
    array_datos = decodificar_datos(leer_transmisor())
    if(segundo_temporizador_actualizacion - primer_temporizador_actualizacion >= PERIODO_ACTUALIZACION or primera_vez):
        if(len(array_datos)>2):
            actualizar_variables(array_datos)
            primer_temporizador_actualizacion = segundo_temporizador_actualizacion
            primera_vez = False
            
    segundo_temporizador_parpadeo = time.time()
    if(segundo_temporizador_parpadeo - primer_temporizador_parpadeo >= PERIODO_PARPADEO):
        if(not primera_vez):
            parpadeo_display()
            primer_temporizador_parpadeo = segundo_temporizador_parpadeo
    
        
    
    
    
    
    
    
     
        
