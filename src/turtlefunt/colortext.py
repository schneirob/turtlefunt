"""src/turtlefunt/colortext.py"""

from PIL import Image, ImageDraw
from typing import Union, Tuple

from .colorbackground import ColorBackground

class ColorText(ColorBackground):
    """Create transparent image with colored text"""
    
    def get_image(
        self,
        bold:bool | None = False,
        background:Union[str, Tuple[int, int, int], None] | None = None,
    ) -> Image:
        """Get image of colored text"""
        w, h = self.get_size_from_text()
        b = int(round(self.font_size / 100 * 1.5, 0))
        if b <= 0:
            b = 1
        if bold:
            self.width += 2 * b
            self.height += 2 * b
            
        self.create_image()
        
        textmask = Image.new("L", (self.width, self.height), "black")
        draw = ImageDraw.Draw(textmask)
        
        xoffset = int(round((self.width - w) / 2, 0))
        yoffset = int(round((self.height - h) / 2, 0))
        for line in self.text.split("\n"):
            if bold:
                draw.text((xoffset - b, yoffset - b), line, 255, self.font)
                draw.text((xoffset + b, yoffset - b), line, 255, self.font)
                draw.text((xoffset - b, yoffset + b), line, 255, self.font)
                draw.text((xoffset + b, yoffset + b), line, 255, self.font)
            else:
                draw.text((xoffset, yoffset), line, "white", self.font)
            
            yoffset += self.line_height
            
        transparent = Image.new("RGBA", (self.width, self.height), background)
        transparent.paste(self._image, (0, 0), textmask)
        
        return transparent
        