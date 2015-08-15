#!/usr/bin/python
# -*- coding: utf-8 -*-

import puremvc.patterns.proxy
import vo
from pyGestorForms import enum
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import DeclarativeMeta
import nisk
import nisk.TUI
import nisk.util
from nisk.util import timed
import json
import logging
import common
from conf import *
#
import orm_os
import orm_listas
import orm_contatos


class OS_Proxy(puremvc.patterns.proxy.Proxy, common.consultor):
    NAME = "OS_Proxy"

    def __init__(self):
        super(OS_Proxy, self).__init__(OS_Proxy.NAME, [])
        self.consultor = common.dbsession.getsession()

    def getItems(self, params):
        return self.data

    def getItem(self, params):
        if params.has_key('os'):
            osn = nisk.util.defaultv(params, 'os', None)
            if not osn is None:
                conts = self.consultor.query(orm_os.os_os)
                sos = conts.filter(orm_os.os_os.os == osn).first()
                return sos
        if params.has_key('id'):
            osn = nisk.util.defaultv(params, 'id', None)
            if not osn is None:
                conts = self.consultor.query(orm_os.os_os)
                sos = conts.filter(orm_os.os_os.id == osn).first()
                return sos

        return None

    def getNovo(self, params, dados):
        x = orm_os.os_os()
        x.inte = 1

        self.consultor.add(x)
        self.consultor.commit()
        self.consultor.flush()
        # nisk.util.dump(x.os)
        # nisk.util.dump(x.id)]
        x = self.getItem({'id': x.id})

        x.marca = dados['marca']['tid']
        x.cliente = dados['cliente']['tid']
        x.tipo = dados['tipo']['tid']
        x.usrresp = dados['marca']['tid']

        self.consultor.commit()
        self.consultor.refresh(x)
        # nisk.util.dump([x, x.id, x.inte], 'after')

        return x

    def deleteItem(self, user):
        pass


class contatos_Proxy(puremvc.patterns.proxy.Proxy, common.consultor):
    NAME = "contatos_Proxy"

    def __init__(self):
        super(contatos_Proxy, self).__init__(contatos_Proxy.NAME, [])
        self.consultor = common.dbsession.getsession()

    def getItems(self, params):
        return self.data

    def getItem(self, params):
        if params.has_key('id'):
            osn = nisk.util.defaultv(params, 'id', None)
            if not osn is None:
                conts = self.consultor.query(orm_contatos.contatos)
                sos = conts.filter(orm_contatos.contatos.id == osn).first()
                return sos

        return None

    def getNovo(self, params, dados):
        x = orm_contatos.contatos()
        x.alias = nisk.util.defaultv(dados, 'nome', '')
        self.consultor.add(x)

        # self.consultor.commit()

        telefones = nisk.util.defaultv(dados, 'telefones', [])
        for t in telefones:
            tx = orm_contatos.cont_num()
            tx.cont_num_contatos = x
            # tx.pai = x.id
            tx.nome = t
            self.consultor.add(tx)
        self.consultor.commit()

        return x

    def deleteItem(self, user):
        pass


class listas_Proxy(puremvc.patterns.proxy.Proxy, common.consultor):
    NAME = "listas_Proxy"

    def __init__(self, rtab_orm, ltab):
        self.rtab_orm = rtab_orm
        self.ltab = ltab
        # self.logictable = logictable
        super(listas_Proxy, self).__init__(listas_Proxy.NAME, [])
        self.consultor = common.dbsession.getsession()

    def getItems(self, params):
        return self.data

    def getItem(self, params):
        if params.has_key('id') and params.has_key('ltab'):
            osn = nisk.util.defaultv(params, 'id', None)

            ltab = nisk.util.defaultv(params, 'ltab', None)
            if osn and ltab:
                conts = self.consultor.query(self.rtab_orm)
                sos = conts.filter(self.rtab_orm.tid == osn).filter(self.rtab_orm.tab == ltab).first()
                return sos

        return None

    def getNovo(self, params, dados):
        x = self.rtab_orm()
        x.nome = dados['nome']
        ltab = nisk.util.defaultv(params, 'ltab', nisk.util.defaultv(dados, 'ltab', ''))
        if not ltab:
            raise 'erro de parametro ltab'
        x.tab = ltab
        self.consultor.add(x)

        self.consultor.commit()

        return x

    def deleteItem(self, user):
        pass


class DB_Procedures(puremvc.patterns.proxy.Proxy):
    def __init__(self):
        super(OS_Proxy, self).__init__(OS_Proxy.NAME, [])
        self.consultor = common.dbsession.getsession()

    @staticmethod
    def sproc_autenticalogin(dados):
        try:
            _oracle = common.dbsession.getsession()
            _rec = _oracle.query(orm_listas.lists_a).filter(
                orm_listas.lists_a.tid == dados['user'],
                orm_listas.lists_a.tab == 'sysus').first()

            return dados['pass'] == _rec.t1b
        except:
            pass
        return False


class UserProxy(puremvc.patterns.proxy.Proxy):
    NAME = "UserProxy"

    def __init__(self):
        super(UserProxy, self).__init__(UserProxy.NAME, [])
        self.data = []
        del self.data[:]
        self.getList()
        # self.addItem(vo.UserVO('lstooge','Larry', 'Stooge', "larry@stooges.com", 'ijk456',enum.DEPT_ACCT))
        # self.addItem(vo.UserVO('cstooge','Curly', 'Stooge', "curly@stooges.com", 'xyz987',enum.DEPT_SALES))
        # self.addItem(vo.UserVO('mstooge','Moe', 'Stooge', "moe@stooges.com", 'abc123',enum.DEPT_PLANT))

    def getUsers(self):
        return self.data

    def getList(self):
        # cur = pyGestorModel.fastConnection().cursor()
        # cur.execute("SELECT nome,alias, t4a, id,nome as nome2 from contatos order by nome asc rows 10")
        #
        # for (nome,alias, t4a, id,nome2) in cur:
        # self.addItem(vo.UserVO(nome,alias, t4a, id,nome2,enum.DEPT_ACCT))
        engine = create_engine("firebird+fdb://sysdba:masterkey@localhost:3050/c:\\teste.fdb?charset=WIN1252")

        result = engine.execute("SELECT nome,alias, t4a, id,nome as nome2 from contatos order by nome asc rows 10")
        for row in result:
            self.addItem(vo.UserVO(row['nome'], row['alias'], row['t4a'], row['id'], row['nome2'], enum.DEPT_ACCT))

        # engine.close()
        return self.data
        pass

    def addItem(self, item):
        self.data.append(item)

    def updateItem(self, user):
        for i in range(0, len(self.data)):
            if self.data[i].username == user.username:
                self.data[i] = user

    def deleteItem(self, user):
        for i in range(0, len(self.data)):
            if self.data[i].username == user.username:
                del self.data[i]


class userAuthProvider(nisk.TUI.nestedwidget):
    def __init__(self, _widgetpai):
        self._lastuserID = None
        self._lastuserName = None
        self._userID = None
        self._userName = None
        self._logouttime = 30
        self._remaintime = self._logouttime

        nisk.TUI.nestedwidget.__init__(self)

    def sproc_autenticalogin(self, dados):
        try:
            _oracle = common.dbsession.getsession()
            _rec = _oracle.query(orm_listas.lists_a).filter(
                orm_listas.lists_a.tid == dados['user'],
                orm_listas.lists_a.tab == 'sysus').first()

            if dados['pass'] == _rec.t1b:
                self._userID = _rec.tid
                self._userName = _rec.nome

                return True
        except:
            pass
        return False


class RoleProxy(puremvc.patterns.proxy.Proxy):
    NAME = "RoleProxy"

    def __init__(self):
        super(RoleProxy, self).__init__(RoleProxy.NAME, [])
        self.data = []
        self.addItem(vo.RoleVO('lstooge', [enum.ROLE_PAYROLL, enum.ROLE_EMP_BENEFITS]))
        self.addItem(vo.RoleVO('cstooge', [enum.ROLE_ACCT_PAY, enum.ROLE_ACCT_RCV, enum.ROLE_GEN_LEDGER]))
        self.addItem(
            vo.RoleVO('mstooge', [enum.ROLE_INVENTORY, enum.ROLE_PRODUCTION, enum.ROLE_SALES, enum.ROLE_SHIPPING]))

    def getRoles(self):
        print self.data
        return self.data

    def addItem(self, item):
        self.data.append(item)

    def deleteItem(self, item):
        for i in range(len(self.data)):
            if self.data[i].username == item.username:
                del self.data[i]
                break

    def doesUserHaveRole(self, user, role):
        hasRole = False;
        for i in range(len(self.data)):
            if self.data[i].username == user.username:
                userRoles = self.data[i].roles
                for j in range(len(userRoles)):
                    if userRoles[j] == role:
                        hasRole = True
                        break
        return hasRole

    def addRoleToUser(self, user, role):
        result = False;
        if not self.doesUserHaveRole(user, role):
            for i in range(0, len(self.data)):
                if self.data[i].username == user.username:
                    userRoles = self.data[i].roles
                    userRoles.append(role)
                    result = True;
                    break
        self.sendNotification(main.AppFacade.ADD_ROLE_RESULT, result)

    def removeRoleFromUser(self, user, role):
        if self.doesUserHaveRole(user, role):
            for i in range(0, len(self.data)):
                if self.data[i].username == user.username:
                    userRoles = self.data[i].roles
                    for j in range(0, len(userRoles)):
                        if userRoles[j] == role:
                            del userRoles[i]
                            break

    def getUserRoles(self, username):
        userRoles = []
        for i in range(0, len(self.data)):
            if self.data[i].username == username:
                userRoles = self.data[i].roles
                break
        return userRoles


class paraserializar:
    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # an SQLAlchemy class
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                    data = obj.__getattribute__(field)
                    try:
                        json.dumps(data)  # this will fail on non-encodable values, like other classes
                        fields[field] = data
                    except TypeError:
                        fields[field] = None
                # a json-encodable dict
                return fields

            return json.JSONEncoder.default(self, obj)

    from collections import OrderedDict

    class DictSerializable(object):
        def _asdict(self):
            result = OrderedDict()
            for key in self.__mapper__.c.keys():
                result[key] = getattr(self, key)
            return result

    from json import dumps

    def to_json(model):
        """ Returns a JSON representation of an SQLAlchemy-backed object.
        """
        json = {}
        json['fields'] = {}
        json['pk'] = getattr(model, 'id')

        for col in model._sa_class_manager.mapper.mapped_table.columns:
            json['fields'][col.name] = getattr(model, col.name)

        return dumps([json])


class tipo_listaorm:
    classico = 0
    multiplo = 1


listas_orm = {
    'lists_a': (orm_listas.lists_a, tipo_listaorm.multiplo),
    'grupos': (orm_listas.grupos, tipo_listaorm.multiplo),
    'contatos': (orm_contatos.contatos, tipo_listaorm.classico)
}


class lists_a_consultor(common.consultor):
    # @staticmethod
    @timed
    def consulta(self, tid, tab='', ltab=''):
        session = common.dbsession.getsession()
        #
        ''''
        def my_import(name):
            mod = __import__(name)
            components = name.split('.')
            for comp in components[1:]:
                mod = getattr(mod, comp)
            return mod
        #'''''

        if len(tab) < 1:
            tab = 'lists_a'

        tabxs, tipo = listas_orm[tab]

        if tipo == tipo_listaorm.multiplo:

            conts = session.query(tabxs).filter(
                tabxs.tid == tid, tabxs.tab == ltab
            ).first()

            # nisk.util.dump(conts)

            if conts is None:
                return None
            else:
                return [
                    conts.tid,
                    conts.nome,
                    conts.id
                ]

        elif tipo == tipo_listaorm.classico:
            session = common.dbsession.getsession()

            conts = session.query(tabxs).filter(
                tabxs.id == tid
            ).first()

            if conts is None:
                return None
            else:
                return [
                    conts.id,
                    conts.nome,
                    conts.id
                ]


class contatos_consultor(lists_a_consultor):
    nono = None
