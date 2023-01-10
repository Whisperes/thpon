from thpon.domain.model import *

def test_element():
    blue = BlueElement()
    red = RedElement()
    assert blue!=red

def test_Field_init():
    id = 1
    rule = Rule(x_len=0, y_len=20)
    f1 = Field(id, rule)
    f1.fill_init()
    assert isinstance(f1.net[0][0], Element)
    settos = f1.find_setto()
    assert len(settos)>0
    f1.kill_items(settos)
    assert f1.net[0][5] is None
    assert f1.score>0
    f1.shift_to_nones()
    assert f1.net[0][5]==BlueElement()
    assert f1.net[0][18] is None
    f1.fill_nones()
    assert f1.net[0][18] is not None
    assert f1.net[0][7]==YellowElement()
    f1.swap((0,7),(0,8))
    assert f1.net[0][8] == YellowElement()
