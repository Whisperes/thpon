from thpon.domain.model import *
from thpon.repository import *

def test_repository():
    f1 = Field()
    f2 = Field()

    fs = SimpleRepository()
    fs.add(f1)
    fs.add(f2)

    assert len(fs.seen)>0
    assert fs.get(f1.id).id==f1.id
    assert fs.get(f2.id).id==f2.id
    assert fs.get(f1.id).id!=f2.id