from dataclasses import dataclass
from typing import List
class Field:
    def __init__(self, id = None):
        if id is None:
            import random
            self.id = random.randint(0,10000)
        else:
            self.id = None
        self.rule = Rule()
        self.net = [[]]
        self.events = []

    def fill_init(self):
        from random import choice
        self.net = [[choice(self.rule.colors) for _y in range(self.rule.y_len)] for _x in range(self.rule.x_len)]
        return self.net

@dataclass
class Element:
    id: int
    score_multiplicator: int = 1

    def __str__(self):
        return self.__class__.__name__[0]

@dataclass
class RedElement(Element):
    id: int = 2
@dataclass
class BlueElement(Element):
    id: int = 1

@dataclass
class GreenElement(Element):
    id: int = 3

@dataclass
class YellowElement(Element):
    id: int = 4

@dataclass
class BrownElement(Element):
    id: int = 5

preset = [RedElement(), BlueElement(), BrownElement(), YellowElement(), GreenElement()]
#Todo: do in in the function
@dataclass
class Rule:
    x_len: int = 5
    y_len: int = 5

    @property
    def colors(self):
        return preset

class Setto():
    pass

class Setto3():
    pass