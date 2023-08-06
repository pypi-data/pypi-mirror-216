import pygame

from TextBox import TextBox, SELECTED, TEXT_COLOR, FONT


class FloatBox(TextBox):
    savedValue = 0

    def __init__(self, x, y, width = 25, height = 25, standardValue = 0, name = "", nameColor = (50, 50, 50)):
        super().__init__(x, y, width, height, standardValue, name, nameColor)

        try:
            self.savedValue = float(standardValue)
        except:
            raise ValueError(f"{standardValue} is not a float")


    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.fgRect.collidepoint(event.pos):
                self.selected = not self.selected
            else:
                self.selected = False

            self.rectColor = SELECTED if self.selected else (255, 255, 255)

        if event.type == pygame.KEYDOWN:
            if self.selected:
                if event.key == pygame.K_RETURN:
                    try:
                        self.savedValue = float(self.value)
                    except:
                        self.savedValue = self.st_val
                    self.value = str(self.savedValue)
                if event.key == pygame.K_BACKSPACE:
                    self.value = self.value[:-1]
                elif self.txt.get_width() < self.width - 10 and event.unicode.isnumeric() or event.unicode == ".":
                    self.value += event.unicode

                # Rendering the text
                self.txt = FONT.render(str(self.value), True, TEXT_COLOR)
