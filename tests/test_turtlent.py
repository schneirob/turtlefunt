"""tests/test_turtlent.py"""

import colorcet as cc
from decimal import Decimal, getcontext
import logging
from PIL import Image
import pytest
from random import randrange as random

from turtlefunt.turtlent import decimal_places, TurtleNT, DEFAULT_IMAGE_HEIGHT, DEFAULT_IMAGE_WIDTH
from turtlefunt.turtlefun_quotientlist import TURTLEFUN_QUOTIENT_LIST
from turtlefunt.palette import TurtlePalette
from .turtle_originreturnsamples import TURTLE_ORIGIN_RETURN_SAMPLES
from .turtlefun_lines_manual import THETA_LINES


def test_decimal_places_int():
    assert decimal_places(int(5)) == 0
    assert decimal_places(5) == 0

def test_decimal_places_float():
    assert decimal_places(float(5)) == 0
    assert decimal_places(float(1.2)) == 1
    assert decimal_places(float(1.123)) == 3
    
def test_decimmal_places_exponent():
    assert decimal_places(float(1E-5)) == 5
    assert decimal_places(float(1.2E3)) == 0
    
def test_decimal_places_str():
    assert decimal_places("1.2345E3") == 1
    assert decimal_places("1.234E3") == 0
    assert decimal_places("1.24E3") == 0
    assert decimal_places("1.234E-7") == 10
    assert decimal_places("1") == 0
    assert decimal_places("1.0") == 0
    assert decimal_places("000001.123400000") == 4
    assert decimal_places("-1.234") == 3
    assert decimal_places(".1234") == 4

def test_init_theta():
    t = TurtleNT("0.1")
    assert t.get_theta() == Decimal("0.1")
    assert t.image_width == DEFAULT_IMAGE_WIDTH
    assert t.image_height == DEFAULT_IMAGE_HEIGHT
    assert t.stepsize == 100
    assert t.image_background == "black"
    
    t = TurtleNT(theta=5, image_width=10, image_height=20, stepsize=5, image_background="white")
    assert t.get_theta() == Decimal("5")
    assert t.image_width == 10
    assert t.image_height == 20
    assert t.stepsize == 5
    assert t.image_background == "white"
    
def test_origin_return_dominant_angles():
    for theta, quotient, alpha in TURTLEFUN_QUOTIENT_LIST[:20]:
        t = TurtleNT(theta)
        assert len(t.origin_return_estimation()) >= 1
        if alpha == 180:
            assert 2 * quotient in t.origin_return_estimation()
        else:
            assert quotient in t.origin_return_estimation()
            
def test_origin_return_origin_return_samples():
    for _r in range(50):
        # testing all takes nearly a minute...
        index = random(len(TURTLE_ORIGIN_RETURN_SAMPLES))
        theta, steps = TURTLE_ORIGIN_RETURN_SAMPLES[index]
        t = TurtleNT(str(theta))
        assert steps in t.origin_return_estimation()

def test_eurler_spiral_run_simple(tmp_path):
    
    t = TurtleNT('1', path=tmp_path)
    t.euler_spiral('720')
    t.save_image()
    
    x, y = t.get_pos()
    assert round(x, 10) == 0
    assert round(y, 10) == 0
    assert t.get_angle() == 0
    assert t.is_home() is True
    assert len(t._xpos_list) == 721
    assert len(t._ypos_list) == 721
    
def test_euler_sprial_straight_line():   
    t = TurtleNT('0')
    t.euler_spiral('100000')
    assert t.get_pos() == (100000 * t.stepsize, 0)
    assert t.get_angle() == 0
    
def test_eurler_spiral_run_simple_home_return_test(tmp_path):
    
    t = TurtleNT('1', path=tmp_path)
    t.euler_spiral()
    t.save_image()
    t._calculate_min_max_positions()
    
    x, y = t.get_pos()
    assert round(x, 10) == 0
    assert round(y, 10) == 0
    assert t.get_angle() == 0
    assert t.is_home() is True
    assert len(t._xpos_list) == 721
    assert len(t._ypos_list) == 721
    
def test_euler_sprial_transparent_image(tmp_path):   
    t = TurtleNT('1', image_background=None, path=tmp_path)
    t.euler_spiral()
    t.get_image(False, False, True)
    t.save_image()
    
def test_is_home_x_to_small(caplog):
    t = TurtleNT('180')
    t.set_angle('180')
    t.forward()
    t.forward()
    t.set_angle('0')
    with caplog.at_level(logging.DEBUG):
        assert t.is_home() is False
        assert "X is to small" in caplog.text
        
def test_is_home_y_to_small(caplog):
    t = TurtleNT('270')
    t.set_angle('270')
    t.forward()
    t.forward()
    t.set_angle('0')
    with caplog.at_level(logging.DEBUG):
        assert t.is_home() is False
        assert "Y is to small" in caplog.text
        
def test_is_home_y_to_big(caplog):
    t = TurtleNT('90')
    t.set_angle('90')
    t.forward()
    t.forward()
    t.set_angle('0')
    with caplog.at_level(logging.DEBUG):
        assert t.is_home() is False
        assert "Y is to big" in caplog.text
      
def test_is_home_x_to_big(caplog):
    t = TurtleNT('0')
    t.forward()
    t.forward()
    with caplog.at_level(logging.DEBUG):
        assert t.is_home() is False
        assert "X is to big" in caplog.text
   
def test_is_home_wrong_angle(caplog):
    t = TurtleNT('0')
    t.set_angle('90')
    with caplog.at_level(logging.DEBUG):
        assert t.is_home() is False
        assert "not in applicable range 359.5" in caplog.text
        
def test_step_limit_to_small():
    t = TurtleNT('1', steplimit=10)
    assert t.euler_spiral() is False

def test_file_exists(tmp_path):
    t = TurtleNT('1', path=tmp_path)
    t.euler_spiral()
    assert t.file_exists() is False
    t.save_image()
    assert t.file_exists() is True
    t2 = TurtleNT('2', path=tmp_path)
    t2.euler_spiral()
    assert t2.file_exists() is False
    t2.save_image()
    assert t.file_exists() is True
    assert t2.file_exists() is True
    
def test_get_image_twice():
    t = TurtleNT('1')
    assert type(t.get_image()) is Image.Image
    t.get_image()
    
def test_wrong_xpos_length():
    t = TurtleNT('1')
    t.euler_spiral()
    t._xpos_list.append(12)
    with pytest.raises(SystemExit) as e:
        t.get_image()
    assert e.type == SystemExit
    assert e.value.code == 1
    
def test_with_more_than_hundredthausend_steps(caplog):
    t = TurtleNT('179.7444')
    with caplog.at_level(logging.DEBUG):
        t.euler_spiral()
        t.get_image()
        assert "remaining time estimate" in caplog.text
        
def test_get_steps():
    t = TurtleNT('1')
    assert t.get_steps() == 0
    
def test_get_xmax():
    t = TurtleNT('1')
    assert t.get_xmax() == 0
    
def test_get_xmin():
    t = TurtleNT('1')
    assert t.get_xmin() == 0
    
def test_get_ymax():
    t = TurtleNT('1')
    assert t.get_ymax() == 0
    
def test_get_ymin():
    t = TurtleNT('1')
    assert t.get_ymin() == 0
    
def test_dominant_angles():
    t = TurtleNT('1')
    assert t.dominant_angles() == [1]
    assert t.dominant_angles() == [1]
    
def test_use_manual_filename(tmp_path):
    t = TurtleNT('1', path=tmp_path)
    t.euler_spiral()
    t.save_image("test.png")
    
def test_using_color_b_palette(tmp_path):
    t = TurtleNT('1', path=tmp_path, image_linecolor=cc.b_cyclic_bgrmb_35_70_c75)
    t.euler_spiral()
    t.save_image()
    
def test_using_color_palette(tmp_path):
    t = TurtleNT('1', path=tmp_path, image_linecolor=cc.cyclic_bgrmb_35_70_c75)
    t.euler_spiral()
    t.save_image()
    
def test_using_invalid_color_palette(tmp_path):
    t = TurtleNT('1', path=tmp_path, image_linecolor=["123", "234"])
    t.euler_spiral()
    t.save_image()
    
def test_turtle_palette(tmp_path):
    t = TurtleNT('1', path=tmp_path, image_linecolor=TurtlePalette(cc.b_cyclic_bgrmb_35_70_c75).get_double_second()[0])
    t.euler_spiral()
    t.save_image()