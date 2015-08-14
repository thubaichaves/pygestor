#!/usr/bin/python
# -- coding: utf-8 --

from pyGestorModel import *
from pyGestorModel.orm_os import *
from pyGestorModel.orm_blobbank import *

from escposx import *
from escposx.constants import *

import nisk.util as util
import nisk.widgets
import datetime
from nisk.util import asstr
# import MiniFrame


def consultaOS(osn):
    session = dbsession.getsession()

    va = session.query(os_os).filter(
        orm_os.os_os.os == osn,
    ).options(
        joinedload(os_os.osmarca).load_only("nome"),
        joinedload(os_os.ostipo).load_only("nome"),
        joinedload(os_os.oscliente).load_only("nome", 't4a')
    )

    vx = va.first()

    return vx


def getBlob(fn):
    s = dbsession.getsession()
    q = s.query(blobbank).filter(blobbank.nome == fn)
    f = q.first()
    if f:
        return f.dados
    return ''

def win():
    m = MiniFrame.WxApp()
    m.MainLoop()
    # m.ExitMainLoop()
    wins.append( m)

wins = []

class imprimir_OS:
    @staticmethod
    def imprimir_OS(params):


        modelo = nisk.util.defaultv(params, 'modelo', None)

        if modelo == 'entrada':
            imprimir_OS.imprimir_OS_entrada(params)
        if modelo == 'etiq':
            imprimir_OS.imprimir_OS_etiq(params)
        if modelo == 'etiqa':
            imprimir_OS.imprimir_OS_etiqa(params)
        if modelo == 'fichaanalise':
            imprimir_OS.imprimir_OS_fichaanalise(params)
        if modelo == 'fichaqc':
            imprimir_OS.imprimir_OS_fichaqc(params)
        if modelo == 'orc':
            imprimir_OS.imprimir_OS_orc(params)
        if modelo == 'saida':
            imprimir_OS.imprimir_OS_saida(params)

    @staticmethod
    def imprimir_OS_entrada(params):
        osn = nisk.util.defaultv(params, 'os', None)
        sos = consultaOS(osn)

        if not sos: return

        var_prnfile = util.getprintfilename()
        prn = printer.File(devfile=var_prnfile)

        prn.set(codepage=cfg_codepage)

        v_cabec = getBlob('cabecalho')
        prn.text(v_cabec, 1)

        prn.pulal()

        prn.textline(
            '{CondensedOn}' + str(datetime.datetime.now()) + '/usr:%s' % sos.usrent + '{CondensedOff}', 1)  # Datetime

        prn.set(bold=1, size='2x', align='center')
        prn.textline("--------------------")
        prn.textline(" ENTRADA OS %s " % sos.os)
        prn.textline("--------------------")
        prn.set(bold=0, size='normal', align='left')

        if sos.dataent:
            prn.textline("Entrada em:" + CTL_HT + " %s " % '{:%d-%m-%Y %H:%M}'.format(sos.dataent))

        prn.textline("Cliente:\t %s " % sos.oscliente.nome if sos.oscliente else '')
        prn.textline("Telefones:\t  %s " % sos.oscliente.t4a if sos.oscliente else '')
        prn.pulal()

        prn.textline("Aparelho:\t %s " % sos.ostipo.nome if sos.ostipo else '')

        prn.textline("Marca:\t  %s " % sos.osmarca.nome if sos.osmarca else '')

        prn.textline("N° Serial:\t  %s " % str(sos.modelo))

        prn.textline("N° Modelo:\t  %s " % str(sos.ns))

        if util.slen(sos.nf) > 0:
            prn.textline("NF:\t  %s " % asstr(str(sos.nf)))

        prn.textline(u"Solicitação:\t  %s " % asstr(sos.solicita))

        prn.textline(u"Acessorios:\t  %s " % asstr(sos.acess))

        prn.textline(u"Estado de Conservação:\t  %s " % asstr(sos.conserva))

        prn.textline(u"Prazo de Orçamento:\t  %s " % asstr(sos.prazoorc))

        prn.textline(u"Lembrete:\t  %s " % asstr(sos.lembrete))

        prn.textline(u"Observações:  %s " % asstr(sos.obsos))

        prn.text(getBlob('termoentradaos'), 1)
        prn.text(getBlob('rodape'), 1)

        # prn.pulal(10)
        prn.textline("____________________\n\r\n\r")
        prn.cut()

        prn.close()

        util.imprimeLPR(cfg_prntxt, var_prnfile)

    @staticmethod
    def imprimir_OS_etiq(params):

        # util.paralelo(win)

        osn = nisk.util.defaultv(params, 'os', None)
        sos = consultaOS(osn)

        if not sos: return

        var_prnfile = util.getprintfilename()
        prn = printer.File(devfile=var_prnfile)

        prn._codepage =  cfg_codepage

        v_cabec = getBlob('etiqos01')
        v_cabec = v_cabec.replace("<##OS##>", util.astext([(sos, 'os')]))

        v_cabec = v_cabec.replace("<##L1##>", util.astext([(sos, 'oscliente', 'nome'), '.'], 27))
        v_cabec = v_cabec.replace("<##L2##>", util.astext([(sos, 'oscliente', 't4a'), '.'], 27))

        v_cabec = v_cabec.replace("<##L3##>", util.astext([(sos, 'ostipo', 'nome'), ' - '], 15) + \
                                  util.astext([(sos, 'osmarca', 'nome'), ' - '], 15))

        v_cabec = v_cabec.replace("<##L4##>", util.astext([(sos, 'modelo'), ' - '], 15) + \
                                  util.astext([(sos, 'ns'), ' - '], 15))

        v_cabec = v_cabec.replace("<##L5##>", "Entrada: " + util.astext([(sos, 'dataent'), ' - '], 15))

        v_cabec = v_cabec.replace("<##L6##>", '')

        v_cabec = v_cabec.replace("<##L7##>", '')

        v_cabec = v_cabec.replace("<##C##>", util.astext(util.defaultv(params, 'qtd', 1)))

        v_cabec = v_cabec.replace("<##", '').replace("##>", '')

        prn.text(v_cabec+'\n', 1)
        prn.close(reset=0)

        util.imprimeLPR(cfg_prnetq, var_prnfile)

    @staticmethod
    def imprimir_OS_etiqa(params):
        '''
                   var printer =
                new Matrixer(Settings.Default.impetq);
            printer.StartJob();

            string s = u.CoalesceS(LocalConf.GetBlobBank(p["_pattern"] as string));

            printer.Replace(ref s, "<##OS##>", u.RecStr(p["OS"]));
            printer.Replace(ref s, "<##E##>", u.RecStr(p["OS"]));
            printer.Replace(ref s, "<##L1##>", u.limit(u.CoalesceS(p["T3XD"]), 27));
            printer.Replace(ref s, "<##L2##>", u.limit(u.CoalesceS(p["T4D"]), 27));
            printer.Replace(ref s, "<##L3##>",
                            u.CoalesceS(p["T1XC"]) + " _ " + u.CoalesceS(p["T1XD"]));
            printer.Replace(ref s, "<##L4##>",
                            u.CoalesceS(p["MODELO"] as String) +
                            ((!string.IsNullOrEmpty(p["NS"] as String)) ? (" _ NS: " + p["NS"]) : ""));
            printer.Replace(ref s, "<##L5##>",
                            "Entrada: " +
                            (p["DATAENT"] is DateTime
                                 ? ((DateTime) p["DATAENT"]).ToString("dd/MM/yyyy HH:mm")
                                 : ""));

            printer.Replace(ref s, "<##L7##>",
                            u.limit(
                                u.CoalesceS(p["SINTOMA"]) + " " + u.CoalesceS(p["SOLICITA"]),
                                27));

            var cx = p["_copias"] as int?;
            cx = cx.HasValue ? cx : 0;
            printer.Replace(ref s, "<##C##>", cx.Value.ToString());

            printer.InternalText = s;
            printer.CleanText("<##", "##>");
            printer.PrintJob();
        :param params:
        :return:
        '''
        pass

    @staticmethod
    def imprimir_OS_fichaanalise(params):
        osn = nisk.util.defaultv(params, 'os', None)
        sos = consultaOS(osn)
        if not sos: return
        var_prnfile = util.getprintfilename()
        prn = printer.File(devfile=var_prnfile)
        prn.set(codepage=cfg_codepage)

        prn.textline(
            '{CondensedOn}' + str(datetime.datetime.now()) + '/usr:%s' % sos.usrent + '{CondensedOff}', 1)  # Datetime

        prn.set(bold=1, size='2x', align='center')
        prn.textline("--------------------")
        prn.textline(" FICHA DE PRÉ-ANÀLISE\n OS %s " % sos.os)
        prn.textline("--------------------")
        prn.set(bold=0, size='normal', align='left')

        prn.textline("Padrão de Verificação: Notebook")
        prn.pulal()

        prn.textline(" # Equipamento Liga ?")
        # prn.pulal()
        prn.textline("  (  ) Sim   (  ) Não (________________________)")

        prn.textline(" # Teclado Funciona ?")
        # prn.pulal()
        prn.textline("  (  ) Sim   (  ) Não (________________________)")

        prn.textline(" # Situação da Fonte de Alimentação ?")
        # prn.pulal()
        prn.textline("  (  ) Sim   (  ) Não (________________________)")

        prn.pulal()

        # prn.pulal(10)
        prn.textline("____________________\n\r\n\r")
        prn.cut()

        prn.close()

        util.imprimeLPR(cfg_prntxt, var_prnfile)

    @staticmethod
    def imprimir_OS_fichaqc(params):
        osn = nisk.util.defaultv(params, 'os', None)
        sos = consultaOS(osn)

        if not sos: return

        var_prnfile = util.getprintfilename()
        prn = printer.File(devfile=var_prnfile)

        prn.set(codepage=cfg_codepage)

        v_cabec = getBlob('cabecalho')
        prn.text(v_cabec, 1)

        prn.pulal()

        prn.textline(
            '{CondensedOn}' + str(datetime.datetime.now()) + '/usr:%s' % sos.usrent + '{CondensedOff}', 1)  # Datetime

        prn.set(bold=1, size='2x', align='center')
        prn.textline("--------------------")
        prn.textline(" CONTROLE DE QUALIDADE\n OS %s " % sos.os)
        prn.textline("--------------------")
        prn.set(bold=0, size='normal', align='left')

        if sos.dataent:
            prn.textline("Entrada em:" + CTL_HT + " %s " % '{:%d-%m-%Y %H:%M}'.format(sos.dataent))

        prn.textline("Cliente:\t %s " % sos.oscliente.nome if sos.oscliente else '')
        prn.textline("Telefones:\t  %s " % sos.oscliente.t4a if sos.oscliente else '')
        prn.pulal()

        prn.textline("Aparelho:\t %s " % sos.ostipo.nome if sos.ostipo else '')

        prn.textline("Marca:\t  %s " % sos.osmarca.nome if sos.osmarca else '')

        prn.textline("N° Serial:\t  %s " % str(sos.modelo))

        prn.textline("N° Serial:\t  %s " % str(sos.ns))

        if util.slen(sos.nf) > 0:
            prn.textline("NF:\t  %s " % asstr(str(sos.nf)))

        prn.textline(u"Solicitação:\t  %s " % asstr(sos.solicita))

        prn.textline(u"Acessorios:\t  %s " % asstr(sos.acess))

        prn.textline(u"Estado de Conservação:\t  %s " % asstr(sos.conserva))

        prn.textline(u"Prazo de Orçamento:\t  %s " % asstr(sos.prazoorc))

        prn.textline(u"Lembrete:\t  %s " % asstr(sos.lembrete))

        prn.textline(u"Observações:  %s " % asstr(sos.obsos))

        prn.text(getBlob('termoentradaos'), 1)
        prn.text(getBlob('rodape'), 1)

        # prn.pulal(10)
        prn.textline("____________________\n\r\n\r")
        prn.cut()

        prn.close()

        util.imprimeLPR(cfg_prntxt, var_prnfile)

    @staticmethod
    def imprimir_OS_orc(params):
        osn = nisk.util.defaultv(params, 'os', None)
        sos = consultaOS(osn)

        if not sos: return

        var_prnfile = util.getprintfilename()
        prn = printer.File(devfile=var_prnfile)

        prn.set(codepage=cfg_codepage)

        v_cabec = getBlob('cabecalho')
        prn.text(v_cabec, 1)

        prn.pulal()

        prn.textline(
            '{CondensedOn}' + str(datetime.datetime.now()) + '/usr:%s' % sos.usrent + '{CondensedOff}', 1)  # Datetime

        prn.set(bold=1, size='2x', align='center')
        prn.textline("--------------------")
        prn.textline(" ORÇAMENTO OS %s " % sos.os)
        prn.textline("--------------------")
        prn.set(bold=0, size='normal', align='left')

        if sos.dataent:
            prn.textline("Entrada em:" + CTL_HT + " %s " % '{:%d-%m-%Y %H:%M}'.format(sos.dataent))

        prn.textline("Cliente:\t %s " % sos.oscliente.nome if sos.oscliente else '')
        prn.textline("Telefones:\t  %s " % sos.oscliente.t4a if sos.oscliente else '')
        prn.pulal()

        prn.textline("Aparelho:\t %s " % sos.ostipo.nome if sos.ostipo else '')

        prn.textline("Marca:\t  %s " % sos.osmarca.nome if sos.osmarca else '')

        prn.textline("N° Serial:\t  %s " % str(sos.modelo))

        prn.textline("N° Serial:\t  %s " % str(sos.ns))

        if util.slen(sos.nf) > 0:
            prn.textline("NF:\t  %s " % asstr(str(sos.nf)))

        prn.textline(u"Solicitação:\t  %s " % asstr(sos.solicita))

        prn.textline(u"Acessorios:\t  %s " % asstr(sos.acess))

        prn.textline(u"Estado de Conservação:\t  %s " % asstr(sos.conserva))

        prn.textline(u"Prazo de Orçamento:\t  %s " % asstr(sos.prazoorc))

        prn.textline(u"Lembrete:\t  %s " % asstr(sos.lembrete))

        prn.textline(u"Observações:  %s " % asstr(sos.obsos))

        prn.text(getBlob('termoentradaos'), 1)
        prn.text(getBlob('rodape'), 1)

        # prn.pulal(10)
        prn.textline("____________________\n\r\n\r")
        prn.cut()

        prn.close()

        util.imprimeLPR(cfg_prntxt, var_prnfile)

    @staticmethod
    def imprimir_OS_saida(params):
        osn = nisk.util.defaultv(params, 'os', None)
        sos = consultaOS(osn)

        if not sos: return

        var_prnfile = util.getprintfilename()
        prn = printer.File(devfile=var_prnfile)

        prn.set(codepage=cfg_codepage)

        v_cabec = getBlob('cabecalho')
        prn.text(v_cabec, 1)

        prn.pulal()

        prn.textline(
            '{CondensedOn}' + str(datetime.datetime.now()) + '/usr:%s' % sos.usrent + '{CondensedOff}', 1)  # Datetime

        prn.set(bold=1, size='2x', align='center')
        prn.textline("--------------------")
        prn.textline(" ENTREGA OS %s " % sos.os)
        prn.textline("--------------------")
        prn.set(bold=0, size='normal', align='left')

        if sos.dataent:
            prn.textline("Entrada em:" + CTL_HT + " %s " % '{:%d-%m-%Y %H:%M}'.format(sos.dataent))

        prn.textline("Cliente:\t %s " % sos.oscliente.nome if sos.oscliente else '')
        prn.textline("Telefones:\t  %s " % sos.oscliente.t4a if sos.oscliente else '')
        prn.pulal()

        prn.textline("Aparelho:\t %s " % sos.ostipo.nome if sos.ostipo else '')

        prn.textline("Marca:\t  %s " % sos.osmarca.nome if sos.osmarca else '')

        prn.textline("N° Serial:\t  %s " % str(sos.modelo))

        prn.textline("N° Modelo:\t  %s " % str(sos.ns))

        if util.slen(sos.nf) > 0:
            prn.textline("NF:\t  %s " % asstr(str(sos.nf)))

        prn.textline(u"Solicitação:\t  %s " % asstr(sos.solicita))

        prn.textline(u"Acessorios:\t  %s " % asstr(sos.acess))

        prn.textline(u"Estado de Conservação:\t  %s " % asstr(sos.conserva))

        prn.textline(u"Prazo de Orçamento:\t  %s " % asstr(sos.prazoorc))

        prn.textline(u"Lembrete:\t  %s " % asstr(sos.lembrete))

        prn.textline(u"Observações:  %s " % asstr(sos.obsos))

        prn.text(getBlob('termoentradaos'), 1)
        prn.text(getBlob('rodape'), 1)

        # prn.pulal(10)
        prn.textline("____________________\n\r\n\r")
        prn.cut()

        prn.close()

        util.imprimeLPR(cfg_prntxt, var_prnfile)
