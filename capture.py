#!/usr/bin/env python
# encoding: utf-8
"""
screengrab.py

Created by Alex Snet on 2011-10-10.
Copyright (c) 2011 CodeTeam. All rights reserved.
"""

import sys
import os
import Image
import logging
import global_values

class screengrab:
    def __init__(self, x1, y1, x2, y2, fn, w):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.filename = fn
        self.window = w

        try:
            import gtk
        except ImportError:
            pass
        else:
            logging.debug("Capturing screen using GTK")
            self.screen = self.getScreenByGtk
            #logging.debug("Capturing screen using QT")
            #self.screen = self.getScreenByQt

    def getScreenByGtk(self):
        import gtk.gdk      
        #w = gtk.gdk.get_default_root_window()
                             
        if (self.x1 <= 0):
            # use entire screen
            sz = w.get_size()
            self.x1 = 0
            self.y1 = 0
            self.x2 = sz[0]
            self.y2 = sz[1]
        pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,self.x2,self.y2)
        pb = pb.get_from_drawable(self.window,self.window.get_colormap(),self.x1,self.y1,0,0,self.x2,self.y2)
        if (pb != None):
            logging.debug("Saving screenshot as "+self.filename)
            pb.save(self.filename,"png")

        return self.filename

    def getScreenByQt(self):
        from PyQt4.QtGui import QPixmap, QApplication
        from PyQt4.Qt import QBuffer, QIODevice, QFile
        import StringIO
        logging.debug("In QT grab...")
        if not global_values.app:
            # init QT app for captuer
            global_values.app = QApplication(sys.argv)
        f = QFile(self.filename)
        f.open(QIODevice.WriteOnly)
        logging.debug("QT opened file...")
        #buffer = QBuffer()
        #buffer.open(QIODevice.ReadWrite)
        QPixmap.grabWindow(QApplication.desktop().winId(),self.x1,self.x2,self.y1,self.y2).save(f, 'png')
        logging.debug("QT grabbed window...")
        f.close()
        del f
        #strio = StringIO.StringIO()
        #strio.write(buffer.data())
        #buffer.close()
        #strio.seek(0)
        #return Image.open(strio)
        return self.filename

    def getScreenByPIL(self):
        import ImageGrab
        img = ImageGrab.grab()
        return img

    def getScreenByWx(self):
        import wx
        wx.App()  # Need to create an App instance before doing anything
        screen = wx.ScreenDC()
        size = screen.GetSize()
        bmp = wx.EmptyBitmap(size[0], size[1])
        mem = wx.MemoryDC(bmp)
        mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
        del mem  # Release bitmap
        #bmp.SaveFile('screenshot.png', wx.BITMAP_TYPE_PNG)
        myWxImage = wx.ImageFromBitmap( myBitmap )
        PilImage = Image.new( 'RGB', (myWxImage.GetWidth(), myWxImage.GetHeight()) )
        PilImage.fromstring( myWxImage.GetData() )
        return PilImage

if __name__ == '__main__':
    s = screengrab(-1,-1,-1,-1)
    screen = s.screen()
    screen.show()
