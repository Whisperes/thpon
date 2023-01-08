# pylint: disable=no-self-use
from __future__ import annotations
from collections import defaultdict
from datetime import date
from typing import Dict, List
import pytest
from thpon import bootstrap
from thpon.domain import commands
from thpon.service_layer import handlers
from thpon.service_layer import unit_of_work


def bootstrap_test_app():
    return bootstrap.bootstrap(
        start_orm=False, uow=unit_of_work.SimpleUnitOfWork()
    )


def test_for_new_field():
    bus = bootstrap_test_app()
    bus.handle(commands.FillInit(1))
    f = bus.uow.fields.get(1)
    assert f is not None
    assert f.score>3
    bus.handle(commands.Swap(1, (0, 7), (0, 8)))
    assert f is not None
    assert f.score > 6
