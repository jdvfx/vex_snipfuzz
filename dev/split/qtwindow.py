# importing QT libraries 
from PyQt5.QtWidgets import * 
from PyQt5 import QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5 import uic
from PyQt5.QtCore import Qt

from shared import Utils

class MainWindow(QMainWindow):
    def __init__(self,ui_file:str,vex_file:str,*args,**kwargs):

        super(MainWindow, self).__init__(*args,**kwargs)

        self.ui = uic.loadUi(ui_file, self) # Load the .ui file

        self.utils = Utils(vex_file)
        self.textfield.textChanged.connect(self.textchanged)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Up:
            self.utils.snippet_index +=1
        elif e.key() == Qt.Key_Down:
            self.utils.snippet_index -=1
        elif e.key() == Qt.Key_Control:
            self.close()

        text = self.ui.textfield.displayText()
        self.textchanged(text)

    def textchanged(self,text):
        (text,status) = self.utils.update_text(text)
        self.ui.status.setText(status)
        self.ui.text.setText(text)
