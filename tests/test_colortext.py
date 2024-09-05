"""tests/test_colortext.py"""

import colorcet as cc
import os

from turtlefunt.colortext import ColorText

def test_colortext_basic(tmp_path):
    ColorText(palette="white").get_image().save(os.path.join(tmp_path, "basic_default.png"))
    
def test_colortext_larger_base_image(tmp_path):
    ColorText(
        palette=cc.b_cyclic_mybm_20_100_c48,
        width=2000,
        height=2000,
    ).get_image().save(os.path.join(tmp_path, "basic_default.png"))
    
def test_colortext_larger_text(tmp_path):
    ColorText(
        palette=cc.b_cyclic_mybm_20_100_c48,
        font_size=300,
    ).get_image().save(os.path.join(tmp_path, "basic_default.png"))
    
def test_colortext_larger_text_on_black(tmp_path):
    ColorText(
        palette=cc.b_cyclic_mybm_20_100_c48,
        font_size=300,
    ).get_image(background="black").save(os.path.join(tmp_path, "basic_default_large.png"))
    ColorText(
        palette=cc.b_cyclic_mybm_20_100_c48,
        font_size=300,
    ).get_image(background="black", bold=True).save(os.path.join(tmp_path, "basic_default_large_bold.png"))
    ColorText(
        palette=cc.b_cyclic_mybm_20_100_c48,
        font_size=30,
    ).get_image(background="black").save(os.path.join(tmp_path, "basic_default_small.png"))
    ColorText(
        palette=cc.b_cyclic_mybm_20_100_c48,
        font_size=30,
    ).get_image(background="black", bold=True).save(os.path.join(tmp_path, "basic_default_small_bold.png"))
    
def test_colortext_alternate_text(tmp_path):
    ColorText(
        palette=cc.b_cyclic_mybm_20_100_c48,
        font_size=300,
        text="The quick brown fox jumps over the lazy dog\nWaltz, bad nymph, for quick jigs vex.\nSphinx of black quartz, judge my vow.\nHow vexingly quick daft zebras jump!\nPack my box with five dozen liquor jugs.\n0123456789"
    ).get_image(background="black").save(os.path.join(tmp_path, "basic_default.png"))