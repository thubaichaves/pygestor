from common import *
from sqlalchemy.orm import *


class lists_a(Base):
    __tablename__ = 'lists_a'
    id = Column(Integer, primary_key=True, autoincrement=False, server_default=FetchedValue())
    tid = Column(Integer, server_default=FetchedValue())
    nome = Column(String(60))
    tab = Column(String(10))
    #
    exc = Column(Integer)
    i1 = Column(Integer)
    i2 = Column(Integer)
    i3 = Column(Integer)
    t1a = Column(String(20))
    t1b = Column(String(20))
    t3a = Column(String(60))
    t3b = Column(String(60))
    descr = Column(String(80))
    n1 = Column(Numeric)
    n2 = Column(Numeric)
    n3 = Column(Numeric)
    n4 = Column(Numeric)
    n5 = Column(Numeric)

    __table_args__ = (
        UniqueConstraint('tab', 'tid', name='tidtab_uc'),
    )


class grupos(Base):
    __tablename__ = 'grupos'

    id = Column(Integer, primary_key=True, autoincrement=False, server_default=FetchedValue())
    tid = Column(Integer, server_default=FetchedValue())
    nome = Column(String(60))
    tab = Column(String(10))
    pai = Column(Integer)
    nivel = Column(Integer)
    #
    exc = Column(Integer)
    i1 = Column(Integer)
    i2 = Column(Integer)
    n1 = Column(Numeric)
    n2 = Column(Numeric)
    n3 = Column(Numeric)
    n4 = Column(Numeric)
    n5 = Column(Numeric)
    descr = Column(String(80))
    t1a = Column(String(20))
    t1b = Column(String(20))
    t3a = Column(String(60))
    t3b = Column(String(60))
    #
    __table_args__ = (
        UniqueConstraint('tab', 'tid', name='tidtab_uc'),
    )