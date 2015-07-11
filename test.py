# !/usr/bin/python
# -- coding: utf-8 --

# from conf import *
# from sqlalchemy.orm import sessionmaker
#
# # from nisk import *
#
# # from escposx import *
# # from escposx.constants import *
# import time
# import sqlite3
# import fdb
#
#
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
#
#
# Base = declarative_base()
# session = scoped_session(sessionmaker())
#
#
# class User(Base):
# __tablename__ = "user"
# id = Column(Integer, primary_key=True)
#     name = Column(String(255))
#
#
# def init_db(dbname='firebird+fdb://sysdba:masterkey@localhost:3050/c:\\teste3.fdb?charset=WIN1252'):
#     try:
#         engine = create_engine(dbname, echo=False)
#     except:
#         pass
#     try:
#         session.remove()
#     except:
#         pass
#     session.configure(bind=engine, autoflush=False, expire_on_commit=False)
#     try:
#         Base.metadata.drop_all(engine)
#     except:
#         pass
#     try:
#         Base.metadata.create_all(engine)
#     except:
#         pass
#     return engine
#
#
# def test_sqlalchemy_orm(number_of_records=10000):
#     init_db()
#     start = time.time()
#     for i in range(number_of_records):
#         user = User()
#         user.name = 'NAME ' + str(i)
#         user.id = i
#         session.add(user)
#     session.commit()
#     end = time.time()
#     print "SQLAlchemy ORM: Insert {0} records in {1} seconds".format(
#         str(number_of_records), str(end - start)
#     )
#
#
# def test_sqlalchemy_core(number_of_records=10000):
#     engine = init_db()
#     start = time.time()
#     engine.execute(
#         User.__table__.insert(),
#         [{"name": "NAME " + str(i),'id': i} for i in range(number_of_records)]
#     )
#     end = time.time()
#     print "SQLAlchemy Core: Insert {0} records in {1} seconds".format(
#         str(number_of_records), str(end - start)
#     )
#
# def init_fdb(dsn='localhost:c:\\teste2.fdb',puser='sysdba',ppassword='masterkey'):
#     conn =fdb.connect(
# 	  dsn=dsn,
# 	  user=puser,
# 	  password=ppassword,
# 	  charset='WIN1252')
#     cursor = conn.cursor()
#     try:
#         cursor.execute("DROP TABLE USERx;")
#     except:
#         pass
#     cursor.execute("CREATE TABLE userx (id int not null primary key, name VARCHAR(9999));")
#     conn.commit()
#     return conn
#
# def init_sqlite3(dbname="sqlite3.db"):
#     conn = sqlite3.connect(dbname)
#     cursor = conn.cursor()
#     cursor.execute("DROP TABLE IF EXISTS user")
#     cursor.execute("CREATE TABLE user (id INTEGER NOT NULL, name VARCHAR(9999), PRIMARY KEY(id))")
#     conn.commit()
#     return conn
#
# def test_sqlite3(number_of_records=10000):
#     conn = init_sqlite3()
#     cursor = conn.cursor()
#     start = time.time()
#     for i in range(number_of_records):
#         cursor.execute("INSERT INTO user (name) VALUES (?)", ("NAME " + str(i),))
#     conn.commit()
#     end = time.time()
#     print "sqlite3: Insert {0} records in {1} seconds".format(
#         str(number_of_records), str(end - start)
#     )
#
# def test_fdb(number_of_records=10000):
#     conn = init_fdb()
#     cursor = conn.cursor()
#     start = time.time()
#     for i in range(number_of_records):
#         cursor.execute("INSERT INTO userx (name,id) VALUES (?,?)", ("NAME " + str(i),i,))
#     conn.commit()
#     end = time.time()
#     print "fdb: Insert {0} records in {1} seconds".format(
#         str(number_of_records), str(end - start)
#     )
#
# if __name__ == "__main__":
#     test_sqlite3()
#     test_fdb()
#     test_sqlalchemy_core()
#     # test_sqlalchemy_orm()
#

from pyGestorModel.orm_os import *
from pyGestorModel.orm_listas import *
from sqlalchemy.orm import *
from conf import *
import logging

logging.basicConfig(filename='test.log', level=logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

engine = create_engine(cfg_dburl, echo=True)
Session = sessionmaker(bind=engine)  #,autoflush=False)
Session.configure(bind=engine)
session = Session()

va = session.query(os_os).filter(and_(os_os.marca > 0, os_os.tipo > 0)).options(
    joinedload(os_os.osmarca).load_only("nome"),
    defaultload(os_os.ostipo).load_only("nome"),
)

vx = va.first()

vc = long(1061 + 2)

print vx.marca
setattr(vx, 'marca', vc)

session.commit()



#
# def consulta():
# engine = create_engine(cfg_dburl, echo=True)
#     Session = sessionmaker(bind=engine)
#     Session.configure(bind=engine)
#     session = Session()
#     conts = session.query(orm_os.os_os)
#
#     #for Contato in conts: print Contato
#     #print conts.count()
#
#     #num1 = input('OS para imprimir: ')
#
#     sos = conts.filter(orm_os.os_os.os == 8887).first()
#     return sos
#     #print sos.count()
#
# def Imprimir_EntradaOS():
#     sos = consulta()
#     var_prnfile=GetPrintFileName()
#
#     print var_prnfile
#     prn = printer.File(devfile = var_prnfile)
#
#     '''
#                     bool epsoncode = true;
#                     var printer = new
#                         Reporter2(Settings.Default.impmp);
#                     printer.StartJob();
#                     // printer.Clean = true;
#                     var tmp = new EpsonCodes();
#                     //if (epsoncode) printer.PutText(tmp.LinesInch6);
#                     //
#                     printer.PutLine("");
#                     printer.PrintStringsLine(LocalConf.GetBlobBank("cabecalho"));
#                     printer.PutLine(DateTime.Now.ToString("dd/MM/yyyy HH:mm"));
#                     printer.PutLine(" ");
#                     //
#                     printer.PutLine((epsoncode ? tmp.ExpandedOn + tmp.BoldOn : "") + "--------------------");
#     '''
#
#     prn.set(codepage = cfg_codepage)
#
#     prn.set(bold=1,inverted = True, size='2x')
#
#     prn.text(" áéíóúçã OS %s " % sos.os)
#     prn.text(TEXT_STYLE['bold'][0])
#     prn.text(TEXT_STYLE['size']['normal'])
#
#
#     prn.text(CTL_LF)
#
#     prn.set(inverted = False, underline=1)
#
#     prn.text("Entrada OS \n\r %s " %  '{:%Y-%m-%d %H:%M:%S}'.format(sos.dataent))
#
#     prn.text(CTL_LF)
#
#     prn.set(inverted = False, underline=2, font='b')
#
#
#     prn.text("SAÍDA%s de OS %s \n\r" %( CTL_HT, '{:%Y-%m-%d %H:%M:%S}'.format(sos.datasai)))
#     prn.text("SA%s de OS %s " %( CTL_HT, '{:%Y-%m-%d %H:%M:%S}'.format(sos.datasai)))
#
#
#     prn.text(CTL_LF)
#     prn.text(CTL_LF)
#     prn.text(CTL_LF)
#     prn.text(CTL_LF)
#
#     prn.close()
#
#     ''' Imprime via LPR
#     #from subprocess import call #'''
#     call(["lpr", "-d",cfg_prntxt, var_prnfile])
#
#     '''
#                     printer.PutLine("  ABERTURA OS " + ((c.RegSource1["OS"] != null) ? c.RegSource1["OS"].ToString() : ""));
#                     printer.PutLine("--------------------" + (epsoncode ? tmp.ExpandedOff + tmp.BoldOff : ""));
#                     //
#                     printer.PutLine("ENTRADA: " +
#                                     ((c.RegSource1["DATAENT"] is DateTime
#                                           ? ((DateTime)c.RegSource1["DATAENT"]).ToString("dd/MM/yyyy HH:mm")
#                                           : "")));
#                     printer.PutLine(" ");
#                     printer.PutLine((epsoncode ? tmp.BoldOn : "") + "Cliente: " +
#                                     u.limit(u.CoalesceS(c.RegSource1["T3XD"]), 31) + (epsoncode ? tmp.BoldOff : ""));
#
#                     printer.PutLine("Fones: " + (u.CoalesceS(c.RegSource1["T4D"])));
#                     printer.PutLine(" ");
#                     //
#                     bool bold = false;
#
#                     if (!String.IsNullOrEmpty(c.RegSource1["T1XC"] as String))
#                     {
#                         printer.PutLine((bold && epsoncode ? tmp.BoldOn : ""));
#                         printer.PrintText_incolRight("Aparelho:", center);
#                         printer.PutText((bold ? tmp.BoldOff : ""));)
#                         printer.PrintText_incol((c.RegSource1["T1XC"] as String), center + 1);
#                     }
#                     if (!String.IsNullOrEmpty(c.RegSource1["T1XD"] as String))
#                     {
#                         printer.PutLine((bold && epsoncode ? tmp.BoldOn : ""));
#                         printer.PrintText_incolRight("Marca:", center);
#                         printer.PutText((bold ? tmp.BoldOff : ""));
#                         printer.PrintText_incol((c.RegSource1["T1XD"] as String), center + 1);
#                     }
#                     if (!String.IsNullOrEmpty(c.RegSource1["MODELO"] as String))
#                     {
#                         printer.PutLine((bold && epsoncode ? tmp.BoldOn : ""));
#                         printer.PrintText_incolRight("Modelo:", center);
#                         printer.PutText((bold ? tmp.BoldOff : ""));
#                         printer.PrintText_incol(c.RegSource1["MODELO"] as String, center + 1);
#                     }
#                     ////
#                     if (!String.IsNullOrEmpty(c.RegSource1["NS"] as String))
#                     {
#                         printer.PutText((bold ? tmp.BoldOn : ""));
#                         printer.PrintText_incolRight("Serial:", center);
#                         printer.PutText((bold ? tmp.BoldOff : ""));
#                         printer.PrintText_incol(c.RegSource1["NS"] as String, center + 1);
#                     }
#                     if (!String.IsNullOrEmpty(c.RegSource1["NF"] as String))
#                     {
#                         printer.PutText((bold ? tmp.BoldOn : ""));
#                         printer.PrintText_incolRight("NF:", center);
#                         if (epsoncode)
#                             printer.PutText(tmp.BoldOff);
#                         printer.PrintText_incol(c.RegSource1["NF"] as String, center + 1);
#                     }
#                     if (!String.IsNullOrEmpty(c.RegSource1["ACESS"] as String))
#                     {
#                         printer.PutText((bold ? tmp.BoldOn : ""));
#                         printer.PrintText_incolRight("Acessórios:", center);
#                         printer.PutText((bold ? tmp.BoldOff : ""));
#                         printer.PrintText_incol(c.RegSource1["ACESS"] as String, center + 1);
#                     }
#                     ////
#                     //printer.PutLine(" ");
#                     if (!String.IsNullOrEmpty(c.RegSource1["CONSERVA"] as String))
#                     {
#                         printer.PutLine((bold && epsoncode ? tmp.BoldOn : "") + "  Conserv.:" + tmp.BoldOff);
#                         printer.PrintText_incol(c.RegSource1["CONSERVA"] as String, center + 1);
#                     }
#                     ////
#                     if (!String.IsNullOrEmpty(c.RegSource1["SOLICITA"] as String))
#                     {
#                         printer.PutLine((bold && epsoncode ? tmp.BoldOn : "") + "   Serviço:" + tmp.BoldOff);
#                         printer.PrintText_incol(c.RegSource1["SOLICITA"] as String, center + 1);
#                     }
#                     ////
#                     if (!String.IsNullOrEmpty(c.RegSource1["PRAZOORC"] as String))
#                     {
#                         printer.PutLine((bold && epsoncode ? tmp.BoldOn : "") + "Prazo orc.:" + tmp.BoldOff);
#                         printer.PrintText_incol(c.RegSource1["PRAZORC"] as String, center + 1);
#                     }
#                     ////
#                     if (!String.IsNullOrEmpty(c.RegSource1["OBSOS"] as String))
#                     {
#                         printer.PutLine(
#                             (bold && epsoncode ? tmp.BoldOn : "") + "      OBS.: " + tmp.BoldOff + c.RegSource1["OBSOS"]);
#                     }
#                     printer.PutLine(" ");
#
#                     printer.PrintStringsLine(LocalConf.GetBlobBank("termoentradaos"));
#
#                     printer.PrintStringsLine(LocalConf.GetBlobBank("rodape"));
#
#                     printer.PutText(tmp.Reset); //tmp.Eject + "" + tmp.BoldOff + );
#                     printer.PrintJob();
#                 }
#                 if (MessageBox.Show("Deseja Imprimir Via do Estabelecimento?", "Atenção", MessageBoxButtons.YesNo) ==
#                     DialogResult.Yes)
#                 {
#                     int center = 12;
#                     //testaEpson();
#                     if (c == null || c.RegSource1 == null)
#                         return;
#                     //
#                     bool epsoncode = true;
#                     var printer = new
#                         Reporter2(Settings.Default.impmp);
#                     printer.StartJob();
#                     printer.Clean = true;
#                     var tmp = new EpsonCodes();
#                     //if (epsoncode) printer.PutText(tmp.LinesInch6);
#                     //
#                     printer.PutLine("");
#                     printer.PutLine((epsoncode ? tmp.ExpandedOn + tmp.BoldOn : "") + "Niskalkat Tecnologia");
#                     if (epsoncode) printer.PutText(tmp.ExpandedOff + tmp.BoldOff);
#                     //
#                     printer.PutLine(" ");
#                     printer.PutLine("Nisk Tecnologia");
#                     printer.PutLine(" ");
#                     //
#                     printer.PutLine("            Via do Estabelecimento");
#                     printer.PutLine((epsoncode ? tmp.ExpandedOn + tmp.BoldOn : "") + "--------------------");
#                     printer.PutLine("  ABERTURA OS " + ((c.RegSource1["OS"] != null) ? c.RegSource1["OS"].ToString() : ""));
#                     printer.PutLine("--------------------" + (epsoncode ? tmp.ExpandedOff + tmp.BoldOff : ""));
#
#                     printer.PutLine("ENTRADA: " +
#                                     ((c.RegSource1["DATAENT"] is DateTime
#                                           ? ((DateTime)c.RegSource1["DATAENT"]).ToString("dd/MM/yyyy HH:mm")
#                                           : "")));
#                     printer.PutLine(" ");
#                     printer.PutLine((epsoncode ? tmp.BoldOn : "") + "Cliente: " +
#                                     u.limit(u.CoalesceS(c.RegSource1["T3XD"]), 31) + (epsoncode ? tmp.BoldOff : ""));
#
#                     printer.PutLine("Fones: " + (u.CoalesceS(c.RegSource1["T4D"])));
#                     printer.PutLine(" ");
#                     //
#                     bool bold = false;
#
#                     if (!String.IsNullOrEmpty(c.RegSource1["T1XC"] as String))
#                     {
#                         printer.PutLine((bold && epsoncode ? tmp.BoldOn : ""));
#                         printer.PrintText_incolRight("Aparelho:", center);
#                         printer.PutText((bold ? tmp.BoldOff : ""));
#                         printer.PrintText_incol((c.RegSource1["T1XC"] as String), center + 1);
#                     }
#                     if (!String.IsNullOrEmpty(c.RegSource1["T1XD"] as String))
#                     {
#                         printer.PutLine((bold && epsoncode ? tmp.BoldOn : ""));
#                         printer.PrintText_incolRight("Marca:", center);
#                         printer.PutText((bold ? tmp.BoldOff : ""));
#                         printer.PrintText_incol((c.RegSource1["T1XD"] as String), center + 1);
#                     }
#                     if (!String.IsNullOrEmpty(c.RegSource1["MODELO"] as String))
#                     {
#                         printer.PutLine((bold && epsoncode ? tmp.BoldOn : ""));
#                         printer.PrintText_incolRight("Modelo:", center);
#                         printer.PutText((bold ? tmp.BoldOff : ""));
#                         printer.PrintText_incol(c.RegSource1["MODELO"] as String, center + 1);
#                     }
#                     ////
#                     if (!String.IsNullOrEmpty(c.RegSource1["NS"] as String))
#                     {
#                         printer.PutText((bold ? tmp.BoldOn : ""));
#                         printer.PrintText_incolRight("Serial:", center);
#                         printer.PutText((bold ? tmp.BoldOff : ""));
#                         printer.PrintText_incol(c.RegSource1["NS"] as String, center + 1);
#                     }
#                     if (!String.IsNullOrEmpty(c.RegSource1["NF"] as String))
#                     {
#                         printer.PutText((bold ? tmp.BoldOn : ""));
#                         printer.PrintText_incolRight("NF:", center);
#                         if (epsoncode)
#                             printer.PutText(tmp.BoldOff);
#                         printer.PrintText_incol(c.RegSource1["NF"] as String, center + 1);
#                     }
#                     if (!String.IsNullOrEmpty(c.RegSource1["ACESS"] as String))
#                     {
#                         printer.PutText((bold ? tmp.BoldOn : ""));
#                         printer.PrintText_incolRight("Acessórios:", center);
#                         printer.PutText((bold ? tmp.BoldOff : ""));
#                         printer.PrintText_incol(c.RegSource1["ACESS"] as String, center + 1);
#                     }
#                     ////
#                     //printer.PutLine(" ");
#                     if (!String.IsNullOrEmpty(c.RegSource1["CONSERVA"] as String))
#                     {
#                         printer.PutLine((bold && epsoncode ? tmp.BoldOn : "") + "  Conserv.:" + tmp.BoldOff);
#                         printer.PrintText_incol(c.RegSource1["CONSERVA"] as String, center + 1);
#                     }
#                     ////
#                     if (!String.IsNullOrEmpty(c.RegSource1["SOLICITA"] as String))
#                     {
#                         printer.PutLine((bold && epsoncode ? tmp.BoldOn : "") + "   Serviço:" + tmp.BoldOff);
#                         printer.PrintText_incol(c.RegSource1["SOLICITA"] as String, center + 1);
#                     }
#                     ////
#                     if (!String.IsNullOrEmpty(c.RegSource1["PRAZOORC"] as String))
#                     {
#                         printer.PutLine((bold && epsoncode ? tmp.BoldOn : "") + "Prazo orc.:" + tmp.BoldOff);
#                         printer.PrintText_incol(c.RegSource1["PRAZORC"] as String, center + 1);
#                     }
#                     ////
#                     if (!String.IsNullOrEmpty(c.RegSource1["OBSOS"] as String))
#                     {
#                         printer.PutLine(
#                             (bold && epsoncode ? tmp.BoldOn : "") + "      OBS.: " + tmp.BoldOff + c.RegSource1["OBSOS"]);
#                     }
#
#                     printer.PutLine(" ");
#                     printer.PutLine("    ------------------------------------");
#                     printer.PutLine("  Assinatura " +
#                                     ((!String.IsNullOrEmpty(c.RegSource1["PORTENT"] as String))
#                                          ? "(Portador: " + (c.RegSource1["PORTENT"] as String) + ")"
#                                          : "") + (epsoncode ? tmp.CondensedOff : ""));
#                     printer.PutLine(" ");
#
#                     printer.PrintStringsLine(LocalConf.GetBlobBank("termoentradaos"));
#
#                     printer.PutText(tmp.Reset); //tmp.Eject + "" + tmp.BoldOff + );
#                     printer.PrintJob();
#                 }
#             }
#             '''
#
#

# Imprimir_EntradaOS()

# #!/usr/bin/python
# # -*- coding: utf-8 -*-
#
# import sys
#
# import time
# import urwid
# from nisk.nsat_widgets import Menu
# import nisk
# from pyGestorForms import frmLogin
#
#
# class FormStart(object):
#     def __init__(self):
#         self._frame = urwid.Frame(urwid.Filler(urwid.Text('')))
#         self.alerttext = urwid.Text(('PopupMessageText', 'Are you sure you want to cancel?\n[Y/N]'), align='center')
#         self.statusbar = urwid.Text(('InfoFooterText', ['Press ', ('InfoFooterHotkey', '"ESC"'), ' for main screen, ',
#                                                         ('InfoFooterHotkey', '"A"'), ' to add, ',
#                                                         ('InfoFooterHotkey', '"S"'), ' to search again']),
#                                     align='center')
#         self.lblRelogio = urwid.AttrWrap(urwid.Text('', align='center'), 'Relogio')
#
#         footer = urwid.AttrMap(urwid.Columns([self.statusbar, ('fixed', 20, self.lblRelogio)]), 'InfoFooter')
#         self.loop = urwid.MainLoop(self._frame, const_PALETTE, unhandled_input=self.keyHandler)
#         self._frame.set_header(self.buildMenu())
#         self._frame.set_footer(footer)
#         self._frame.set_focus('header')
#         self.loop.set_alarm_in(1, self.alarmou, None)
#         self.mainScreen = self._frame
#         nisk.MainHost = self
#
#     def run(self):
#         self.loop.run()
#
#     def _messageExit(self, message):
#
#         lb = nisk.LineBox(self.alerttext, title='|** Import **|')
#
#         from trash import forms
#
#         lb = forms.MyForm()
#
#         w = urwid.Overlay(urwid.AttrWrap(lb, 'PopupMessageBg'), self._frame, 'center', 40, 'middle', None)
#         self.loop.widget = w
#
#         # self.loop.run()
#         #self.loop.draw_screen()
#         #5 seconds pause
#         #time.sleep(5)
#         #see you
#         #self.loop.widget = _frame
#         #self.loop.run()
#         #self.loop.draw_screen()
#         #raise urwid.ExitMainLoop()
#         #sys.exit("You have quit Gestor. Have a nice day!\n")
#
#     def alarmou(self, xxx, yyy):
#         self.lblRelogio.set_text(time.strftime('%H:%M:%S'))
#         self.loop.set_alarm_in(1, self.alarmou, None)
#
#     def actSai(self):
#         sys.exit("Obrigado por usar Neon Gestor!\n")
#
#     def _resume(self):
#
#         self.loop.widget = self._frame
#         # self.loop.draw_screen()
#         #self.loop.draw_screen()
#         #5 seconds pause
#         #see you
#         #self.loop.run()
#
#         #time.sleep(10)
#         #self.loop.draw_screen()
#         #raise urwid.ExitMainLoop()
#         # sys.exit("You have quit Gestor. Have a nice day!\n")
#
#     def menu_cb(self, menu_data):
#         self._messageExit("Menu selected: %s/%s" % menu_data)
#
#     def exit_cb(self, menu_data):
#         self._messageExit("Exiting throught 'Exit' menu item")
#
#     def buildMenu(self):
#         self.menu = Menu(self.loop)
#
#         _menu1 = "Comercial"
#         self.menu.addMenu(_menu1, 'Produtos e Preços', self.menu_cb, 'meta p')  # Adding a menu is quite easy
#         self.menu.addMenu(_menu1, "Novo Orçamento/Venda a-V", self.menu_cb,
#                           'meta v')  # Here the callback is always the same,
#         self.menu.addMenu(_menu1, "Encomendas", self.menu_cb, 'meta e')  # but you use different ones in real life :)
#         self.menu.addMenu(_menu1, "Demais Operações", self.exit_cb, 'd')  # You can also add a shortcut
#
#         _menu2 = "Serviços"
#         self.menu.addMenu(_menu2, "Nova OS a-N", self.menu_cb, 'meta n')
#         self.menu.addMenu(_menu2, "Consultar OS", self.menu_cb, 'meta o')
#         self.menu.addMenu(_menu2, "Imprimir Etiqueta de OS", self.menu_cb)
#
#         _menu2 = "Financeiro"
#         self.menu.addMenu(_menu2, "Caixa a-C", self.menu_cb, 'meta c')
#         self.menu.addMenu(_menu2, "Novo Lançamento de Caixa", self.menu_cb)
#         self.menu.addMenu(_menu2, "Fechar Caixa", self.menu_cb)
#
#         _menu2 = "Útil"
#         self.menu.addMenu(_menu2, "Imprimir Etiqueta", self.menu_cb)
#         self.menu.addMenu(_menu2, "Lista de Contatos", self.menu_cb)
#         self.menu.addMenu(_menu2, "Realizar Backup", self.menu_cb)
#
#         _menu2 = "Outros"
#         self.menu.addMenu(_menu2, "Ajuda", self.menu_cb)
#         self.menu.addMenu(_menu2, "Configurações", self.menu_cb)
#         self.menu.addMenu(_menu2, "Sair a-esc", self.menu_cb, 'meta esc')
#
#         return self.menu
#
#     def roda(self, janela):
#         if (janela == 'frmLogin'):
#             frmLogin.frmLoginScreens().showLogwin(self)
#
#             # statusbar.set_text('frmLogin')
#             #frmInterfaces = frmLogin.frmLoginScreens()
#             #frmLoginInst = frmInterfaces.showLogwin(self)
#
#             #self.loop.unhandled_input = frmInterfaces.frmLoginMenu
#
#             #self.loop.widget = urwid.Overlay(frmLoginInst,_frame, 'center', 50, 'middle', 20)
#             #self.loop.widget = frmLoginInst
#             #urwid.MainLoop(frmLoginInst, self.palette, unhandled_input=frmInterfaces.frmLoginMenu )
#
#             #self.loop.run()
#         return
#
#     def get_Loop(self):
#         return self.loop;
#
#     def get_Frame(self):
#         return self._frame;
#
#     def keyHandler(self, input):
#         if input in ('meta esc', 'meta f4', 'f1'):
#             raise urwid.ExitMainLoop()
#
#         if input in ('ctrl c', 'ctrl esc', 'meta f1'):
#             return self.actSai()
#
#         elif input in ('x', 'X'):
#             self._resume()
#
#         elif input in ('b', 'B', 'ctrl f'):
#             self.statusbar.set_text('bbbbbbb')
#
#         elif input in ('o', 'O'):
#             self.roda('frmLogin')
#
#         elif input in ('i', 'I'):
#             self.roda('frmLogin')
#
#         else:
#             return self.menu.checkShortcuts(input)  # needed to manage shortcuts
#
#
# # teste mvc
# import mvc
#
# #if __name__ == '__init__':Frame)
# #wxApp.MainLoop()
#
# mainform = mvc.components.WxApp()
#
# app = mvc.main.AppFacade.getInstance()
#
# app.sendNotification(mvc.main.AppFacade.STARTUP, mainform.x)
# mainform.run()
#
# #wxApp = components.WxApp()
# #app.sendNotification(AppFacade.STARTUP, wxApp.app
