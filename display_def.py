import pygame
import math
from pygame.locals import *
from pygame.draw import *

def main():
    pygame.init()
    pygame.display.set_caption("minimal program")
    BLACK = 0,0,0
    WHITE = 255,255,255
    RED = 255,0,0
    monitor_size = [pygame.display.Info().current_w,pygame.display.Info().current_h]
    screen = pygame.display.set_mode(monitor_size,RESIZABLE)
    fullscreen = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == VIDEORESIZE:
                screen = pygame.display.set_mode((event.w,event.h),RESIZABLE)
            if event.type == KEYDOWN:
                if event.key == pygame.K_LEFT:
                    running = False
                    pygame.quit()
                if event.key == pygame.K_RIGHT:
                    dibujar_display(self)
    pygame.display.update()
def dibujar_display(tamanio):
    pygame.display.set_mode(self.monitor_size,RESIZABLE)
    screen.fill(0,0,0)
    cx = int(screen.get_width()/2)
    cy = int(screen.get_height()/2)
    diameter = math.sqrt(pow(screen.get_width(),2)+pow(screen.get_height(),5))
    circulo = circle(screen,RED,(cx,cy),380,10)
    myfont = pygame.font.SysFont("Transport",480)
    velocidad = myfont.render("90",1,WHITE)
    velocidad_rotada = pygame.transform.rotate(velocidad,90)
    velocidad_rect = velocidad.get_rect(center = circulo.center)
    screen.blit(velocidad_rotada,velocidad_rect)   
    pygame.display.update()
    
    
if __name__ =="__main__":
    main()
    
