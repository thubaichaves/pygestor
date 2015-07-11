#!/usr/bin/env python
# lpstat.py - jbauer at rubic.com

import os, socket, sys

def lpstat(host, printer):
    s = socket.gethostbyname(host)
    fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fd.bind(('0.0.0.0', 855))
    fd.connect((s, 515))
    str = '\003%s\n' % printer
    fd.send(str, 0)
    return fd.recv(2048, 0)



if __name__ == '__main__':
    usage = "usage: %s host printer" % os.path.basename(sys.argv[0])
    if len(sys.argv) < 3:
        print usage
    else:
        print lpstat(sys.argv[1], sys.argv[2])