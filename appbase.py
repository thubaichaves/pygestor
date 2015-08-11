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

class conecta:
    def __init__(self,_widgetpai,params=None):
        self._widgetpai=_widgetpai
        self.dados={}
        self.stepcallback = util.defaultv(params,'callback',None)
        for x in range(0,len(sys.argv)):
            if sys.argv[x] == '-db':
                if len(sys.argv)> x+1 and sys.argv[x+1] and conf.cfg_dburl_list.has_key(sys.argv[x+1]):
                    pyGestorModel.common.dbsession.configura_dburl(conf.cfg_dburl_list[sys.argv[x+1]],sys.argv[x+1])
                else:
                    raise "Configuração Inválida "+sys.argv[0]

        conecta.sstart = step = 0
        conecta.s_1 = step = step + 1
        conecta.sfim = step = step + 1
        self.step=conecta.sstart
        if not pyGestorModel.common.dbsession.sessionconfname:
            self.step_x(self.step)

    def callback(self, data=None):

        if self.step == conecta.sstart:
            (self.r, self.dados['confname'], z) = data

            if self.dados['confname']:
                if conf.cfg_dburl_list.has_key(self.dados['confname']):
                    pyGestorModel.common.dbsession.configura_dburl(
                        conf.cfg_dburl_list[self.dados['confname']],self.dados['confname'])
                else:
                    self.step_x(conecta.sstart)
                    return
            else:
                pyGestorModel.common.dbsession.configura_dburl(conf.cfg_dburl,'default')
            if self.stepcallback:
                self.stepcallback()

    def step_x(self, step=None, data=None):
        if step == conecta.sstart:
            nisk.dialogs.dlgInput.show('Conectar a qual servidor?', self._widgetpai, tocall=self.callback,
                                       isdialog=False)

consultor = pyGestorModel.lists_a_consultor()
nisk.widgets.wgtFieldBoxDb.defaultConsultor = consultor.consulta
nisk.widgets.wgtFieldBoxDb.defaultPopupSelector = defaultPopupSelector_