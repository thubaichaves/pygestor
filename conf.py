﻿#!/usr/bin/python
# -*- coding: utf-8 -*-

cfg_prntxt = "\\\\terminal1\\vox"
cfg_prnetq = "\\\\terminal1\\l42"

cfg_prncmd_cyg = 'printer.sh %var_prnfile %cfg_prntxt'
cfg_prncmd_win = 'lpr -d %cfg_prntxt %var_prnfile'
cfg_prncmd_unix = 'cat $1 | smbclient $2 -c "print -" -N -U "nisk%000"'

cfg_dburl = "firebird+fdb://sysdba:masterkey@localhost:3050/o:\\prog\\pygestor\\banco.fdb?charset=WIN1252"
cfg_sqlecho = False

cfg_dburl_list = {
    'dev': "firebird+fdb://sysdba:masterkey@localhost:3050/c:\\neon\\banco.gdb?charset=WIN1252",
    'server': "firebird+fdb://sysdba:masterkey@server:3050/c:\\neon\\banco.gdb?charset=WIN1252",
    'nb': "firebird+fdb://sysdba:masterkey@172.73.0.1:3050/c:\\neon\\banco.gdb?charset=WIN1252",
    'linux': "firebird+fdb://sysdba:masterkey@localhost:3050//srv/banco.fdb?charset=WIN1252",
}

cfg_codepage = 'cp850'
cfg_trashpath = 'trashx'

GlobalKeys = ('meta f1', 'meta f4', 'ctrl c', 'ctrl f')

keys = {
    ("edit", "EDIT_HOME"): 'ctrl a',
    ("edit", "EDIT_END"): 'ctrl e',
    ("edit", "EDIT_DELETE_TO_END"): 'ctrl k',
    ("edit", "EDIT_DELETE_LAST_WORD"): 'ctrl w',
    ("edit", "EDIT_ENTER"): 'enter',
    ("edit", "EDIT_COMPLETE"): 'shift tab',
    (("edit", "modal"), "MODAL_ESCAPE"): 'esc',
    ("selectable", "TEXT_SELECT"): ' ',
    ("selectable", "TEXT_SELECT2"): 'enter',
    ("menu_box", "MENU_BOX_UP"): 'up',
    ("menu_box", "MENU_BOX_LEFT"): 'left',
    ("menu_box", "MENU_BOX_RIGHT"): 'right',
    ("menu", "MENU_DOWN"): 'down',
    ("menu", "MENU_UP"): 'up',
    ("menu_roller", "MENU_ROLLER_UP"): 'up',
    ("menu_roller", "MENU_ROLLER_DOWN"): 'down',
    ("menu_roller", "MENU_ROLLER_RIGHT"): 'right',
    ("columns_roller", "COLUMNS_ROLLER_LEFT"): 'left',
    ("columns_roller", "COLUMNS_ROLLER_RIGHT"): 'right',
    ("focus", "FOCUS_SWITCH"): 'tab',
    ('focus', "FOCUS_UP"): 'ctrl up',
    ('focus', "FOCUS_DOWN"): 'ctrl down',
    ('focus', "FOCUS_LEFT"): 'ctrl left',
    ('focus', "FOCUS_RIGHT"): 'ctrl right',
    ('files_management', "FILES_HIDDEN_HIDE"): 'meta h',
    ('files_management', "FILES_JUMP_DIRECTORIES"): 'meta d',
    ('files_management', "FILES_JUMP_FILES"): 'meta f',
}

''' CORES

FORE
    'black'
    'dark red'
    'dark green'
    'brown'
    'dark blue'
    'dark magenta'
    'dark cyan'
    'light gray'
    'dark gray'
    'light red'
    'light green'
    'yellow'
    'light blue'
    'light magenta'
    'light cyan'
    'white'

BACK
    'black'
    'dark red'
    'dark green'
    'brown'
    'dark blue'
    'dark magenta'
    'dark cyan'
    'light gray'

OPTs
    'bold'
    'underline'
    'standout'

('InfoHeaderText', 'white, bold', 'dark blue'),  # header text
('flagged', 'black', 'dark green', ('bold', 'underline'))

'''

const_PALETTE = [
    ('handle', 'yellow', 'black', 'standout'),  # scrollbar manipulador
    ('scrollbar_bg', 'black', 'dark cyan', 'bold'),  # scrollbar fundo
    #
    ('PopupMessageBg', 'white', 'dark green'),  # popup message background
    ('windowsborder', 'white', 'dark green','bold,underline','#668', '#035'),
    ('windowsborder_of', 'white', 'dark green','bold,underline','#ddf', '#06a'),
    ('foot', 'light gray', 'dark blue', 'standout'),
    ('body', 'white', 'dark cyan'),
    ('body_of', 'black', 'dark gray'),
    ('key', 'dark blue', 'light gray'),
    ('title', 'white', 'black', 'bold'),

    #################################################################

    ('field', 'white', 'dark blue'),#'','#ffd', '#00a'),
    # ('field', 'white', 'dark cyan'),#'','#ffd', '#00a'),
    ('field_of', 'white', 'light red'),# 'bold','#ff8', '#806'),  ,

    ('fieldb',  'white', 'dark green'),#'','#ffd', '#00a'),
    ('field_ofb', 'white', 'light red'),# 'bold','#ff8', '#806'),

    ('field_cap', 'light gray', 'dark blue'),#'','#ffd', '#00a'),
    ('fieldb_cap', 'light gray', 'dark green'),#'','#ffd', '#00a'),
    ('field_cap_of', 'black', 'light gray'),# 'bold','#ff8', '#806'),  ,
    ('field_cap_ofb', 'black', 'dark gray'),# 'bold','#ff8', '#806'),  


    ('gridrow', 'white', 'dark blue'),#'','#ffd', '#00a'),
    ('gridhead', 'yellow', 'dark blue'),
    ('gridrowb',  'white', 'dark blue'),#'','#ffd', '#00a'),
    ('gridrow_of', 'white', 'light red'),# 'bold','#ff8', '#806'),  ,
    ('gridrow_ofb', 'white', 'light red'),

    ('heading', 'black', 'light red'),
    ('line', 'light gray', 'white'),
    ('options', 'white', 'dark blue','bold,underline','#fff', '#06a'),
    ('options_nf', 'white', 'dark blue','bold,underline','#668', '#035'),
    ('selected', 'white', 'light red'),

    #################################################################
    ('menubar', 'white', 'dark blue'),
    ('menubar_focus', 'dark blue', 'white'),
    ('menuitem', 'white', 'dark blue'),
    ('menuitem_focus', 'dark blue', 'white'),
    #################################################################
    ('Field', 'dark green', 'black'),  
    ('OnFocusBg', 'black', 'light blue'),  # background when a widget is focused
    ('Info', 'white', 'light blue'),  # information in fields
    ('Bg', 'dark gray', 'black'),  # screen background
    ('InfoFooterText', 'white', 'dark blue'),  # footer text
    ('InfoFooterHotkey', 'white', 'light blue'),  # hotkeys in footer text
    ('InfoFooter', 'yellow', 'dark blue'),  # footer background
    ('InfoHeaderText', 'white', 'dark blue'),  # header text
    ('InfoHeader', 'black', 'dark blue'),  # header background
    ('GeneralInfo', 'brown', 'black'),  # main menu text
    ('LastModifiedField', 'dark cyan', 'black'),  # Last modified:
    ('LastModifiedDate', 'dark cyan', 'black'),  # info in Last modified:
    ('PopupMessageText', 'black', 'dark cyan'),  # popup message text
    ('SearchBoxHeaderText', 'light gray', 'dark cyan'),  # field names in the search box
    ('SearchBoxHeaderBg', 'black', 'dark cyan'),  # field name background in the search box
    ('Relogio', 'white', 'dark red'),  # background when a widget is focused

    ('flagged', 'black', 'dark green', ('bold', 'underline')),
    ('focus', 'light gray', 'dark blue', 'standout'),
    ('flagged focus', 'yellow', 'dark cyan',
    ('bold', 'standout', 'underline')),
    ('head', 'yellow', 'black', 'standout'),
    ('dirmark', 'black', 'dark cyan', 'bold'),
    ('flag', 'dark gray', 'light gray'),
    ('error', 'dark red', 'light gray'),
    (None, 'light gray', 'black'),

    ('focus heading', 'white', 'light red'),
    ('focus line', 'black', 'light red'),
    ('focus options', 'black', 'light gray'),
]
def mudacor():
    conf.const_PALETTE[3] = ('windowsborder', 'white', 'black')
    tui.mdi.loop.screen.register_palette(conf.const_PALETTE)
    pass

sizes = {
    "ListBrowser1": ( ('fixed left', 8), 120, ('fixed top', 6), 40),
    "wgtFieldBoxDb1": (18, 5  ),
    "wgtFieldBox": 18,
    "statusbarbuttonA": 20,


}
menu_top = (
    u'Neon Gestor', [
        (u'&Ordem de Serviço', [
            (u'&Listar OSs', 'os_lista'),
            (u'&Criar OS', 'os_create'),
            (u'&Abrir OS', 'os_abrir'),
            (u'Imprimir Entrada OS', 'os_print_ent'),
            (u'Histórico', [
                (u'Visualisar Histórico',),
                (u'Terminal')]),
            (u'Encerrar OS'),
            (u'Incluir Tarefa')]),
        (u'Pro&dutos', [
            (u'Relatórios', [
                (u'Discriminação de Orçamento')]),
            (u'Etiquetas')]),
        (u'Con&tatos', [
            (u'Relatórios', [
                (u'Discriminação de Orçamento')]),
            (u'Etiquetas')]),
        (u'Fina&nceiro', [
            (u'Caixa', [
                (u'Discriminação de Orçamento')]),
            (u'Títulos', [
                (u'Títulos a Receber'),
                (u'Títulos a Pagar'),
                (u'Incluir Novo Título'),
                (u'Títulos Atrasados')])]),
        (u'Des&logar', 'logout'),
        (u'&Sair', 'sair')]
)
menu_os_edit = (
    u'Menu', [
        (u'&Ordem de Serviço', [
            (u'&Histórico', [
                (u'&Visualisar Histórico',),
                (u'&Terminal')]),
            (u'&Encerrar OS'),
            (u'&Incluir Tarefa')]),
        (u'&Impressão', [
            (u'&Relatórios', [
                (u'&Discriminação de Orçamento')]),
            (u'&Cupom de Entrada',('imprime','entrada')),
            (u'&Etiqueta',('imprime','etiq')),
            (u'Etiqueta &anotável',('imprime','etiqa')),
            (u'&Ficha de Análise',('imprime','fichaanalise')),
            (u'&Ficha de Q.C.',('imprime','fichaqc')),
            (u'&Orçamento',('imprime','orc')),
            (u'&Cupom de Saída',('imprime','saida'))]),
        (u'&Salvar', 'saveorabort'),
        (u'Cancelar', 'abort')])

menu_contatos_edit = (
    u'Menu', [
        (u'&Contatos', [
            (u'&Histórico')]),
        (u'&Salvar', 'saveorabort'),
        (u'Cancelar', 'abort')])

menu_listsA_edit = (
    u'Menu', [
        (u'&Contatos', [
            (u'&Histórico')]),
        (u'&Salvar', 'save'),
        (u'Cancelar', 'abort')])

menu_os_add = (
    u'Menu', [
        (u'Relatar OS &Anterior', 'osanterior'),
        (u'&Concluir', 'concluir'),
        (u'Cance&lar', 'cancel')])

footer_frmListContatos2 = [
        ('title', "OK"), ('key', "Enter"), "|",
        ('title', "Voltar"), ('key', "Home"), "|",
        ('title', "Novo"), ('key', "F2"), "|",
        ('title', "Editar"), ('key', "F4"), "|",
        ('title', "Cancelar"), ('key', "ESC" ), "\n",
        #
        # ('title', "Infomacoes Sobre o Contato"), ('key', "F5"), "|",
        # ('title', "Ajuda"), ('key', "Ctrl-Back"), "|",
    ]


textos = {
    'frmmain.statustext': ('InfoFooterText', ['Escolha a Opção no Menu. As Letras em DESTAQUE são ATALHOS']),
    'frmmain.mural.titulo':'*** Mural ***',
    ############################################################################################################
    'crtl_os.erro_abriros':'Não foi possível abrir essa OS',
    'crtl_os.erro_abriros1':'Não foi possível abrir essa OS',
    'crtl_os.erro_abriros2':'Não foi possível abrir essa OS',
    ############################################################################################################
    '':'',
}

class cmds:
    cmd_frmMain = "cmd_frmMain"
    cmd_checkLogin = "cmd_checkLogin"
    cmd_os_impr = "cmd_os_impr"
    cmd_os_create= "cmd_os_create"
    cmd_os_list= "cmd_os_list"

    dlg_frmlistsA_add = "dlg_frmlistsA_add"
    dlg_frmlistsA_open = "dlg_frmlistsA_open"

    dlg_frmlistcontatos_add = "dlg_frmlistcontatos_add"
    dlg_frmlistcontatos_open = "dlg_frmlistcontatos_open"

    dlg_statusbar_put = "dlg_statusbar_put"
    dlg_statusbar_pop = "dlg_statusbar_pop"
    dlg_statusbar_change = "dlg_statusbar_change"

    OS_ADD = "novaOS"
    STARTUP = "STARTUP"
    OS_OPEN = "abrirOS"
    OS_PRINTENT = "OS_printent"
    DELETE_USER = "deleteUser"
    CANCEL_SELECTED = "cancelSelected"

    USER_SELECTED = "userSelected"
    USER_ADDED = "userAdded"
    USER_UPDATED = "userUpdated"
    USER_DELETED = "userDeleted"

    ADD_ROLE = "addRole"
    ADD_ROLE_RESULT = "addRoleResult"

    SHOW_DIALOG = "showDialog"
    SESSION_UNLOGIN = "SESSION_UNLOGIN"


corJanela = 'janela'
corButton = 'button'
corTxtfield = 'txtfield'
corLabel = 'label'


# NORMAL_FG_16 = "default"
# NORMAL_BG_16 = "black"
#
# NORMAL_FG_256 = "default"
# NORMAL_BG_256 = "black"
#
# FOCUSED_FG_16 = "black"
# FOCUSED_FG_256 = "black"
#
# FOCUSED_BG_16 = "light gray"
# FOCUSED_BG_256 = "g40"
#
# HEADER_FG_16 = "black,bold"
# HEADER_FG_256 = "black,bold"
#
# HEADER_BG_16 = "white"
# HEADER_BG_256 = "g99"
#
# HIGHLIGHT_FG_16 = "light green,bold"
# HIGHLIGHT_BG_16 = HEADER_BG_16
#
# HIGHLIGHT_FG_256 = "light green,bold"
# HIGHLIGHT_BG_256 = HEADER_BG_256
# const_PALETTE = [('menubar', 'white,bold', 'dark blue'),
# ('menubar_focus', 'dark blue,bold', 'white'),("normal",
# NORMAL_FG_16, NORMAL_BG_16, "default",
# NORMAL_FG_256, NORMAL_BG_256),
# ("focused",
#          FOCUSED_FG_16, FOCUSED_BG_16, "default,underline",
#          FOCUSED_FG_256, FOCUSED_BG_256),
#         ("normal focused",
#          FOCUSED_FG_16, FOCUSED_BG_16, "default,underline",
#          FOCUSED_FG_256, FOCUSED_BG_256),
#         ("header",
#          HEADER_FG_16, HEADER_BG_16, "standout",
#          HEADER_FG_256, HEADER_BG_256),
#         ("header focused",
#          HEADER_FG_16, FOCUSED_BG_16, "standout,underline",
#          HEADER_FG_256, FOCUSED_BG_256),
#         ("highlight",
#          HIGHLIGHT_FG_16, HEADER_BG_16, "standout,bold",
#          HIGHLIGHT_FG_256, HEADER_BG_256),
#         ("highlight focused",
#          HIGHLIGHT_FG_16, FOCUSED_BG_16, "standout,bold,underline",
#          HIGHLIGHT_FG_256, FOCUSED_BG_256), ]
