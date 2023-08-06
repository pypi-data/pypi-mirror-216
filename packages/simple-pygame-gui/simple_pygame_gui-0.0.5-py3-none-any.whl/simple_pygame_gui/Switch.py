import pygame
from importlib import resources
import io


class Switch:
    def __init__(
        self, 
        x: int=0, 
        y: int=0, 
        width: int=70, 
        height:int=35,
        use_sprite: bool=True,
        on_sprite: str=None,
        off_sprite: str=None,
        state: bool=True, 
        name: str='', 
        font: str='FreeSans.ttf', 
        font_size: int=20,
        text_color: tuple[int]=(0, 0, 0),
        outline_color: tuple[int]=(135, 135, 135),
        base_color: tuple[int]=(150, 150, 150),
        on_color: tuple[int]=(0, 139, 0),
        off_color: tuple[int]=(205, 55, 0),
        inner_color: tuple[int]=(170, 170, 170)
        ):
        if use_sprite and (on_sprite == None and off_sprite == None):
            with resources.open_binary('simple_pygame_gui', 'Switch_on.png') as on:
                self._on_Sprite = on.read()
            self._on_Sprite = pygame.image.load(io.BytesIO(self._on_Sprite)).convert_alpha()
            
            with resources.open_binary('simple_pygame_gui', 'Switch_off.png') as off:
                self._off_Sprite = off.read()
            self._off_Sprite = pygame.image.load(io.BytesIO(self._off_Sprite)).convert_alpha()
            
            width = 70
            height = 35
        elif use_sprite:
            self._on_Sprite = pygame.image.load(on_sprite)
            self._off_Sprite = pygame.image.load(off_sprite)
        
        with resources.open_binary('simple_pygame_gui', font) as fp:
            name_font = fp.read()
        name_font = pygame.font.Font(io.BytesIO(name_font), font_size)
        
        self._use_sprite = use_sprite 
        self._state = state
        self._name_label = name_font.render(name, True, text_color)
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._bg_rect = pygame.Rect(x, y, width, height)
        self._base_rect = pygame.Rect(x + 2, y + 2, width - 4, height - 4)
        self._on_rect = pygame.Rect(x + 4, y + 4, (width - 4) / 2 - 2, height - 8)
        self._off_rect = pygame.Rect(x + width / 2, y + 4, (width - 4) / 2 - 2, height - 8)
        self._outline_color = outline_color
        self._base_color = base_color
        self._on_color = on_color
        self._off_color = off_color
        self._inner_color = inner_color


    def __bool__(self):
        return self._state
    
    
    def get_state(self):
        return self._state


    def draw(self, surface):
        if not self._use_sprite:
            pygame.draw.rect(surface, self._outline_color, self._bg_rect)
            pygame.draw.rect(surface, self._base_color, self._base_rect)
            pygame.draw.rect(surface, self._on_color, self._on_rect)
            pygame.draw.rect(surface, self._off_color, self._off_rect)

            if not self._state:
                pygame.draw.rect(surface, self._inner_color, self._on_rect)
            else:
                pygame.draw.rect(surface, self._inner_color, self._off_rect)

        else:
            if not self._state:
                surface.blit(self._off_Sprite, self._bg_rect)
            else:
                surface.blit(self._on_Sprite, self._bg_rect)

        w, h = self._name_label.get_size()
        surface.blit(self._name_label, (self._x + (self._width - w) / 2, self._y - h - 2))


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._on_rect.collidepoint(event.pos) or self._off_rect.collidepoint(event.pos):
                self._state = not self._state

