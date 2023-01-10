from dataclasses import dataclass
from typing import List
from thpon.domain import events

@dataclass
class Element:
    id: int
    score_multiplicator: int = 1

    def __str__(self):
        return self.__class__.__name__[0]


@dataclass
class RedElement(Element):
    id: int = 2
    color: tuple = (255, 0, 0)

@dataclass
class BlueElement(Element):
    id: int = 1
    color: tuple = (0, 0, 255)

@dataclass
class GreenElement(Element):
    id: int = 3
    color: tuple = (0, 255, 0)

@dataclass
class YellowElement(Element):
    id: int = 4
    color: tuple = (255, 255, 0)

@dataclass
class PurpleElement(Element):
    id: int = 5
    color: tuple = (255, 0, 255)

preset = [RedElement(), BlueElement(), PurpleElement(), YellowElement(), GreenElement()]

# Todo: do in in the function
@dataclass
class Rule:
    x_len: int = 5
    y_len: int = 5

    @property
    def colors(self):
        return preset


@dataclass()
class Setto():
    color: Element
    length: int
    els: list


class Field:
    def __init__(self, id: int =None, rule: Rule = None):
        if id is None:
            import random
            self.id = random.randint(0, 10000)
        else:
            self.id = id

        if rule is None:
            self.rule = Rule()
        else:
            self.rule = rule()

        self.net = [[]]
        self.events = []
        self.score = 0

    def fill_init(self):
        from random import seed, choice
        seed(self.id, version=2)
        self.net = [[choice(self.rule.colors) for _y in range(self.rule.y_len)] for _x in range(self.rule.x_len)]
        self.events.append(events.Filled(self.id))
        return self.net

    def find_setto(self):
        list_of_setto = []

        for x in range(0, self.rule.x_len):
            for y in range(0, self.rule.y_len):
                if y == 0:
                    l = 1
                    old = self.net[x][y]
                elif old == self.net[x][y]:
                    l += 1
                    if y==(self.rule.y_len-1) and l >= 3:
                        list_of_setto.append(Setto(old, l, [(x, y - e) for e in range(l)]))
                        l = 1
                elif old != self.net[x][y] and l >= 3:
                    list_of_setto.append(Setto(old, l, [(x, y - 1 - e) for e in range(l)]))
                    l = 1
                    old = self.net[x][y]
                else:
                    l = 1
                    old = self.net[x][y]

        for y in range(self.rule.y_len):
            for x in range(self.rule.x_len):
                if x == 0:
                    l = 1
                    old = self.net[x][y]
                elif old == self.net[x][y]:
                    l += 1
                    if x == (self.rule.x_len - 1) and l >= 3:
                        list_of_setto.append(Setto(old, l, [(x - 1 - e, y) for e in range(l)]))
                        l = 1
                elif old != self.net[x][y] and l >= 3:
                    list_of_setto.append(Setto(old, l, [(x - 1 - e, y ) for e in range(l)]))
                    l = 1
                    old = self.net[x][y]
                else:
                    l = 1
                    old = self.net[x][y]
        return list_of_setto

    def kill_items(self, settos):
        score = 0
        for s in settos:
            for p in s.els:
                if self.net[p[0]][p[1]] is not None:
                    score += self.net[p[0]][p[1]].score_multiplicator
                    self.net[p[0]][p[1]]=None
        self.score += score
        if score>0:
            self.events.append(events.Killed(self.id, score=score, settos=settos))

    def swap(self, first, second):
        #TODO if not neighboors
        a = self.net[first[0]][first[1]]
        self.net[first[0]][first[1]] =  self.net[second[0]][second[1]]
        self.net[second[0]][second[1]] = a
        self.events.append(events.Swaped(self.id, l=first, r=second))

    def shift_to_nones(self):
        for x in range(self.rule.x_len):
            self.net[x] = list(filter(lambda x: x is not None, self.net[x]))
            self.net[x] += [None]*(self.rule.y_len - len(self.net[x]))
        self.events.append(events.Shifted(self.id))

    def fill_nones(self):
        from random import seed, choice
        # seed(self.id, version=2)

        for x in range(self.rule.x_len):
            for y in range(self.rule.y_len):
                if self.net[x][y] is None:
                    self.net[x][y] = choice(self.rule.colors)
        self.events.append(events.Filled(self.id))
