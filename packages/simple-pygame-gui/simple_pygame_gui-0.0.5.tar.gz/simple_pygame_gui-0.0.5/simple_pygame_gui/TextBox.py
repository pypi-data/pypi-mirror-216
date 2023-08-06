import pygame
from importlib import resources
import io

pygame.init()


class TextBox:
    def __init__(
        self, 
        x: int=0, 
        y:int=0, 
        width: int=120, 
        height: int=30, 
        standard_value: str="",
        font: str='FreeSans.ttf',
        font_size: int=20,
        box_color: tuple[int]=(200, 200, 200),
        border: bool=True,
        border_color: tuple[int]=(70, 70, 70),
        border_radius: int=3,
        text_color: tuple[int]=(70, 70, 70),
        selected_text_color: tuple[int]=(0, 0, 0),
        selected_color: tuple[int]=(220, 255, 255),
        name = "", 
        name_color: str= (0, 0, 0)
        ) -> None:
        """Generates a textbox. the saved value can be returned using Textbox.get_value()

        Args:
            x (int, optional): the x position of the textbox. Defaults to 0.
            y (int, optional): the y position of the textbox. Defaults to 0.
            width (int, optional): the width of the textbox. Defaults to 120.
            height (int, optional): the height of the textbox. Defaults to 30.
            standard_value (str, optional): the value the textbox has when initialized. Defaults to "".
            font (str, optional): the font used for the text and name of the textbox. Defaults to 'FreeSans.ttf'.
            font_size (int, optional): the size of the font. Defaults to 20.
            box_color (tuple[int], optional): the color of the textbox. Defaults to (200, 200, 200).
            border (bool, optional): if True the textbox will have a displayed border. Defaults to True.
            border_color (tuple[int], optional): the color of the border of the textbox. Defaults to (70, 70, 70).
            border_radius (int, optional): smoothens the edge of the textbox. Defaults to 3.
            text_color (tuple[int], optional): the color of the text within the textbox if not selected. Defaults to (70, 70, 70).
            selected_text_color (tuple[int], optional): the color of the text within the textbox when selected. Defaults to (0, 0, 0).
            selected_color (tuple[int], optional): the color of the textbox when selected. Defaults to (220, 255, 255).
            name (str, optional): the name of the textbox that will be displayed above the textbox. Defaults to "".
            name_color (str, optional): the color of the name that will be displayed above the textbox. Defaults to (0, 0, 0).

        Raises:
            ValueError: a minimum height of 25 is required to be able to display the text correctly
        """
        if width < 25 or height < 25:
            raise ValueError("minumum dimensions must be 25")
        
        with resources.open_binary('simple_pygame_gui', font) as fp:
            self._font = fp.read()
        self._font = pygame.font.Font(io.BytesIO(self._font), font_size)
        self._text = self._font.render(str(standard_value), True, text_color)
        
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._value = str(standard_value)
        self._bgRect = pygame.Rect(self._x - 2, self._y - 2, self._width + 4, self._height + 4)
        self._fgRect = pygame.Rect(self._x, self._y, self._width, self._height)
        self._name = self._font.render(name, True, name_color)
        self._selected = False
        self._saved_val = standard_value
        self._st_val = standard_value
        self._box_color = box_color
        self._border_color = border_color if border else box_color
        self._selected_color = selected_color
        self._border_radius = border_radius
        self._text_color = text_color
        self._selected_text_color = selected_text_color
        self._current_box_color = box_color


    def get_value(self) -> str:
        """This method returns the value within the textbox

        Returns:
            str: the saved value within the textbox
        """
        return self._value


    def draw(self, surface: pygame.Surface) -> None:
        """This method displays the textbox on a given pygame surface

        Args:
            surface (pygame.Surface): the surface the textbox will be displayed on
        """
        pygame.draw.rect(surface, self._border_color, self._bgRect, border_radius=self._border_radius)
        pygame.draw.rect(surface, self._current_box_color, self._fgRect, border_radius=self._border_radius)

        text_width, text_height = self._text.get_size()
        name_width, name_height = self._name.get_size()

        surface.blit(self._name, (self._x - ((name_width - self._width) / 2), self._y - name_height))
        surface.blit(self._text, (self._x + 2, self._y - (text_height - self._height) / 2))


    def handleEvent(self, event: pygame.event.Event) -> None:
        """Eventhandler for pygame events makes the textbox accessable

        Args:
            event (pygame.event.Event): makes the textbox accessable
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._fgRect.collidepoint(event.pos):
                self._selected = not self._selected
            else:
                self._selected = False

        if event.type == pygame.KEYDOWN:
            if self._selected:
                if event.key == pygame.K_RETURN:
                    self._selected = False
                    self._saved_val = self._value
                    self._value = self._st_val
                elif event.key == pygame.K_BACKSPACE:
                    self._value = self._value[:-1]
                elif self._text.get_width() < self._width - 10:
                    self._value += event.unicode

        # Rendering the text
        text_color = self._text_color if not self._selected else self._selected_text_color
        self._text = self._font.render(self._value, True, text_color)
        self._current_box_color = self._selected_color if self._selected else self._box_color