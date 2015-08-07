# try:

import sys
sys.path.append('/lib/python2.7/site-packages/pycharm-debug.egg')
# from pydev import pydevd

import pydevd

pydevd.settrace('localhost', port=2222, stdoutToServer=True, stderrToServer=True)
import run
# except:
#     pass
