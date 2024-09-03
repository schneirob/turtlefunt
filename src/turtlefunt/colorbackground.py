"""src/turtlefunt/colorbackground.py"""

import colorcet as cc
from loguru import logger
import math
from PIL import Image, ImageDraw, ImageFont, ImageOps
from typing import Union, Iterable, Tuple, Final, Literal

LINEAR:Final[int] = 2
CIRCULAR:Final[int] = 3

DIAGONAL:Final[int] = 5
VERTICAL:Final[int] = 7
HORIZONTAL:Final[int] = 13
CENTER:Final[int] = 17

KEEP:Final[int] = 19
MIRROR:Final[int] = 23
FLIP:Final[int] = 29


class ColorBackground:
    """Provide colored backgrounds"""
    
    def __init__(
        self,
        width:Union[int, None] | None = None,
        height:Union[int, None] | None = None,
        palette:Union[Iterable, list, str, Tuple[int, int, int], None] | None = None,
        mode:Literal[LINEAR, CIRCULAR] | None = LINEAR,
        direction:Literal[DIAGONAL, VERTICAL, HORIZONTAL, CENTER] | None = DIAGONAL,
        transform:Literal[KEEP, MIRROR, FLIP, MIRROR * FLIP] | None = KEEP,
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
            direction (DIAGONAL, VERTICAL, HORIZONTAL, CENTER): main drawing direction (LINEAR does not support CENTER)
            transform (KEEP, MIRROR, FLIP, MIRROR * FLIP): transformation after generation
            font (str): path to ttf font file for size creation by text
            font_size (int): size of font for test text creation
            size_by_text (str): sample text to size the image by
            spacing (int, float): text spacing between lines in fraction of textheight (e.g. 0.1 == 10%)
        """
        
        self.width = width
        self.height = height
        self.draw_mode = mode
        self.draw_direction = direction
        self.draw_transform = transform
        
        self.palette = palette
        
        self.font = ImageFont.truetype(font, font_size)
        self.text = size_by_text
        self.spacing = spacing
        
        self._image = None
        
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
    
    def _get_color(self, fraction:float) -> Tuple[int, int, int]:
        """Get the required color
        
        Args:
            fraction (float): current percentage of the way in the range between 0 and 1
        """
        color_num = int(round(len(self.palette) * fraction, 0))
        if color_num < 0:
            color_num = 0
        elif color_num > len(self.palette) - 1:
            color_num = len(self.palette) - 1
        
        color = self.palette[color_num]
        if type(color) is str and color.startswith("#") and len(color) == 7:
            color = color.lstrip('#')
            return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        elif type(color) is list and len(color) == 3:
            for index in range(len(color)):
                color[index] = int(round(color[index] * 255, 0))
            return tuple(color)
        else:
            logger.critical("Palette returns invalid color code! Returning white as default!")
            return (255, 255, 255)
    
    def _create_image_linear(self) -> None:
        """Create images with lines"""
        
        if self.draw_mode == LINEAR:
            if self.draw_direction == VERTICAL:
                self._create_image_linear_vertical()
            elif self.draw_direction == HORIZONTAL:
                self._create_image_linear_horizontal()
            elif self.draw_direction == DIAGONAL:
                self._create_image_linear_diagonal()
            else:
                logger.critical("Invalid direction {} identified", self.draw_direction)
        
    def _create_image_linear_diagonal(self):
        """Create image with diagonal lines"""
        
        logger.debug("Drawing linear diagonal background.")
        draw = ImageDraw.Draw(self._image)
        offset = min(self.width, self.height)
        
        steps = offset + self.width + 4
        
        for step in range(steps):
            draw.line((step - offset - 2, self.height + 10, step, -10), self._get_color(step / steps), 3)
        
    def _create_image_linear_vertical(self):
        """Create image with vertical lines"""
        
        logger.debug("Drawing linear vertical background.")
        draw = ImageDraw.Draw(self._image)
        
        for step in range(self.width + 1):
            draw.line((step, self.height + 10, step, -10), self._get_color(step / (self.width + 1)), 3)
       
    def _create_image_linear_horizontal(self):
        """Create image with horizontal lines"""
        
        logger.debug("Drawing linear horizontal background.")
        draw = ImageDraw.Draw(self._image)
        
        for step in range(self.height + 1):
            draw.line((-10, step, self.width + 10, step), self._get_color(step / (self.height + 1)), 3)
    
    def _create_image_circular(self):
        """Create background images using circles"""
        
        if self.draw_mode == CIRCULAR:
            if self.draw_direction == CENTER:
                self._create_image_circular_center()
            elif self.draw_direction == HORIZONTAL:
                self._create_image_circular_horizontal()
            elif self.draw_direction == VERTICAL:
                self._create_image_circular_vertical()
            elif self.draw_direction == DIAGONAL:
                self._create_image_circular_diagonal()
    
    def _create_image_circular_center(self):
        """Create background image using centered circles"""
        
        logger.debug("Drawing circular centered background.")
        draw = ImageDraw.Draw(self._image)
        
        center_width = int(round(self.width / 2, 0))
        center_height = int(round(self.height / 2, 0))
        
        radius = int(math.dist((0, 0), (center_width, center_height)) + 2)
        
        for r in reversed(range(radius)):
            draw.ellipse((center_width - (r + 1), center_height - (r + 1), center_width + (r + 1), center_height + (r + 1)), self._get_color(r / radius))
            
    def _create_image_circular_horizontal(self):
        """Create background image using horizontal circles"""
        
        logger.debug("Drawing circular horizontal background.")
        draw = ImageDraw.Draw(self._image)
        
        center_width = int(round(self.width / 2, 0))
        center_height = int(round(self.height + 10, 0))
        
        radius_end = int(math.dist((0, 0), (center_width, center_height)) + 2)
        radius_start = int(math.dist((center_width, center_height), (center_width, self.height)))
        
        for r in reversed(range(radius_end - radius_start)):
            draw.ellipse(
                (center_width - (r + 1 + radius_start),
                 center_height - (r + 1 + radius_start),
                 center_width + (r + 1 + radius_start),
                 center_height + (r + 1 + radius_start)),
                self._get_color(r / (radius_end - radius_start)))
             
    def _create_image_circular_vertical(self):
        """Create background image using vertical circles"""
        
        logger.debug("Drawing circular vertical background.")
        draw = ImageDraw.Draw(self._image)
        
        center_width = int(round(self.width + 10, 0))
        center_height = int(round(self.height / 2, 0))
        
        radius_end = int(math.dist((0, 0), (center_width, center_height)) + 2)
        radius_start = int(math.dist((center_width, center_height), (self.width, center_height)))
        
        for r in reversed(range(radius_end - radius_start)):
            draw.ellipse(
                (center_width - (r + 1 + radius_start),
                 center_height - (r + 1 + radius_start),
                 center_width + (r + 1 + radius_start),
                 center_height + (r + 1 + radius_start)),
                self._get_color(r / (radius_end - radius_start)))
             
    def _create_image_circular_diagonal(self):
        """Create background image using vertical circles"""
        
        logger.debug("Drawing circular diagonal background.")
        draw = ImageDraw.Draw(self._image)
        
        center_width = int(round(self.width + 10, 0))
        center_height = int(round(self.height + 10, 0))
        
        radius_end = int(math.dist((0, 0), (center_width, center_height)) + 2)
        radius_start = int(math.dist((center_width, center_height), (self.width, self.height)))
        
        for r in reversed(range(radius_end - radius_start)):
            draw.ellipse(
                (center_width - (r + 1 + radius_start),
                 center_height - (r + 1 + radius_start),
                 center_width + (r + 1 + radius_start),
                 center_height + (r + 1 + radius_start)),
                self._get_color(r / (radius_end - radius_start)))
                                    
    def _image_transform(self) -> None:
        """Flip or mirror image on request"""
                    
        if self.draw_transform % FLIP == 0:
            logger.debug("Flipping background image.")
            self._image = ImageOps.flip(self._image)
        if self.draw_transform % MIRROR == 0:
            logger.debug("Mirroring background image.")
            self._image = ImageOps.mirror(self._image)
                     
    def create_image(
        self,
        force:bool | None = False,
        ) -> None:
        """Create background image
        
        Args:
            force (bool): force recreation of image, even if it exists
        """
        if self._image is not None and not force:
            return
        
        if self.palette is None:
            self._image = Image.new("RGBA", (self.width, self.height))
            logger.debug("Successfully created transparent image.")
        elif type(self.palette) is str or type(self.palette) is tuple:
            self._image = Image.new("RGB", (self.width, self.height), self.palette)
            logger.debug("Successfully created image with color '{}'", self.palette)
        elif type(self.palette) is Iterable or type(self.palette) is list:
            self._image = Image.new("RGB", (self.width, self.height), "black")
            self._create_image_linear()
            self._create_image_circular()
        else:
            logger.critical("Palette type is unkown")

        self._image_transform()
        
    def get_image(self):
        """Return current background image"""
        self.get_size_from_text()
        self.create_image()
        return self._image
