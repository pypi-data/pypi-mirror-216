import pygame
from importlib import resources
import io

pygame.init()

SELECTED = pygame.color.Color(220, 255, 255)
TEXT_COLOR = pygame.color.Color(70, 70, 70)
with resources.open_binary('simple_pygame_gui', 'FreeSans.ttf') as fp:
    FONT = fp.read()
FONT = pygame.font.Font(io.BytesIO(FONT), 25)

class TextBox:
    def __init__(self, x, y, width = 25, height = 25, standardValue = "", name = "", nameColor = (50, 50, 50)):
        if width < 25 or height < 25:
            raise ValueError("minumum dimensions must be 25")
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = str(standardValue)
        self.bgRect = pygame.Rect(self.x - 2, self.y - 2, self.width + 4, self.height + 4)
        self.fgRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.txt = FONT.render(str(standardValue), True, TEXT_COLOR)
        self.rectColor = (255, 255, 255)
        self.name = name
        self.nameColor = nameColor
        self.selected = False
        self.savedValue = standardValue
        self.st_val = standardValue


    def getValue(self):
        return self.value


    def draw(self, surface):
        pygame.draw.rect(surface, (50, 50, 50), self.bgRect)
        pygame.draw.rect(surface, self.rectColor, self.fgRect)

        NAME = FONT.render(self.name, True, self.nameColor)
        TEXT = FONT.render(str(self.value), True, TEXT_COLOR)
        width, height = NAME.get_size()

        surface.blit(NAME, (self.x - ((width - self.width) / 2), self.y - 25))
        surface.blit(TEXT, (self.x + 2, self.y + self.height / 2 - 8))


    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.fgRect.collidepoint(event.pos):
                self.__selected = not self.__selected
            else:
                self.__selected = False

            self.rectColor = SELECTED if self.selected else (255, 255, 255)

        if event.type == pygame.KEYDOWN:
            if self.selected:
                if event.key == pygame.K_RETURN:
                    self.savedValue = self.value
                    # self.value = stValue
                if event.key == pygame.K_BACKSPACE:
                    self.value = self.value[:-1]
                elif self.txt.get_width() < self.width - 10:
                    self.value += event.unicode

                # Rendering the text
                self.__txt = FONT.render(self.value, True, TEXT_COLOR)