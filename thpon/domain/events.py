from dataclasses import dataclass

@dataclass()
class Event:
    fid: int

@dataclass()
class Swaped(Event):
    fid: int
    l: tuple
    r: tuple

@dataclass()
class Killed(Event):
    score: int

@dataclass()
class Shifted(Event):
    pass

@dataclass()
class Filled(Event):
    pass

