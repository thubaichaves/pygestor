#!/usr/bin/python
# -*- coding: utf-8 -*-

from nisk import *
from nisk.actionKeys import ActionMap
import conf
import logging, sys
import nisk
import nisk.widgets
import pyGestorModel
import pyGestorModel.common
from pyGestorForms.frmListA import defaultPopupSelector_

# TODO
action_key_map = ActionMap(conf.keys)
#urwid.set_encoding("cp850")

pyGestorModel.common.dbsession.configura_dburl(conf.cfg_dburl)
for x in range(0,len(sys.argv)):
    if sys.argv[x] == '-db':
        if len(sys.argv)> x+1 and sys.argv[x+1] and conf.cfg_dburl_list.has_key(sys.argv[x+1]):
            pyGestorModel.common.dbsession.configura_dburl(conf.cfg_dburl_list[sys.argv[x+1]])
        else:
            raise "Configuração Inválida "+sys.argv[0]

consultor = pyGestorModel.lists_a_consultor()
nisk.widgets.wgtFieldBoxDb.defaultConsultor = consultor.consulta
nisk.widgets.wgtFieldBoxDb.defaultPopupSelector = defaultPopupSelector_