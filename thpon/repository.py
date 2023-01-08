import abc
from typing import Set
from thpon.domain import model

class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, field: model.Field):
        self._add(field)
        self.seen.add(field)

    def get(self, fid) -> model.Field:
        field = self._get(fid)
        if field:
            self.seen.add(field)
        return field

    # def get_by_batchref(self, batchref) -> model.Field:
    #     product = self._get_by_batchref(batchref)
    #     if product:
    #         self.seen.add(product)
    #     return product

    @abc.abstractmethod
    def _add(self, product: model.Field):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sku) -> model.Field:
        raise NotImplementedError

    # @abc.abstractmethod
    # def _get_by_batchref(self, batchref) -> model.Field:
    #     raise NotImplementedError

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class SimpleRepository(AbstractRepository):
    def __init__(self):
        super().__init__()

    def _add(self, product):
        pass

    def _get(self, fid):
        try:
            return next(filter(lambda x: x.id == fid, self.seen))
        except StopIteration:
            return None

class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, product):
        self.session.add(product)

    def _get(self, fid):
        return self.session.query(model.Field).filter_by(fid=fid).first()

    def _get_by_batchref(self, batchref):
        return (
            self.session.query(model.Field)
            .join(model.Field)
            .filter(
                orm.batches.c.reference == batchref,
            )
            .first()
        )