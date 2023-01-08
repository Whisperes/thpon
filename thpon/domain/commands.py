from datetime import date
from typing import Optional
from dataclasses import dataclass
from thpon.domain.model import Field


@dataclass()
class Command:
    fid: int

@dataclass()
class FillInit(Command):
    pass

@dataclass()
class Fill(Command):
    pass
@dataclass()
class Swap(Command):
    first: tuple
    second: tuple

@dataclass()
class Kill(Command):
    pass


