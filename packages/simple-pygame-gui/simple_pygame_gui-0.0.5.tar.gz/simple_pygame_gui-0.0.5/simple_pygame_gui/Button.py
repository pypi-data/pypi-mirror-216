import time
import pygame
from importlib import resources
import io

pygame.init()
pygame.font.init()

class Button:
    def __init__(
        self,
        x: int=0, 
        y: int=0,
        width: int=100, 
        height: int=40,
        target=None,
        args=(), 
        text: str="Button", 
        font: str="FreeSans.ttf",
        font_size: int=20,
        text_color: tuple[int]=(0, 0, 0), 
        button_color: tuple[int]=(200, 200, 200),
        click_color: tuple[int]=(202, 225, 255),
        border_radius: int=3
    ) -> None:
        """Creates a Button that can be costumized. Set a target function. If the target function is None. The Button
        will be initialized, but will have no effect.
        
        Use Button.draw(screen) to draw the button to your pygame screen
        Use Button.handle_event(event) to make the button clickable.

        Args:
            x (int, optional): x position of the Button. Defaults to 0.
            y (int, optional): x position of the Button. Defaults to 0.
            width (int, optional): width of the button. Defaults to 100.
            height (int, optional): height of the button. Defaults to 40.
            target (optional): the target function. Defaults to None.
            args (tuple, optional): the arguments for target if needed (if one argument enter it like this (arg,)). Defaults to ().
            text (str, optional): text displayed on the button. Defaults to "Button".
            font (str, optional): the font of the text on the button. Defaults to "FreeSans.ttf".
            font_size (int, optional): the size of the text on the button. Defaults to 20.
            text_color (tuple[int], optional): the color of the text on the button. Defaults to (0, 0, 0).
            button_color (tuple[int], optional): the color of the button. Defaults to (200, 200, 200).
            click_color (tuple[int], optional): the color of the button when clicked. Defaults to (202, 225, 255).
            border_radius (int, optional): sets the border radius of the Button (rounds the edges). Defaults to 3.
        """
        
        # load font
        with resources.open_binary('simple_pygame_gui', font) as fp:
            self._font = fp.read()
        self._font = pygame.font.Font(io.BytesIO(self._font), font_size)
        
        if(target == None):
            print('\nWARNING: no target function set!\n')
        
        self._target = target
        self._args = args
        self._rect = pygame.Rect(x, y, width, height)
        
        txt_width, txt_height = self._font.size(text)
        self._textrect = pygame.Rect(x + (width / 2 - txt_width / 2), y + (height / 2 - txt_height / 2), width, height)
        self._text = text
        self._selected = False
        self._textColor = text_color
        self._buttonColor = button_color
        self._time = time.time()
        self._click_color = click_color
        self._border_radius = border_radius
        

    def _on_click(self) -> None:
        """
        Executes the function set as target
        """
        if self._target == None:
            return
        self._target(*self._args)


    def handle_event(self, event: pygame.event.Event) -> None:
        """This method handles the pygame events to make the button clickable

        Args:
            event (pygame.event.Event): insert event from for event in pygame.event.get()
        """
        if event.type == pygame.MOUSEBUTTONDOWN and self._rect.collidepoint(event.pos):
            self._time = time.time()
            self._selected = True
            self._on_click()


    def draw(self, surface: pygame.Surface) -> None:
        """This method draws the button to the screen

        Args:
            surface (pygame.Surface): the pygame surface the button should be displayed on
        """
        # illuminate the button if clicked
        if time.time() - self._time > 0.05:
            self._selected = False
        if self._selected:
            pygame.draw.rect(surface, self._click_color, self._rect, border_radius=self._border_radius)

        else:
            pygame.draw.rect(surface, self._buttonColor, self._rect, border_radius=self._border_radius)
        TXT = self._font.render(self._text, True, self._textColor)
        surface.blit(TXT, self._textrect)
