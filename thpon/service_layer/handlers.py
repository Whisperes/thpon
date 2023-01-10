# pylint: disable=unused-argument
from __future__ import annotations
from dataclasses import asdict
from typing import List, Dict, Callable, Type, TYPE_CHECKING
from thpon.domain import commands, events, model
from thpon.domain.model import Field

if TYPE_CHECKING:
    from . import unit_of_work

def fill_init(cmd: commands.FillInit,
              uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        field = uow.fields.get(fid=cmd.fid)
        if field is None:
            field = model.Field(id=cmd.fid)
            uow.fields.add(field)

        field.fill_init()
        uow.commit()
    return field

def fill_kill(event: events.Killed,
              uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        field = uow.fields.get(fid=event.fid)
        if field is None:
            raise 'No any field'

        settos = field.find_setto()
        field.kill_items(settos)
        uow.commit()


def shift(event: events.Killed,
              uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        field = uow.fields.get(fid=event.fid)
        if field is None:
            raise 'No any field'

        field.shift_to_nones()
        uow.commit()

def fill(event: events.Filled,
              uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        field = uow.fields.get(fid=event.fid)
        if field is None:
            raise 'No any field'

        field.fill_nones()
        uow.commit()

def swap(cmd: commands.Swap,
              uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        field = uow.fields.get(fid=cmd.fid)
        if field is None:
            raise 'No any field'

        field.swap(first=cmd.first, second=cmd.second)
        uow.commit()

EVENT_HANDLERS = {
    events.Killed: [shift],
    events.Shifted: [fill],
    events.Filled: [fill_kill],
    events.Swaped: [fill_kill]
}  # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    commands.FillInit: fill_init,
    commands.Swap: swap,
}  # type: Dict[Type[commands.Command], Callable]