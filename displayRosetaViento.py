import pygame
import math
import os
import sys
from pygame.locals import *
from pygame.draw import *

import pygame
import math
import os
import sys
from pygame.locals import *
from pygame.draw import *

pygame.init()
pygame.display.set_caption("minimal program")
BLACK = 0,0,0
WHITE = 255,255,255
RED = 255,0,0
monitor_width = pygame.display.Info().current_w
monitor_height = pygame.display.Info().current_h
monitor_size = [monitor_width,monitor_height]
screen = pygame.display.set_mode(monitor_size,FULLSCREEN)

arrow_surface = pygame.Surface((int(monitor_width/2),monitor_height),pygame.SRCALPHA)
fullscreen = False
running = True
rad = math.pi/180
circle_offset = int(monitor_width/4)
arrow_start = [int(monitor_width/2),int(monitor_height/2)]
arrow_end = [int(monitor_width-monitor_width/3.5),int(monitor_height/2)]
longitud_flecha = math.sqrt(math.pow((arrow_end[0]-arrow_start[0]),2) + math.pow((arrow_end[1]-arrow_start[1]),2)) 
centro_flecha = [int((arrow_end[0]+arrow_start[0])/2),int((arrow_end[1]+arrow_start [1])/2)]

aviso_centro = [int(monitor_width-monitor_width/6),int(monitor_height/2)]
aviso_font_size = 120


        
        
def draw_velocidad(screen,velocidad):
    screen.fill(BLACK)
    if (velocidad!=0):
        cx = int(screen.get_width()/2)
        cy = int(screen.get_height()/2)
        font_size = 480
        circle_size = 380
        circle_width = 30
        circulo = circle(screen,RED,(cx-circle_offset,cy),circle_size,circle_width)
        myfont = pygame.font.SysFont("Transport",font_size)
        velocidad = myfont.render(str(velocidad),1,WHITE)
        velocidad_rotada = pygame.transform.rotate(velocidad,90)
        velocidad_rect = velocidad_rotada.get_rect(center = circulo.center)
        screen.blit(velocidad_rotada,velocidad_rect)
    pygame.display.update()

def draw_rosa_viento(screen,direccion,velocidad = 0):
    screen.fill(BLACK)
    imagen = pygame.image.load(direccion)
    imagen_escalada = pygame.transform.scale(imagen,(int(monitor_width/1.7),int(monitor_height)))
    imagen_rotada = pygame.transform.rotate(imagen_escalada,90)
    imagen_rect = imagen_rotada.get_rect(center=centro_flecha)
    screen.blit(imagen_rotada,imagen_rect)
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
                
v = logica_trafico(20,False)
draw_velocidad(screen,v)
wait()
draw_rosa_viento(screen,"N.png")
wait()

v = logica_trafico(25,False)
draw_velocidad(screen,v)
wait()
pygame.quit()
    
