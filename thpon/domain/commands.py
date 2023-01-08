from datetime import date
from typing import Optional
from dataclasses import dataclass
from thpon.domain.model import Field


@dataclass()
class Command:
    fid: int

class FillInit(Command):
    pass

class Fill(Command):
    pass
class Switch(Command):
    pass
class Kill(Command):
    pass


