"""tests/test_colorbackground.py"""

import colorcet as cc
from turtlefunt import colorbackground as cb
import logging
from os.path import join
    
def test_init_fix_color(caplog):
    with caplog.at_level(logging.DEBUG):
        b = cb.ColorBackground(palette="black")
        b.get_image()
        assert "Successfully created image with color 'black'" in caplog.text
        
def test_width_no_text():
    b = cb.ColorBackground(size_by_text="")
    b.get_size_from_text()
    assert b.width == 1
    
def test_size_fixed():
    b = cb.ColorBackground(width=123, height=456)
    b.get_size_from_text()
    assert b.width == 123
    assert b.height == 456
    
def test_default_size(caplog, tmp_path):
    with caplog.at_level(logging.DEBUG):
        b = cb.ColorBackground()
        b.get_image()
        assert "Successfully created transparent image." in caplog.text
        b.get_image().save(join(tmp_path, "transparent.png"))
    assert b.width == 720 # experimentally determined, adjust if default values change
    assert b.height == 252
    
def test_create_image_twice():
    b = cb.ColorBackground()
    b.get_image()
    b.get_image()
    
def test_color_tuple(tmp_path):
    b = cb.ColorBackground(palette=(255, 0, 0))
    b.get_image().save(join(tmp_path, "red.png"))
    
def test_invalid_palette(caplog):
    with caplog.at_level(logging.CRITICAL):
        b = cb.ColorBackground(palette=True)
        b.get_image()
        assert "Palette type is unkown" in caplog.text
    
def test_get_color_no_color(caplog):
    with caplog.at_level(logging.CRITICAL):
        b = cb.ColorBackground(palette="notreallyapallette")
        c = b._get_color(0.5)
        assert c == (255, 255, 255)
        assert "Palette returns invalid color code! Returning white as default!" in caplog.text
        
def test_get_color_text_hex_color():
    b = cb.ColorBackground(palette=cc.b_cyclic_mybm_20_100_c48)
    c = b._get_color(0)
    assert c == (194, 127, 116)
    
def test_get_color_fractions():
    b = cb.ColorBackground(palette=cc.cyclic_mybm_20_100_c48)
    c = b._get_color(0)
    assert c == (194, 127, 117)
    
def test_get_color_fraction_less_than_zero():
    b = cb.ColorBackground(palette=cc.b_cyclic_mybm_20_100_c48)
    c = b._get_color(-5)
    assert c == (194, 127, 116)
    
def test_get_color_fraction_greater_one():
    b = cb.ColorBackground(palette=cc.b_cyclic_mybm_20_100_c48)
    c = b._get_color(5)
    assert c == (193, 125, 117)
    
def test_image_palette_linear_diagonal(tmp_path, caplog):
    with caplog.at_level(logging.DEBUG):
        b = cb.ColorBackground(palette=cc.b_cyclic_mybm_20_100_c48)
        b.get_image().save(join(tmp_path, "cyclic_palette_linear_diagonal.png"))
        assert "Drawing linear diagonal background." in caplog.text
        assert "Flipping background image." not in caplog.text
        assert "Mirroring background image." not in caplog.text

def test_image_palette_linear_diagonal_mirror(tmp_path, caplog):    
    with caplog.at_level(logging.DEBUG):    
        b = cb.ColorBackground(palette=cc.b_cyclic_mybm_20_100_c48, transform=cb.MIRROR)
        b.get_image().save(join(tmp_path, "cyclic_palette_linear_diagonal_mirror.png"))
        assert "Drawing linear diagonal background." in caplog.text
        assert "Flipping background image." not in caplog.text
        assert "Mirroring background image." in caplog.text
    
def test_image_palette_linear_diagonal_flip(tmp_path, caplog):    
    with caplog.at_level(logging.DEBUG):    
        b = cb.ColorBackground(palette=cc.b_cyclic_mybm_20_100_c48, transform=cb.FLIP)
        b.get_image().save(join(tmp_path, "cyclic_palette_linear_diagonal_flip.png"))
        assert "Drawing linear diagonal background." in caplog.text
        assert "Flipping background image." in caplog.text
        assert "Mirroring background image." not in caplog.text
    
def test_image_palette_linear_diagonal_flip_mirror(tmp_path, caplog):
    with caplog.at_level(logging.DEBUG):    
        b = cb.ColorBackground(palette=cc.b_cyclic_mybm_20_100_c48, transform=cb.FLIP * cb.MIRROR)
        b.get_image().save(join(tmp_path, "cyclic_palette_linear_diagonal_flip_mirror.png"))
        assert "Drawing linear diagonal background." in caplog.text
        assert "Flipping background image." in caplog.text
        assert "Mirroring background image." in caplog.text
    
def test_image_palette_linear_vertical(tmp_path, caplog):
    with caplog.at_level(logging.DEBUG):
        b = cb.ColorBackground(palette=cc.b_cyclic_mybm_20_100_c48, direction=cb.VERTICAL)
        b.get_image().save(join(tmp_path, "cyclic_palette_linear_vertical.png"))
        assert "Drawing linear vertical background." in caplog.text
        assert "Flipping background image." not in caplog.text
        assert "Mirroring background image." not in caplog.text
    
def test_image_palette_linear_horizontal(tmp_path, caplog):
    with caplog.at_level(logging.DEBUG):
        b = cb.ColorBackground(palette=cc.b_cyclic_mybm_20_100_c48, direction=cb.HORIZONTAL)
        b.get_image().save(join(tmp_path, "cyclic_palette_linear_horizontal.png"))
        assert "Drawing linear horizontal background." in caplog.text
        assert "Flipping background image." not in caplog.text
        assert "Mirroring background image." not in caplog.text

def test_image_palette_linear_invalid_direction(caplog):
    with caplog.at_level(logging.CRITICAL):
        b = cb.ColorBackground(palette=cc.b_cyclic_mybm_20_100_c48, direction=cb.CENTER)
        b.get_image()
        assert "Invalid direction " + str(cb.CENTER) + " identified" in caplog.text
        
def test_image_palette_circular_center(tmp_path, caplog):
    with caplog.at_level(logging.DEBUG):
        b = cb.ColorBackground(palette=cc.b_cyclic_mybm_20_100_c48, direction=cb.CENTER, mode=cb.CIRCULAR)
        b.get_image().save(join(tmp_path, "cyclic_palette_circular_center.png"))
        assert "Drawing circular centered background." in caplog.text
        
def test_image_palette_circular_horizontal(tmp_path, caplog):
    with caplog.at_level(logging.DEBUG):
        b = cb.ColorBackground(palette=cc.b_cyclic_mybm_20_100_c48, direction=cb.HORIZONTAL, mode=cb.CIRCULAR)
        b.get_image().save(join(tmp_path, "cyclic_palette_circular_horizontal.png"))
        assert "Drawing circular horizontal background." in caplog.text
        
def test_image_palette_circular_vertical(tmp_path, caplog):
    with caplog.at_level(logging.DEBUG):
        b = cb.ColorBackground(palette=cc.b_cyclic_mybm_20_100_c48, direction=cb.VERTICAL, mode=cb.CIRCULAR)
        b.get_image().save(join(tmp_path, "cyclic_palette_circular_vertical.png"))
        assert "Drawing circular vertical background." in caplog.text
 
def test_image_palette_circular_diagonal(tmp_path, caplog):
    with caplog.at_level(logging.DEBUG):
        b = cb.ColorBackground(palette=cc.b_cyclic_mybm_20_100_c48, direction=cb.DIAGONAL, mode=cb.CIRCULAR)
        b.get_image().save(join(tmp_path, "cyclic_palette_circular_diagonal.png"))
        assert "Drawing circular diagonal background." in caplog.text
