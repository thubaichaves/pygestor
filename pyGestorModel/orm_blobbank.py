from common import *
from sqlalchemy.orm import *


class blobbank(Base):
    __tablename__ = 'blobbank'
    id = Column(Integer, primary_key=True, autoincrement=False, server_default=FetchedValue())
    nome = Column(String(60))
    dados = Column(String())
    s_insdt = Column(DateTime)
    vers = Column(Integer)
    s_upddt = Column(DateTime)
    # s_len1 =  computed by (octet_length(dados)),

    __table_args__ = (
        UniqueConstraint('nome', name='blobname_uc'),
    )

