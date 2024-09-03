"""src/turtlefunt/colorbackground.py"""

import colorcet as cc
from PIL import Image, ImageDraw, ImageFont
from typing import Union, Iterable, Tuple, Final, Literal

LINEAR:Final[int] = 0
CIRCULAR:Final[int] = 1


class ColorBackground:
    """Provide colored backgrounds"""
    
    def __init__(
        self,
        width:Union[int, None] | None = None,
        height:Union[int, None] | None = None,
        palette:Union[Iterable, list, str, Tuple[int, int, int], None] | None = None,
        mode:Literal[0, 1] | None = LINEAR,
        font:str | None = "./freefont/FreeMonoBold.ttf",
        font_size:int | None = 60,
        size_by_text:str | None = "REPEAT 999999999 [ \n  RT # * 0.12345678 \n  FD 100000 \n]",
        spacing:Union[int, float] | None = 0.1,
    ) -> None:
        """Initialize colored background creation
        
        Args:
            width (int): with of background image
            height (int): height of background image
            palette (Iterable, list): Color palette, color name or color tuple
            mode (LINEAR, CIRCULAR): draw colors in lines or circles on the background
            font (str): path to ttf font file for size creation by text
            font_size (int): size of font for test text creation
            size_by_text (str): sample text to size the image by
            spacing (int, float): text spacing between lines in fraction of textheight (e.g. 0.1 == 10%)
        """
        
        self.width = width
        self.height = height
        self.draw_mode = mode
        
        self.palette = palette
        
        self.font = ImageFont.truetype(font, font_size)
        self.text = size_by_text
        self.spacing = spacing
        
        self.color_mode = "RGB"
        if self.palette is None:
            self.color_mode = "RGBA"
        
        self._image = None
        self.get_size_from_text()
        self.create_image()
        
    def get_size_from_text(
        self,
        force:bool | None = False,
        ) -> None:
        """Generate image dimensions by test text
        
        Args:
            force (bool): force creation, even though dimensions are not None
        """
        if self.height is not None and self.width is not None and not force:
            return
        
        image = Image.new("RGBA", (100,100))
        draw = ImageDraw.Draw(image)
        
        _, _, _, self.height = draw.textbbox((0, 0), self.text.replace("\n", ""), font=self.font) # height of line in all text
        self.height = int(round(self.height * (1 + self.spacing), 0)) # add spacing
        self.height = int(self.height * len(self.text.split("\n"))) # number of lines
        
        self.width = 1
        for line in self.text.split("\n"):
            _, _, w, _ = draw.textbbox((0, 0), line, font=self.font)
            self.width = max(w, self.width)
    
    def create_image(
        self,
        force:bool | None = False,
        ) -> None:
        """Create background image
        
        Args:
            force (bool): force recreation of image, even if it exists
        """
        
        