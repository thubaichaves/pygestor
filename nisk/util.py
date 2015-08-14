#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import conf
import datetime
import time
import logging
import os
import subprocess
import thread
from pprint import pprint


def stringExactLen(txt, lenx):
    return str(str(txt) + '                                   ')[:lenx]


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        # d[column.name] = str(getattr(row, column.name))
        d[column.name] = getattr(row, column.name)

    return d


def getprintfilename(fileformat="printf-%s.txt"):
    if not os.path.exists(conf.cfg_trashpath):
        os.makedirs(conf.cfg_trashpath)
    now = datetime.datetime.now()
    dir = now.__format__('%y%m%d')
    dir = os.path.join(conf.cfg_trashpath, dir)
    if not os.path.exists(dir):
        os.makedirs(dir)
    file = timestampf()
    p = os.path.join(dir, fileformat % file)

    return os.path.abspath(p)


def timestamp():
    return datetime.datetime.now().__format__('%y%m%d-%H%M-%S')


def timestampf():
    return datetime.datetime.now().__format__('%y%m%d-%H%M-%S%f')


def espera(lck):
    raise 'espera/threads=obsoleto'
    def gett(lck):
        r = not lck.acquire(False)
        # logging.debug('gett - %s' % str(r))
        return r

    # logging.debug('espera - %s' % util.timestampf())
    t = lck.acquire()

    # logging.debug('travando - %s' % str(t))
    while 1 == 1 or 1 > 0:
        # logging.debug('WAITLOOP - %s' % timestampf())
        time.sleep(0.1)
        if not gett(lck):
            break


def canBeInt(s):
    try:
        int(s)
        return True
    except:
        return False


def isEquivalent(a, b):
    x = a if a else ''
    y = b if b else ''
    z = x == y
    return z

def isTuple(v):
    return type(v) == tuple
    return False

def isStr(v):
    return type(v)==str

def asstr(v):
    try:
        v= str(v)
    except:
        v=''
    return v

def noExcept():
    pass

def astext(v, limit=None, exact=None):
    if  isinstance(v , list):
        v = coal(v)
    try:
        if isinstance(v, unicode):
            pass
        elif isinstance(v, str):
            pass
        elif not v:
            v = ''
        else:
            v= str(v)
    except:
        noExcept()
        v=''
    if limit and len(v)>limit:
        exact = limit
    if exact:
        v = v + '                                   '
        return v[:exact]
    return v

def asInt(v):
    i = None
    try:
        # if not v is None:
        i = int(v)
    except:
        pass
    return i


def asDateTime(t, f=None):
    formats = [
        f,
        None,
        '%d/%m/%y',
        '%d/%m/%Y',
        '%d/%m/%y %H:%M',
        '%d/%m/%Y %H:%M',
        '%d-%m-%y',
        '%d-%m-%Y',
        '%d/%m/%y %H']
    d = None
    if type(t) in (str, unicode):
        for fx in formats:
            try:
                d = datetime.datetime.strptime(t, fx) if fx else  datetime.datetime.strptime(t)
                if d:
                    break
            except:
                pass

    return d


def asUnicode(sx):
    u = u''
    if not type(sx) in (tuple,list):
        s=[sx]
    else:
        s=sx
    for t in s:
        try:
            x = t.decode('utf-8')
            u = u + x
        except: 
            try:
                u = u + t
            except:
                u = u + '?'
    return u


def defaultv(a, b, c):
    if isinstance(a, dict):
        if b in a:
            if not a[b] is None:
                return a[b]

    if isinstance(a, tuple):
        if len(a) > b:
            if not a[b] is None:
                return a[b]

    if isinstance(a, list):
        if len(a) > b:
            if not a[b] is None:
                return a[b]
    return c


def defiter(a, b, c):
    if len(a) > b:
        if not a[b] is None:
            return a[b]
    return c


def dump(a, txt=None):
    if txt:
        print(txt)
    pprint(a)
    return


class pilha:
    def __init__(self):
        self.dados = []

    def empilha(self, elemento):
        self.dados.append(elemento)

    def desempilha(self):
        if not self.vazia():
            return self.dados.pop(-1)
        return None

    def vazia(self):
        return len(self.dados) == 0

    def topo(self):
        if not self.vazia():
            return self.dados[len(self.dados) - 1]
        else:
            return None


def paralelo(function, args=None):
    # Thread(target=function, args=tuple(args)).start()
    if not isinstance(args,tuple):
        args = ()
    return thread.start_new(function,args)
    pass


def getlogfilename(fileformat="log-%s.log"):
    if not os.path.exists(conf.cfg_trashpath):
        os.makedirs(conf.cfg_trashpath)
    now = datetime.datetime.now()
    dir = now.__format__('%y%m%d')
    dir = os.path.join(conf.cfg_trashpath, dir)
    if not os.path.exists(dir):
        os.makedirs(dir)
    file = timestampf()
    p = os.path.join(dir, fileformat % file)
    return os.path.abspath(p)

def coal(*args):
    ''' Retorno primeiro argumento válido, ou faz busca recursiva
    em objeto contido em tupla, seguido de seus atributos'''
    if len(args)==1 and  isinstance(args[0] , list):
        args=args[0]
    for arg in args:
        if arg:
            breakaway=0
            if isinstance(arg , tuple):
                d=arg[0]
                for v in arg[1:]:
                    try:
                        if v:
                            d = getattr(d, v)
                    except:
                        breakaway=1
                        break
                    if not d:
                        breakaway=1
                        break
                if breakaway or not d:
                    break
                return d
            else:
                return arg

class TerminalLogger(object):
    errinfo = ''
    logfile = None
    logstream = None

    def __init__(self, filename=None, iserr=False):
        if filename is None:
            if TerminalLogger.logfile is None:
                TerminalLogger.logfile = getlogfilename("stdout-%s.log")
            filename = TerminalLogger.logfile

        if TerminalLogger.logfile is None:
            TerminalLogger.logfile = filename

        TerminalLogger.logfile = os.path.abspath(TerminalLogger.logfile)

        self.terminal = sys.stdout
        self.filename = filename
        self.iserr = iserr
        self.log = None

    def PintOnScreen(self, txt):
        pass

    def write(self, message,a=0,b=0):
        # self.terminal.write(message)
        if self.log is None:
            self.log = open(self.filename, "a")

        self.log.write(message)
        self.log.flush()
        if self.iserr:
            TerminalLogger.errinfo = TerminalLogger.errinfo + message

    @staticmethod
    def setup():
        sys.stdout = TerminalLogger('log.log')  # todo
        sys.stderr = TerminalLogger(filename=TerminalLogger.logfile)  # , iserr=True)

        # import logging.handlers
        # logging.setLevel(logging.DEBUG)
        # handler = logging.handlers.SysLogHandler(address = '/dev/log')
        # logging.addHandler(handler)
        # logging.debug('this is debug')
        # logging.critical('this is critical')
        #TerminalLogger.logstream = open(TerminalLogger.logfile, "a")
        #logging.basicConfig(stream=TerminalLogger.TerminalLogger, level=logging.DEBUG)
        #logging.basicConfig(stream =sys.stderr, level=logging.DEBUG)
        logging.debug('''.*************************************.''')   

    @staticmethod
    def flush():
        try:
            if len(logging.root.handlers) > 0:
                logging.root.handlers[0].acquire()
                logging.root.handlers[0].flush()
        except:
            pass

    @staticmethod
    def showerr():
        # nisk.widgets.dlgInput.show('Erros!', TerminalLogger.errinfo)
        logging.debug('mostrado erro')
        TerminalLogger.errinfo = ''


def slen(txt):
    if txt is None:
        return 0;
    else:
        return len(txt)


def show(message, title='NeonGestor'):
    # import nisk
    # nisk.tui.mdi.dialog_ShowText(message, title)
    raise u'implementar uso com sessão'


def imprimeLPR(cfg_prntxt, var_prnfile):
    try:
        # cfg_prncmd_cyg = 'printer.sh %var_prnfile %cfg_prntxt'
        # cfg_prncmd_win = 'lpr -d %cfg_prntxt %var_prnfile'
        # cfg_prncmd_unix = 'cat $1 | smbclient $2 -c "print -" -N -U "nisk%000"'
        #
        cfg_prncmd_cyg = 'printer.sh %var_prnfile %cfg_prntxt'
        cfg_prncmd_win = 'copy %var_prnfile %cfg_prntxt'
        cfg_prncmd_unix = 'cat $1 | smbclient $2 -c "print -" -N -U "nisk%000"'

        if sys.platform == "win32":
            cmd = cfg_prncmd_win.replace('%cfg_prntxt', cfg_prntxt).replace('%var_prnfile', var_prnfile)
            x = subprocess.check_output(cmd, shell=True)

        else:
            cmd = conf.cfg_prncmd.replace('%cfg_prntxt', cfg_prntxt).replace('%var_prnfile', var_prnfile).split(' ')

            dump(['!!cmd!! ', cmd])
            p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            stdout, stderr = p1.communicate()

            if len(stdout) > 0:
                logging.debug('!!out!! ' + stdout)
            if len(stderr) > 0:
                logging.debug('!!out!! ' + stderr)

        '''
        import os
        os.name
        import platform
        platform.system()
        import sys
        sys.platform
        '''
    except:
        pass

def abreGestor():
    p1 = subprocess.Popen(["/home/dingo/neon/GESTOR.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p1.communicate()

    # print('Got stdout:', stdout)
    # print('Got stderr:', stderr)

    if len(stdout) > 0:
        logging.debug('!!out!! ' + stdout)
    if len(stderr) > 0:
        logging.debug('!!out!! ' + stderr)
