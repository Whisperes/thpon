# pylint: disable=attribute-defined-outside-init
from __future__ import annotations
import abc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from thpon import repository

class AbstractUnitOfWork(abc.ABC):
    fields: repository.AbstractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def collect_new_events(self):
        for fld in self.fields.seen:
            while fld.events:
                yield fld.events.pop(0)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class SimpleUnitOfWork(AbstractUnitOfWork):
    def __enter__(self):
        self.fields = repository.SimpleRepository()
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)

    def _commit(self):
        pass

    def rollback(self):
        pass



# DEFAULT_SESSION_FACTORY = sessionmaker(
#     bind=create_engine(
#         config.get_postgres_uri(),
#         isolation_level="REPEATABLE READ",
#     )
# )
#
#
# class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
#     def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
#         self.session_factory = session_factory
#
#     def __enter__(self):
#         self.session = self.session_factory()  # type: Session
#         self.products = repository.SqlAlchemyRepository(self.session)
#         return super().__enter__()
#
#     def __exit__(self, *args):
#         super().__exit__(*args)
#         self.session.close()
#
#     def _commit(self):
#         self.session.commit()
#
#     def rollback(self):
#         self.session.rollback()