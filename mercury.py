#!/usr/bin/python

from subsystem import init_sub
from subsystem import take_screenshot
import sys, getopt

def handle_args(argv):
    try:
        opts, args = getopt.getopt(argv, "s", ["square"])
    except getopt.GetoptError:
        print 'improper usage!'
        return -1
    for opt, arg in opts:
        if opt in ("-s", "--square"):
            return 1
        else:
            return -1
        
if __name__ == '__main__':
    init_sub()
    command = handle_args(sys.argv[1:])
    if command == 1:
        take_screenshot()

