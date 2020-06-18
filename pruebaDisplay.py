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

monitor_center = [int(monitor_width/2),int(monitor_height/2)]

screen = pygame.display.set_mode(monitor_size,RESIZABLE)

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
class displaySignal(object):
    def __init__(self,velocidad,dirViento):
        self.velocidad = velocidad
        self.dirViento = dirViento
    
    def draw(self,screen):
        screen.fill(BLACK)
        if (self.velocidad!=0):
            cx = int(screen.get_width()/2)
            cy = int(screen.get_height()/2)
            font_size = 480
            circle_size = 380
            circle_width = 10
            circulo = circle(screen,RED,(cx-circle_offset,cy),circle_size,circle_width)
            myfont = pygame.font.SysFont("Transport",font_size)
            velocidad = myfont.render(str(self.velocidad),1,WHITE)
            velocidad_rotada = pygame.transform.rotate(velocidad,90)
            velocidad_rect = velocidad_rotada.get_rect(center = circulo.center)
            screen.blit(velocidad_rotada,velocidad_rect)
            dibujar_flecha(self.dirViento,screen,WHITE,WHITE,arrow_start,arrow_end,50)
            
            fuente_aviso = pygame.font.SysFont("Transport",aviso_font_size)
            aviso = fuente_aviso.render("VIENTO FUERTE",1,WHITE)
            aviso_rotado = pygame.transform.rotate(aviso,90)
            aviso_rect = aviso_rotado.get_rect(center = aviso_centro)
            screen.blit(aviso_rotado,aviso_rect)
        pygame.display.update()
        
def dibujar_flecha(dir_cardinal,screen,lcolor,tricolor,start,end,trirad,thickness=20):
    if(dir_cardinal == "N"):
        arrow(screen,lcolor,tricolor,end,start,trirad,thickness=20)
    elif(dir_cardinal == "E"):
        inicio = [centro_flecha[0],centro_flecha[1]+int(longitud_flecha/2)]
        fin = [centro_flecha[0],centro_flecha[1]-int(longitud_flecha/2)]
        arrow(screen,lcolor,tricolor,inicio,fin,trirad,thickness=20)
    elif(dir_cardinal == "S"):
        arrow(screen,lcolor,tricolor,start,end,trirad,thickness=20)
    
    
def arrow(screen, lcolor, tricolor, start, end, trirad, thickness=20):
    pygame.draw.line(screen, lcolor, start, end, thickness)
    rotation = (math.atan2(start[1] - end[1], end[0] - start[0])) + math.pi/2
    pygame.draw.polygon(screen, tricolor, ((end[0] + trirad * math.sin(rotation),
                                        end[1] + trirad * math.cos(rotation)),
                                       (end[0] + trirad * math.sin(rotation - 120*rad),
                                        end[1] + trirad * math.cos(rotation - 120*rad)),
                                       (end[0] + trirad * math.sin(rotation + 120*rad),
                                        end[1] + trirad * math.cos(rotation + 120*rad))))
p1 = [int(monitor_width/3),int(monitor_height/2)]
p2 = [int(monitor_width-monitor_width/3),int(monitor_height/5)]
p3 = [int(monitor_width-monitor_width/3),int(monitor_height-monitor_height/5)]



    
    
    
    
    
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
                
draw_peligro(screen)
pygame.display.update()
wait()
pygame.quit()
    