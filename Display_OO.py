import pygame
import math
from pygame.locals import *
from pygame.draw import *
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
        if(velocidad_viento<15 and velocidad_viento>10):
            return 100
        elif (velocidad_viento <20 and velocidad_viento>15):
            return 90
        elif (velocidad_viento <25 and velocidad_viento>20):
            return 70
        elif (velocidad_viento >25):
            return CODIGO_PELIGRO
        else return 0
    if(lluvia):
          if(velocidad_viento<15 and velocidad_viento>10):
            return 90
        elif (velocidad_viento <20 and velocidad_viento>15):
            return 70
        elif (velocidad_viento <25 and velocidad_viento>20):
            return CODIGO_PELIGRO
        elif (velocidad_viento >25):
            return CODIGO_PELIGRO
        else return 0
        
        


signal = displaySignal(90)
signal.draw(screen)
input()
pygame.quit()
        
        