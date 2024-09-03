"""tests/test_colorbackground.py"""

from turtlefunt import colorbackground as cb

def test_init():
    cb.ColorBackground()
    
def test_init_fix_color():
    cb.ColorBackground(palette="black")
    
def test_width_no_text():
    b = cb.ColorBackground(size_by_text="")
    assert b.width == 1
    
def test_size_fixed():
    b = cb.ColorBackground(width=123, height=456)
    assert b.width == 123
    assert b.height == 456
    
def test_default_size():
    b = cb.ColorBackground()
    assert b.width == 720 # experimentally determined, adjust if default values change
    assert b.height == 252