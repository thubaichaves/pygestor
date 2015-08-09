import fdb
#
from conf import *
#
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
import logging
import nisk
import puremvc.patterns.mediator

Base = declarative_base()


class dbsession:
    smaker = None


    def __init__(self):
        pass

    @staticmethod
    def initonce():
        if dbsession.smaker is None:
            dbsession.engine = create_engine(dbsession._dburl, echo=False)
            dbsession.smaker = sessionmaker(bind=dbsession.engine)
            dbsession.smaker.configure(bind=dbsession.engine)
            # session = SessionMkr()

    @staticmethod
    def configura_dburl(urlx):
        if dbsession.smaker is None:
            dbsession._dburl = urlx

    @staticmethod
    def getsession():
        if dbsession.smaker is None:
            dbsession.initonce()
        return dbsession.smaker()


class consultor:
    id = 0
    nome = 1
    tid = 2

    def __init__(self):
        self.consultor = None

    def updateItem(self, dados=None):
        try:
            self.consultor.commit()
        except Exception, e:
            logging.exception(e)

    def revertItem(self, dados=None):
        try:
            self.consultor.rollback()
        except Exception, e:
            logging.exception(e)

class mediator_base(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator, nisk.formmer.binder):

    def __init__(self, f, proxy, nome):
        super(mediator_base, self).__init__(nome, viewComponent=None)
        nisk.formmer.binder.__init__(self, f.widgets, f.fields)
        #
        self.consultor = proxy

    def listNotificationInterests(self):
        return []

    def handleNotification(self, note):
        pass

    def handleCommand(self, cmd, par=None):
        if cmd == 'salvar':
            self.update()
            return

    def consulta(self, params={}):
        if params.has_key('new') and params.has_key('dados'):
            r = self.consultor.getNovo(params, params['dados'])
            if not r is None:
                self.load(r)
                return True

        else:
            r = self.consultor.getItem(params)
            if not r is None:
                self.load(r)
                return True

        return False


    def update(self):
        nisk.formmer.binder.update(self)
        self.consultor.updateItem(self._dados)
        self.load(self._dados, isreload=True)
        self.set_isdirty(False)

    def abort(self):
        nisk.formmer.binder.abort(self)



    def onAdd(self, evt):
        pass


    def onUpdate(self, evt):
        pass


    def onCancel(self, evt):
        pass