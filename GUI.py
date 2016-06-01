import os
import sys
import cherrypy
from PyQt4 import QtGui, QtCore,QtWebKit,QtScript



def Init_Server():
    PATH = os.path.abspath(os.path.dirname(__file__))
    class Root(object): pass

    logger = cherrypy.log.access_log
    logger.removeHandler(logger.handlers[0])

    cherrypy.tree.mount(Root(), '/', config={
            '/': {
                    'tools.staticdir.on': True,
                    'tools.staticdir.dir': PATH+'/GUI',
                    'tools.staticdir.index': 'index.html',
                },
        })

    cherrypy.engine.start()
    return



def Init_GUI():

    app = QtGui.QApplication(sys.argv)
    browser = QtWebKit.QWebView()
    browser.setGeometry(0,0,1080,720)
    browser.setWindowTitle("ADS-B Decoder")
    browser.load(QtCore.QUrl('http://127.0.0.1:8080'))
    browser.show()

    sys.exit(app.exec_())
 