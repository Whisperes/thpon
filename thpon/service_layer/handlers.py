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


EVENT_HANDLERS = {

}  # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    commands.FillInit: fill_init,
}  # type: Dict[Type[commands.Command], Callable]