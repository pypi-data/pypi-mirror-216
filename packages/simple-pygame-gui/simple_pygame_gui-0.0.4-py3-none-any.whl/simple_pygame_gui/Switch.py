import pygame
from importlib import resources
import io


class Switch:
    def __init__(self, x, y, width=70, height=35, state=True, name="", font="FreeSans.ttf", fontSize=25):
        if width == 70 and height == 35:
            self.useSprite = True
            with resources.open_binary('simple_pygame_gui', 'Switch_on.png') as on:
                self.on_Sprite = on.read()
            self.on_Sprite = pygame.image.load(io.BytesIO(self.on_Sprite)).convert_alpha()
            
            with resources.open_binary('simple_pygame_gui', 'Switch_off.png') as off:
                self.off_Sprite = off.read()
            self.off_Sprite = pygame.image.load(io.BytesIO(self.off_Sprite)).convert_alpha()
        else:
            self.useSprite = False


        self.state = state
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        
        with resources.open_binary('simple_pygame_gui', font) as fp:
            self.font = fp.read()
        self.font = pygame.font.Font(io.BytesIO(self.font), fontSize)
        
        self.bgRect = pygame.Rect(x, y, width, height)
        self.baseRect = pygame.Rect(x + 2, y + 2, width - 4, height - 4)
        self.onRect = pygame.Rect(x + 4, y + 4, (width - 4) / 2 - 2, height - 8)
        self.offRect = pygame.Rect(x + width / 2, y + 4, (width - 4) / 2 - 2, height - 8)


    def __bool__(self):
        return self.state


    def draw(self, surface):
        if not self.useSprite:
            pygame.draw.rect(surface, (135, 135, 135), self.bgRect)
            pygame.draw.rect(surface, (150, 150, 150), self.baseRect)
            pygame.draw.rect(surface, (0, 139, 0), self.onRect)
            pygame.draw.rect(surface, (205, 55, 0), self.offRect)

            if not self.state:
                pygame.draw.rect(surface, (170, 170, 170), self.onRect)
            else:
                pygame.draw.rect(surface, (170, 170, 170), self.offRect)

        else:
            if not self.state:
                surface.blit(self.off_Sprite, self.bgRect)
            else:
                surface.blit(self.on_Sprite, self.bgRect)


        TXT = self.font.render(self.name, True, (0, 0, 0))
        w, h = TXT.get_size()
        surface.blit(TXT, (self.x + (self.width - w) / 2, self.y - h - 2))


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.onRect.collidepoint(event.pos) or self.offRect.collidepoint(event.pos):
                self.state = not self.state

