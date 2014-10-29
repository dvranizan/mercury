#!/usr/bin/python

import logging
import threading
import thread
import os
from math import fabs
from mouse import initMouseAndGetSquare
from mouse import initInputKeyboard
from capture import screengrab
from copybuf import add_http_path_to_clipboard
import global_values

def convert_to_offset(b):
    temp = [-1,-1,-1,-1]
    temp[0] = (b[0] if b[0] < b[2] else b[2])
    temp[1] = (b[1] if b[1] < b[3] else b[3])
    temp[2] = abs(b[0] - b[2])
    temp[3] = abs(b[1] - b[3])
    return temp

class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)

def init_sub():
    # setup logging
    logging.basicConfig(level=logging.DEBUG)

    # Hardset set save dir
    # TODO: Generalize this routine, allow for init via config
    global_values.set_base_file_path("/home/david/clipdump")
    global_values.set_base_http_path("http://subsonic.brewpdx.org/clipdump")

def take_screenshot():
    # user wants screencap, listen to mouse and get
    logging.debug("Initing mouse thread...")
    window = initMouseAndGetSquare()
    b = convert_to_offset(global_values.box)
    # grab a file name
    filename = global_values.get_file_path()
    logging.info("Grabbing screencap box at:"+str(b))
    logging.info("Init fb grab, storing at "+str(filename)+" ...")
    s = screengrab(b[0],b[1],b[2],b[3], filename, window)
    screen = s.screen()
    if (screen):
        # success! put file path in buffer
        add_http_path_to_clipboard(global_values.get_http_path(filename))
        logging.debug("File saved at "+str(screen))
    else:
        logging.debug("Screen save failed")
    del screen

if __name__ == '__main__':
    # setup logging
    logging.basicConfig(level=logging.DEBUG)

    # set save dir
    # TODO - This needs to be generalized and moved into init routine
    global_values.set_base_file_path("/home/david/clipdump")
    global_values.set_base_http_path("http://subsonic.brewpdx.org/clipdump")
    # create event for triggering of screen grab
    #keyboardEvent = threading.Event()
    mouseEvent = threading.Event()
    #keyboardEvent.clear()
    mouseEvent.clear()
    
    logging.info("Init kb/m monitor...")
    #inputMouseThread = FuncThread(initMouseAndGetSquare, mouseEvent)
    #inputKeyboardThread = FuncThread(initInputKeyboard, keyboardEvent)
    #inputMouseThread.start()
    #inputKeyboardThread.start()

    # wait for event trigger
    while(1):
        #keyboardEvent.wait()
        # user wants screencap, listen to mouse and get
        logging.debug("Initing mouse thread...")
        window = initMouseAndGetSquare(mouseEvent)
        b = convert_to_offset(global_values.box)
        # grab a file name
        filename = global_values.get_file_path()
        logging.info("Grabbing screencap box at:"+str(b))
        logging.info("Init fb grab, storing at "+str(filename)+" ...")
        #keyboardEvent.clear()
        s = screengrab(b[0],b[1],b[2],b[3], filename, window)
        screen = s.screen()
        if (screen):
            # success! put file path in buffer
            add_http_path_to_clipboard(global_values.get_http_path(filename))
            logging.debug("File saved at "+str(screen))
        else:
            logging.debug("Screen save failed")
        del screen
