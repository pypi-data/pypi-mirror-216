import time
from abc import abstractmethod
import pygame
from importlib import resources
import io

pygame.init()
pygame.font.init()


class Button:
    def __init__(self, target, x, y, width, height, text="Button", font="FreeSans.ttf", fontSize=20, bold=False, italic=False, textColor=(0, 0, 0), buttonColor=(200, 200, 200)):
        """
        create a new class that overwrites the function "function"
        """
        if (target == None):
            ValueError('No function for target is specified')
        self.target = target
        self.rect = pygame.Rect(x, y, width, height)
        
        with resources.open_binary('simple_pygame_gui', font) as fp:
            self.font = fp.read()
        self.font = pygame.font.Font(io.BytesIO(self.font), fontSize)
        
        txt_width, txt_height = self.font.size(text)
        self.textrect = pygame.Rect(x + (width / 2 - txt_width / 2), y + (height / 2 - txt_height / 2), width, height)
        self.text = text
        self.selected = False
        self.textColor = textColor
        self.buttonColor = buttonColor
        self.time = time.time()
        self.event = pygame.USEREVENT
        pygame.time.set_timer(self.event, 200)


    def on_click(self):
        self.target()


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.time = time.time()
            self.selected = True
            self.on_click()


    def draw(self, surface):
        if time.time() - self.time > 0.05:
            self.selected = False
        if self.selected:
            pygame.draw.rect(surface, (202, 225, 255), self.rect, border_radius=3)

        else:
            pygame.draw.rect(surface, self.buttonColor, self.rect, border_radius=3)
        TXT = self.font.render(self.text, True, self.textColor)
        surface.blit(TXT, self.textrect)
