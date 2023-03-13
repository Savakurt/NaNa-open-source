import time
import pyglet
import pygame
def hello() :
    pygame.init()
    pygame.mixer.init()
    sounda2 = pygame.mixer.Sound("Hello.mp3")
    sounda2.play()
def goodbye():
    pygame.init()
    pygame.mixer.init()
    sounda2 = pygame.mixer.Sound("goodbye.mp3")
    sounda2.play()
def access():
    pygame.init()
    pygame.mixer.init()
    sounda3 = pygame.mixer.Sound("access.mp3")
    sounda3.play()
def cancel():
    pygame.init()
    pygame.mixer.init()
    sounda5 = pygame.mixer.Sound("cancel.mp3")
    sounda5.play()
def open():
    pygame.init()
    pygame.mixer.init()
    sounda6 = pygame.mixer.Sound("open.mp3")
    sounda6.play()
    time.sleep(3)
def shutdown():
    pygame.init()
    pygame.mixer.init()
    sounda7 = pygame.mixer.Sound("shutdown.mp3")
    sounda7.play()
def listening():
    pygame.init()
    pygame.mixer.init()
    sounda8 = pygame.mixer.Sound("listen.mp3")
    sounda8.play()
def creator():
    pygame.init()
    pygame.mixer.init()
    sounda9 = pygame.mixer.Sound("Who.mp3")
    sounda9.play()
