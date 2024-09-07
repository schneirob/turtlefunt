"""src/turtlefunt/palette.py"""

import colorcet as cc
import os
from PIL import Image
from typing import Tuple
from .colorbackground import ColorBackground, Direction

def create_palette_sample(palette:list) -> Image:
    """Create a palette sample"""
    
    return ColorBackground(
        2048,
        500,
        palette,
        direction=Direction.VERTICAL,
    ).get_image()
    
def get_all_colorcet_cyclic_turtle_palettes(
    path:str | None = None,
) -> dict:
    """Collect all colorcet palettes that are cyclic in TurtlePalette format
    
    Args:
        path (str, None): if not None: create samples of palettes
    """
    
    palettes = {}
    for ccpalette, name in [
        (cc.b_cyclic_bgrmb_35_70_c75, "cyclic_bgrmb_35_70_c75"),
        (cc.b_cyclic_bgrmb_35_70_c75_s25, "cyclic_bgrmb_35_70_c75_s25"),
        (cc.b_cyclic_grey_15_85_c0, "cyclic_grey_15_85_c0"),
        (cc.b_cyclic_grey_15_85_c0_s25, "cyclic_grey_15_85_c0_s25"),
        (cc.b_cyclic_mrybm_35_75_c68, "cyclic_mrybm_35_75_c68"),
        (cc.b_cyclic_mrybm_35_75_c68_s25, "cyclic_mrybm_35_75_c68_s25"),
        (cc.b_cyclic_mybm_20_100_c48, "cyclic_mybm_20_100_c48"),
        (cc.b_cyclic_mybm_20_100_c48_s25, "cyclic_mybm_20_100_c48_s25"),
        (cc.b_cyclic_mygbm_30_95_c78, "cyclic_mygbm_30_95_c78"),
        (cc.b_cyclic_mygbm_30_95_c78_s25, "cyclic_mygbm_30_95_c78_s25"),
        (cc.b_cyclic_mygbm_50_90_c46, "cyclic_mygbm_50_90_c46"),
        (cc.b_cyclic_mygbm_50_90_c46_s25, "cyclic_mygbm_50_90_c46_s25"),
        (cc.b_cyclic_protanopic_deuteranopic_bwyk_16_96_c31, "cyclic_protanopic_deuteranopic_bwyk_16_96_c31"),
        (cc.b_cyclic_protanopic_deuteranopic_wywb_55_96_c33, "cyclic_protanopic_deuteranopic_wywb_55_96_c33"),
        (cc.b_cyclic_rygcbmr_50_90_c64, "cyclic_rygcbmr_50_90_c64"),
        (cc.b_cyclic_rygcbmr_50_90_c64_s25, "cyclic_rygcbmr_50_90_c64_s25"),
        (cc.b_cyclic_tritanopic_cwrk_40_100_c20, "cyclic_tritanopic_cwrk_40_100_c20"),
        (cc.b_cyclic_tritanopic_wrwc_70_100_c20, "cyclic_tritanopic_wrwc_70_100_c20"),
        (cc.b_cyclic_wrkbw_10_90_c43, "cyclic_wrkbw_10_90_c43"),
        (cc.b_cyclic_wrkbw_10_90_c43_s25, "cyclic_wrkbw_10_90_c43_s25"),
        (cc.b_cyclic_wrwbw_40_90_c42, "cyclic_wrwbw_40_90_c42"),
        (cc.b_cyclic_wrwbw_40_90_c42_s25, "cyclic_wrwbw_40_90_c42_s25"),
        (cc.b_cyclic_ymcgy_60_90_c67, "cyclic_ymcgy_60_90_c67"),
        (cc.b_cyclic_ymcgy_60_90_c67_s25, "cyclic_ymcgy_60_90_c67_s25"),
    ]:
        palette = TurtlePalette(ccpalette)
        palettes[name] = palette.get_all()
        
        if path is not None:
            palette.create_samples(os.path.join(path, name))
            

class TurtlePalette:
    """Modify palettes fit for purpose to draw
    Euler Spirals
    """
    
    def __init__(self, palette:list):
        """Initilize Turtle Palette
        
        Args:
            palette: List of colors, optimized for circular palettes
        """
        
        self.palette = palette
        self.middle = int(round(len(self.palette) / 2, 0))
        
    def get_double_first(self) -> Tuple[list, list]:
        """Flavour double first"""
        
        return (
            2 * (
                self.palette[:self.middle-1:-1] + 
                self.palette[self.middle-1::-1]
            ),
            self.palette[:self.middle] +
            self.palette[self.middle-1::-1]
        )
        
    def get_double_second(self) -> Tuple[list, list]:
        """Flavour double second"""
        
        return (
            2 * (
                self.palette    
            ),
            self.palette[self.middle:] +
            self.palette[:self.middle-1:-1]
        )
        
    def get_normal(self) -> Tuple[list, list]:
        """Flavour normal"""
        
        return (
            self.palette[self.middle-1::-1] + 
            self.palette[:self.middle-1:-1] +
            self.palette[self.middle:] + 
            self.palette[:self.middle],
            self.palette
        )
        
    def get_quadrupel(self) -> Tuple[list, list]:
        """Flavor quadrupel"""
        
        return(
            4 * (
                self.palette
            ),
            self.palette +
            self.palette[::-1]
        )
        
    def get_all(self) -> dict:
        """Get all palette flavors in a list"""
        palettes = {
            "double_first": self.get_double_first(),
            "double_first_revers": self.get_double_first(),
            "double_second": self.get_double_second(),
            "double_second_reverse": self.get_double_second(),
            "normal": self.get_normal(),
            "normal_revers": self.get_normal(),
            "quadrupel": self.get_quadrupel(),
            "quadrupel_reverse": self.get_quadrupel(),
        }
        
        for paldef in palettes:
            if paldef.endswith("_reverse"):
                turtle, text = palettes[paldef]
                turtle.reverse()
                text.reverse()
                palettes[paldef] = (turtle, text)
        
        return palettes
        
    def create_samples(
        self,
        path: str | None = "./palette_samples"
    ) -> None:
        """Create sample images"""
        
        os.makedirs(path, exist_ok=True)
        
        palettes = self.get_all()
        for paldef in palettes:
            create_palette_sample(palettes[paldef][0]).save(os.path.join(path, paldef + "_turtle.png"))
            create_palette_sample(palettes[paldef][1]).save(os.path.join(path, paldef + "_text.png"))
