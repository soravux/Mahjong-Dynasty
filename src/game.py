#-*- coding: utf-8 -*-
import pygame
import random
import os
from graphics import DISPLAY_WIDTH, DISPLAY_HEIGHT, TILE_WIDTH, TILE_HEIGHT
from graphics import black, white # Redo with class, plz

MEDIA_PATH = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'tiles')

class mahjong_text(pygame.font.Font):
    def __init__(self, text, x, y):
        pygame.font.Font.__init__(self, None, 30) # Font, size en pt
        self.text = text
        self.x = x
        self.y = y
    
    def get_rendering(self):
        return self.render(self.text, True, black) # text, anti-aliasing, color
    
    def get_position(self):
        return [self.x, self.y]


class mahjong_tile(pygame.sprite.Sprite):
    def __init__(self, filename):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
        
        self.name = filename
        
        self.hidden = pygame.image.load(os.path.join(MEDIA_PATH, "hidden.png")).convert()
        self.hidden.set_colorkey(white)
        self.tile = pygame.image.load(os.path.join(MEDIA_PATH, "MJ" + filename + ".png")).convert()
        self.tile.set_colorkey(white)
        
        # Visible par défault
        self.image = self.tile
        self.visible = True

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        global TILE_WIDTH, TILE_HEIGHT
        if TILE_WIDTH == -1:
            TILE_WIDTH = self.rect.width
        if TILE_HEIGHT == -1:
            TILE_HEIGHT = self.rect.height
            
    def set_angle(self, angle):
        rotate = pygame.transform.rotate
        self.image = rotate(self.tile if self.visible == True else self.hidden, angle)
    
    def set_visibility(self, visible=True):
        if visible:
            self.image = self.tile
            self.visible = True
        else:
            self.image = self.hidden
            self.visible = False
    
    def get_name(self):
        return self.name

class mahjong_board(object):
    """
    Tiles (44x53):
    d = Dragons
    f = Vents
    s = Bamboos
    t = Cercles
    w = Character
    """
    def __init__(self, graphic_system):
        self.graphic_system = graphic_system
        self.mur = []
        self.player = [[],[],[],[]]
        
        self.generate_mur()
        self.set_sprites_from_mur()
        self.refresh_mur_gfx()
        self.refresh_player_gfx(0)
        self.refresh_player_gfx(1)
        self.refresh_player_gfx(2)
        self.refresh_player_gfx(3)
        
        self.game_state = None
        self.player_actuel = 0
        
    
    def generate_mur(self):
        self.mur = [mahjong_tile(a+str(b)) for a in 'stw' for b in range(1,10)] + [mahjong_tile('d'+str(a)) for a in range(1,4)] + [mahjong_tile('f'+str(a)) for a in range(1,5)]
        self.mur += [mahjong_tile(a+str(b)) for a in 'stw' for b in range(1,10)] + [mahjong_tile('d'+str(a)) for a in range(1,4)] + [mahjong_tile('f'+str(a)) for a in range(1,5)]
        self.mur += [mahjong_tile(a+str(b)) for a in 'stw' for b in range(1,10)] + [mahjong_tile('d'+str(a)) for a in range(1,4)] + [mahjong_tile('f'+str(a)) for a in range(1,5)]
        self.mur += [mahjong_tile(a+str(b)) for a in 'stw' for b in range(1,10)] + [mahjong_tile('d'+str(a)) for a in range(1,4)] + [mahjong_tile('f'+str(a)) for a in range(1,5)]
        [a.set_visibility(False) for a in self.mur] # Hack de compréhension de liste
        random.shuffle(self.mur)
        
    def set_sprites_from_mur(self):
        self.graphic_system.clear_all_sprites()
        for a in self.mur:
            self.graphic_system.add_sprite(a)
    
    def get_next_mur_gfx_position(self):
        global DISPLAY_WIDTH, DISPLAY_HEIGHT, TILE_WIDTH, TILE_HEIGHT
        wdt_bnd_rto = 0.55 # Tile Width Bounding Ratio
        while True:
            for x in range(int(DISPLAY_WIDTH/2 + (TILE_WIDTH*wdt_bnd_rto*16)/2), int(DISPLAY_WIDTH/2 - (TILE_WIDTH*wdt_bnd_rto*16)/2), int(-TILE_WIDTH*wdt_bnd_rto)):
                for y in range(int(DISPLAY_HEIGHT/2 + (TILE_WIDTH*wdt_bnd_rto*(17))/2), int(DISPLAY_HEIGHT/2 + (TILE_WIDTH*wdt_bnd_rto*(17))/2 + 8), 6):
                    yield x, y, 0
            for y in range(int(DISPLAY_HEIGHT/2 + (TILE_WIDTH*wdt_bnd_rto*(16))/2), int(DISPLAY_HEIGHT/2 - (TILE_WIDTH*wdt_bnd_rto*(16))/2 ), int(-TILE_WIDTH*wdt_bnd_rto)):
                for x in range(int(DISPLAY_WIDTH/2 - (TILE_WIDTH*wdt_bnd_rto*17)/2) - (TILE_HEIGHT/2), int(DISPLAY_WIDTH/2 - (TILE_WIDTH*wdt_bnd_rto*17)/2) - (TILE_HEIGHT/2) - 8, -6):
                    yield x, y, 270
            for x in range(int(DISPLAY_WIDTH/2 - (TILE_WIDTH*wdt_bnd_rto*16)/2), int(DISPLAY_WIDTH/2 + (TILE_WIDTH*wdt_bnd_rto*16)/2), int(TILE_WIDTH*wdt_bnd_rto)):
                for y in range(int(DISPLAY_HEIGHT/2 - (TILE_WIDTH*wdt_bnd_rto*(17))/2), int(DISPLAY_HEIGHT/2 - (TILE_WIDTH*wdt_bnd_rto*(17))/2 + 8), 6):
                    yield x, y, 0
            for y in range(int(DISPLAY_HEIGHT/2 - (TILE_WIDTH*wdt_bnd_rto*(16))/2), int(DISPLAY_HEIGHT/2 + (TILE_WIDTH*wdt_bnd_rto*(16))/2 ), int(TILE_WIDTH*wdt_bnd_rto)):
                for x in range(int(DISPLAY_WIDTH/2 + (TILE_WIDTH*wdt_bnd_rto*17)/2) + (TILE_HEIGHT/2), int(DISPLAY_WIDTH/2 + (TILE_WIDTH*wdt_bnd_rto*17)/2) + (TILE_HEIGHT/2) + 8, 6):
                    yield x, y, 270
    
    def refresh_mur_gfx(self):
        
        """
        Actualise les sprites affichant le mur
        """
        fgx_pos_iterateur = self.get_next_mur_gfx_position()
        for tile in self.mur:
            x, y, angle = fgx_pos_iterateur.next()
            tile.set_angle(angle)
            tile.rect.x = x
            tile.rect.y = y
            
    
    def refresh_player_gfx(self, player=0):
        """
        Actualise les sprites affichant le mur
        """
        wdt_bnd_rto = 1.0 # Tile Width Bounding Ratio
        global DISPLAY_WIDTH, DISPLAY_HEIGHT, TILE_WIDTH, TILE_HEIGHT
        for num, tile in enumerate(self.player[player]):
            if player == 0:
                tile.rect.x = int(DISPLAY_WIDTH/2 - (TILE_WIDTH*wdt_bnd_rto*13)/2) + (TILE_WIDTH*wdt_bnd_rto*num)
                tile.rect.y = int(DISPLAY_HEIGHT/2 + (TILE_WIDTH*wdt_bnd_rto*(17))/2) + TILE_WIDTH/2
                tile.set_angle(0)
            elif player == 1:
                tile.rect.x = int(DISPLAY_WIDTH/2 - (TILE_WIDTH*wdt_bnd_rto*17)/2) - (TILE_HEIGHT/2) - TILE_HEIGHT
                tile.rect.y = int(DISPLAY_HEIGHT/2 - (TILE_WIDTH*wdt_bnd_rto*(13))/2) + (TILE_WIDTH*wdt_bnd_rto*num)
                tile.set_angle(90)
            elif player == 2:
                tile.rect.x = int(DISPLAY_WIDTH/2 + (TILE_WIDTH*wdt_bnd_rto*13)/2) - (TILE_WIDTH*wdt_bnd_rto*num)
                tile.rect.y = int(DISPLAY_HEIGHT/2 - (TILE_WIDTH*wdt_bnd_rto*(17))/2) - TILE_WIDTH/2
                tile.set_angle(180)
            else:
                tile.rect.x = int(DISPLAY_WIDTH/2 + (TILE_WIDTH*wdt_bnd_rto*17)/2) + (TILE_HEIGHT/2) - TILE_HEIGHT
                tile.rect.y = int(DISPLAY_HEIGHT/2 + (TILE_WIDTH*wdt_bnd_rto*(13))/2) - (TILE_WIDTH*wdt_bnd_rto*num)
                tile.set_angle(270)
    
    def reorder_player_hand(self, player=0):
        self.player[player].sort(key=lambda clef: clef.get_name())
    
    def pioche(self, player=0, refresh=True):
        # Déplacer la tile dans la main du joueur
        tile_piochee = self.mur.pop()
        if player == 0:
            tile_piochee.set_visibility(True)
        self.player[player].append(tile_piochee)
        self.reorder_player_hand(player)
        
        # Si on veut que la pioche regénère les graphiques (lent)
        if refresh:
            # Regenerer le mur
            self.refresh_mur_gfx()
            
            # Regenerer la vue du joueur
            self.refresh_player_gfx(player)
            
            
    def next_step(self):
    
        if self.game_state == "piocher":
            self.pioche(self.player_actuel)
            self.game_state = "waiting_action"
        elif self.game_state == "waiting_action":
            pass
        elif self.game_state == "done":
            self.player_actuel = (self.player_actuel + 1) if self.player_actuel <4 else 0
        else:
            # On débute ou on est perdu
            self.player_actuel = 0
            self.game_state = "piocher"