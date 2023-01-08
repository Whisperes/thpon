
class Event:
    pass
class Switched(Event):
    fid: str
    l: tuple
    r: tuple
class Killed(Event):
    fid: str
class Filleed(Event):
    fid: str

