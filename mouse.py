import logging
from threading import Event
from Xlib.display import Display
from Xlib import X
import gtk.gdk
from pymouse import PyMouseEvent
from pykeyboard import PyKeyboardEvent
import global_values

class listenToMouse(PyMouseEvent):
    def __init__(self):
        PyMouseEvent.__init__(self)
        self.x_click_down = -1
        self.y_click_down = -1
        self.x_click_up = -1
        self.y_click_up = -1

    def move(self, x, y):
        pass

    def click(self, x, y, button, press):
        if press:
            logging.info('{ "event": "click", "type": "press", "x": "' + str(x) + '", "y": "' + str(y) + '"}')
            self.x_click_down = x
            self.y_click_down = y
        else:
            logging.info('{ "event": "click", "type": "release", "x": "' + str(x) + '", "y": "' + str(y) + '"}') 
            self.x_click_up = x
            self.y_click_up = y
            global_values.box = self.getLoc()
            logging.debug("Mouse box set to: "+str(global_values.box))
            self.stop()
            self.stop()
    
    def getLoc(self):
        return [self.x_click_down, self.y_click_down,self.x_click_up, self.y_click_up]


    
class listenToKeys(PyKeyboardEvent):
    def __init__(self, ev):
        PyKeyboardEvent.__init__(self)
        self.cntl = False;
        self.event = ev

    def key_press(self, key):
        #logging.debug("Key press"+str(key))
        if (key == 37):
            """cntl is pressed"""
            self.cntl = True
        elif (key == 13):
            """screenshot time?"""
            if (self.cntl):
                logging.info("Detect request for screengrab")
                self.event.set()
            
    def key_release(self, key):
        if (key == 37):
            """cntl is released"""
            self.cntl = False

def initMouseAndGetSquare():
    """ init gtk window and grab mouse """
    w = gtk.gdk.get_default_root_window()
    """change cursor"""
    cursor = gtk.gdk.Cursor(gtk.gdk.CROSSHAIR)
    gtk.gdk.pointer_grab(w, 
                         False,
                         0,
                         None,
                         cursor, 
                         0)
    """ first grab all mouse events """
    display = Display(':0')
    root = display.screen().root
    root.grab_pointer(True, X.ButtonPressMask | X.ButtonReleaseMask, X.GrabModeAsync, X.GrabModeAsync, 0, 0, X.CurrentTime)
    mouse_handle = listenToMouse()
    mouse_handle.run()
    display.close()
    """release mouse"""
    gtk.gdk.pointer_ungrab()
    del display
    return w


def initInputMouse(ev):
    mouse_handle = listenToMouse(ev)
    logging.debug("Initing mouse...")
    mouse_handle.run()

def initInputKeyboard(ev):
    key_handle = listenToKeys(ev)
    logging.debug("Initing keyboard...")
    key_handle.run()

if __name__ == '__main__':
    key_handle = listenToKeys()
    mouse_handle = listenToMouse()
    key_handle.run()
    mouse_handle.capture = False
    mouse_handle.daemon = False
    mouse_handle.start()

