
import colorcet as cc
from turtlefunt.palette import TurtlePalette, get_all_colorcet_cyclic_turtle_palettes

def test_double_first():
    p = TurtlePalette([1,2,3,4,5,6,7,8])
    
    a, b = p.get_double_first()
    
    assert a == [8,7,6,5,4,3,2,1,8,7,6,5,4,3,2,1]
    assert b == [1,2,3,4,4,3,2,1]
    
def test_double_second():
    p = TurtlePalette([1,2,3,4,5,6,7,8])
    
    a, b = p.get_double_second()
    
    assert a == [1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8]
    assert b == [5,6,7,8,8,7,6,5]
    
def test_normal():
    p = TurtlePalette([1,2,3,4,5,6,7,8])
    
    a, b = p.get_normal()
    
    assert a == [4,3,2,1,8,7,6,5,5,6,7,8,1,2,3,4]
    assert b == [1,2,3,4,5,6,7,8]
    
def test_quadrupel():
    p = TurtlePalette([1,2,3,4])
    
    a, b = p.get_quadrupel()
    
    assert a == [1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4]
    assert b == [1,2,3,4,4,3,2,1]
    
def test_all():
    p = TurtlePalette([1,2])
    
    a = p.get_all()
    
    assert len(a) == 8
    assert "double_first" in a
    assert "double_first_revers" in a
    assert "double_second" in a
    assert "double_second_reverse" in a
    assert "normal" in a
    assert "normal_revers" in a
    assert "quadrupel" in a
    assert "quadrupel_reverse" in a

def test_create_samples(tmp_path):
    p = TurtlePalette(cc.b_cyclic_mybm_20_100_c48)
    
    p.create_samples(tmp_path)
    
def test_get_all_cyclic():
    get_all_colorcet_cyclic_turtle_palettes()
    
def test_get_all_cyclic_samples(tmp_path):
    get_all_colorcet_cyclic_turtle_palettes(tmp_path)