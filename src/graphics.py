#-*- coding: utf-8 -*-
import pygame
import random
import os

black    = (   0,   0,   0)
white    = ( 255, 255, 255)

DISPLAY_WIDTH  = 1024
DISPLAY_HEIGHT = 1024
TILE_WIDTH     = -1 # Dynamique
TILE_HEIGHT    = -1 # Idem

class graphic_system(object):
    def __init__(self):
        global DISPLAY_WIDTH, DISPLAY_HEIGHT
        pygame.init()
        self.screen=pygame.display.set_mode([DISPLAY_WIDTH, DISPLAY_HEIGHT])
        self.all_sprites = pygame.sprite.OrderedUpdates()
        self.all_text = []

    def add_sprite(self, sprite):
        self.all_sprites.add(sprite)
        
    def clear_all_sprites(self):
        self.all_sprites.empty()
    
    def remove_sprite(self, sprite):
        self.all_sprites.remove(sprite)
        
    def add_text(self, text):
        self.all_text.append(text)
        
    def remove_text(self, text):
        self.all_text.remove(text)
        
    def clear_text(self):
        self.all_text = []
        
    def draw_game(self):
        # Draw Sprites
        self.all_sprites.draw(self.screen)
        
        # Draw Texts
        for text in self.all_text:
            self.screen.blit(text.get_rendering(), text.get_position())

            
class mouse_cursor_underlay(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
        
        self.image = pygame.Surface([1, 1])
        self.image.fill(white)
        self.image.set_colorkey(white)
        
        self.rect = self.image.get_rect()
