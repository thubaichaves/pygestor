from sqlalchemy.orm import *
from orm_contatos import *


class os_os(Base):
    __tablename__ = 'os_os'

    id = Column(Integer, primary_key=True, autoincrement=False, server_default=FetchedValue())
    os = Column(Integer)
    exc = Column(Integer)
    #
    cliente = Column(Integer, ForeignKey('contatos.id'))
    marca = Column(Integer, ForeignKey('lists_a.tid'))
    tipo = Column(Integer, ForeignKey('lists_a.tid'))
    usrent = Column(Integer, ForeignKey('lists_a.tid'))
    usrresp = Column(Integer, ForeignKey('lists_a.tid'))
    usrsai = Column(Integer, ForeignKey('lists_a.tid'))
    status = Column(Integer, ForeignKey('lists_a.tid'))
    ntarefa = Column(Integer, ForeignKey('lists_a.tid'))
    quite = Column(Integer, ForeignKey('lists_a.tid'))
    edt = Column(Integer)
    #
    ativo = Column(Numeric)
    #
    acess = Column(String(250))
    conserva = Column(String(60))
    diag = Column(String(250))
    estsai = Column(String(60))
    garantia = Column(String(60))
    lembrete = Column(String(60))
    modelo = Column(String(20))
    nf = Column(String(20))
    nome = Column(String(60))
    sintoma = Column(String(250))
    solicita = Column(String(250))
    obsint = Column(String(250))
    obsos = Column(String(250))
    obssai = Column(String(250))
    orc = Column(String(250))
    portent = Column(String(60))
    portsai = Column(String(60))
    prazoexe = Column(String(20))
    prazoorc = Column(String(20))
    ns = Column(String(20))
    #
    dataent = Column(DateTime,server_default=FetchedValue())
    dataok = Column(DateTime)
    datasai = Column(DateTime)
    dta = Column(DateTime)
    dtb = Column(DateTime)
    dtc = Column(DateTime)
    dte = Column(DateTime)
    dtf = Column(DateTime)
    #
    oscliente = relationship("contatos")
    ostipo = relationship("lists_a", primaryjoin="and_(lists_a.tab=='ostip',os_os.tipo==lists_a.tid)",
                          backref='ostipox')
    osmarca = relationship("lists_a", primaryjoin="and_(lists_a.tab=='osfab',os_os.marca==lists_a.tid)",
                           backref='osmarcax')
    osusrent = relationship("lists_a", primaryjoin="and_(lists_a.tab=='sysus',os_os.usrent==lists_a.tid)",
                            backref='osusrentx')
    osusrresp = relationship("lists_a", primaryjoin="and_(lists_a.tab=='sysus',os_os.usrresp==lists_a.tid)",
                             backref='osusrrespx')
    osusrsai = relationship("lists_a", primaryjoin="and_(lists_a.tab=='sysus',os_os.usrsai==lists_a.tid)",
                            backref='osusrsaix')
    osstatus = relationship("lists_a", primaryjoin="and_(lists_a.tab=='osstt',os_os.status==lists_a.tid)",
                            backref='osstatusx')
    osntarefa = relationship("lists_a", primaryjoin="and_(lists_a.tab=='osnxt',os_os.ntarefa==lists_a.tid)",
                             backref='osntarefax')
    #
    # lst_lista1 = (
    # 'os',
    # 'cliente',
    # 'solicita',
    # 'dataent',
    #     'datasai',
    #     'tipo',
    #     'marca'
    # )

    # infopag = Column(String(60))
    # inta = Column(Integer)
    # intb = Column(Integer)
    # intc = Column(Integer)
    # intd = Column(Integer)
    inte = Column(Integer,server_default="0")
    # intf = Column(Integer)
    # intg = Column(Integer)
    # inth = Column(Integer)
    # inti = Column(Integer)
    # intj = Column(Integer)
    # intk = Column(Integer)
    # intl = Column(Integer)
    # intm = Column(Integer)
    # intn = Column(Integer)
    # rgs = Column(Integer)
    # s_bd = Column(Integer)
    # s_dirty = Column(Integer)
    # s_excdt = Column(DateTime)
    # s_excloc = Column(Integer)
    # s_excusr = Column(Integer)
    # s_free = Column(Integer)
    # s_insdt = Column(DateTime)
    # s_insloc = Column(Integer)
    # s_insusr = Column(Integer)
    # s_loc = Column(Integer)
    # s_upddt = Column(DateTime)
    # s_updloc = Column(Integer)
    # s_updusr = Column(Integer)
    # s_ver = Column(Integer)
    # t1a = Column(String(20))
    # t1b = Column(String(20))
    # t1c = Column(String(20))
    # t1d = Column(String(20))
    # t2a = Column(String(40))
    # t2b = Column(String(40))
    # t2c = Column(String(40))
    # t2d = Column(String(40))
    # t3a = Column(String(60))
    # t3b = Column(String(60))
    # t3c = Column(String(60))
    # t3d = Column(String(60))
    # t4a = Column(String(80))
    # t4b = Column(String(80))
    # t4c = Column(String(80))
    # t4d = Column(String(80))
    # t5a = Column(String(250))
    # t5b = Column(String(250))
    # vala = Column(Numeric)
    # valb = Column(Numeric)
    # valc = Column(Numeric)
    # vald = Column(Numeric)










