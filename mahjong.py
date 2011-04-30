#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pygame
import random
import os
from src import *

if __name__ == '__main__':
    # Systems initialisation
    graphics = graphic_system()
    jeu_mahjong = mahjong_board(graphics)
    
    # Piocher les 13 tuiles - REDO with real rules
    for player in range(4):
        for tile in range(13):
            jeu_mahjong.pioche(player, refresh=False)
        jeu_mahjong.refresh_player_gfx(player)
    jeu_mahjong.refresh_mur_gfx()
    
    # Framerate handling
    clock = pygame.time.Clock()
    
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for a in graphics.all_sprites:
                        print(a.clickCheck(event.pos))
        
        # Game handling
        jeu_mahjong.next_step()
        
        # Display handling
        graphics.screen.fill(white)
        graphics.draw_game()
        
        # Limit to 30 frames per second
        clock.tick(30)
        
        # Buffering
        pygame.display.flip()
        
    pygame.quit()