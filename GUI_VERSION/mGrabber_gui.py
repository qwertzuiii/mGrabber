import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from PyQt5 import uic, QtWidgets, QtGui, QtCore
from skingrabber import skingrabber
from res.modules import phasto as psto
from res.image import resources
from PyQt5 import QtTest
sking = skingrabber()
somedeb = False

PATH_TO_CONFIGFILE = 'res/config.json'
PATH_TO_RENDER = 'res/image/skin_render_new.png'

cfg = psto.file.read_json(PATH_TO_CONFIGFILE)


class MainApp(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(cfg['ui'], self)  # ui file load
        self.setWindowIcon(QtGui.QIcon(cfg['icon']))  # Icon Loading
        self.setWindowTitle(' ')

        self.pixmap = QtWidgets.QGraphicsPixmapItem()

        self.activeUser = ""
        self.renderLink = ""
        self.ProgressDef = "Idle..."

        self.CURSOR_DEFAULT = QtGui.QCursor(QtCore.Qt.ArrowCursor)
        self.CURSOR_POINTING = QtGui.QCursor(QtCore.Qt.PointingHandCursor)

        self.Progress.setText(self.ProgressDef)
        self.versionText.setText('v' + str(cfg['version']))

        self.btn_grab.clicked.connect(self.grab_skin)
        self.btn_saveskin.clicked.connect(self.download_skin)

        if cfg['clickableSkin'] == True:
            self.skinimg.mousePressEvent = self.linkOpen
            self.skinimg.setCursor(self.CURSOR_POINTING)
        else:
            self.skinimg.setCursor(self.CURSOR_DEFAULT)

        if somedeb:
            print(self.skinimg.mousePressEvent)

        if cfg['buttoncursor'] == True:
            self.btn_grab.setCursor(self.CURSOR_POINTING)
            self.btn_saveskin.setCursor(self.CURSOR_POINTING)
        else:
            self.btn_grab.setCursor(self.CURSOR_DEFAULT)
            self.btn_saveskin.setCursor(self.CURSOR_DEFAULT)

    def sleep(self, i):
        QtTest.QTest.qWait(i)
    
    def grab_skin(self):
        try:
            user = self.getname.text()
            skin_render = sking.get_skin_rendered(user)
            req_render = psto.web.getcontent(skin_render)
        except:
            print('<mGrabber> No player found')
            self.Progress.setText('No player Found')
            self.sleep(2000)
            self.Progress.setText(self.ProgressDef)
            return
        
        
        psto.file.write_bytes(PATH_TO_RENDER, req_render)

        img = QtGui.QPixmap(PATH_TO_RENDER)
        self.skinimg.setPixmap(img)
        self.renderLink = skin_render
        self.activeUser = user
        print(f'<mGrabber> {user} found!')
        self.Progress.setText(user + ' found!')

        try:
            os.remove(PATH_TO_RENDER)
        except: pass
        
        self.sleep(2000)
        self.Progress.setText(self.ProgressDef)

    def download_skin(self):
        if self.activeUser == "":
            print('<mGrabber> No grabbed Player')
            self.Progress.setText('No grabbed Player')
            self.sleep(2000)
            self.Progress.setText(self.ProgressDef)
            return

        skin = sking.get_skin(self.activeUser)
        req = psto.web.getcontent(skin)

        psto.file.write_bytes(cfg['skin_output'] + '/' + self.activeUser + '.png', req)

        print('<mGrabber> Grabbed Player (%s) saved!' % self.activeUser)
        self.Progress.setText('%s saved!' % self.activeUser)

        self.sleep(2000)
        self.Progress.setText(self.ProgressDef)

    def linkOpen(self, event):
        if self.renderLink != "":
            psto.web.open(self.renderLink)
        else:
            print('<mGrabber> Cant open link')
            self.Progress.setText("Can't open link")

            self.sleep(2000)
            self.Progress.setText(self.ProgressDef)

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    appMain = MainApp()
    appMain.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Exiting...')