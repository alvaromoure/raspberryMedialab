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
    screen = pygame.display.set_mode(monitor_size,FULLSCREEN)
    fullscreen = False
    running = True
    
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
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == VIDEORESIZE:
                screen = pygame.display.set_mode((event.w,event.h),RESIZABLE)
            if event.type == KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pygame.quit()
                if event.key == pygame.K_RIGHT:
                    screen.fill(BLACK)
                    circulo = circle(screen,RED,(cx,cy),300,10)
                    velocidad = myfont.render("80",1,WHITE)
                    velocidad_rect = velocidad.get_rect(center = circulo.center)
                    screen.blit(velocidad,velocidad_rect)
                    pygame.display.update()
    pygame.display.update()

    
if __name__ =="__main__":
    main()
    