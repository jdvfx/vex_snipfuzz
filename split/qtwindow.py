
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

        # set font and style        
        text_style  = 'background-color: #161616; color: #aaaaaa; padding: 7px;'
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setStyleHint(QFont.Monospace)
        #     
        self.ui.textfield.textChanged.connect(self.textchanged)
        self.ui.setStyleSheet("background-color: #000000;") 
        self.ui.text.setStyleSheet(text_style)
        self.ui.text.setFont(font)
        self.ui.textfield.setStyleSheet(text_style)
        self.ui.textfield.setFont(font)
        self.ui.status.setStyleSheet(text_style)
        self.ui.status.setFont(font)

        self.utils = Utils(vex_file)

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
