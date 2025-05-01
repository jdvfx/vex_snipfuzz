# importing libraries 
import PyQt5
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
from PyQt5 import uic


import json

import re
import difflib
from typing import List,Tuple

# >> QApplication holds the event loop
# app = QApplication(sys.argv)

# if we don't pass any cli args to the app, can pass empty array
app = QApplication([])

class MainWindow(QMainWindow):

    def __init__(self,*args,**kwargs):
        super(MainWindow, self).__init__(*args,**kwargs)

        self.input_char_list:List[str] = []
        self.snippet_index:int = 0
        vex_file:str = "/home/bunker/projects/python/vex_snipfuzz/vex.c"
        self.file = vex_file
        # self.snippets:List[str] = self.get_snippet_list()
    
        d = {}
        json_file = "data.json"
        with open(json_file) as f:
            d = json.load(f)

        self.snippets:List[dict] = d

        # set font and style
        cascadia_available = True

        text_style  = 'background-color: #161616; color: #aaaaaa; padding: 7px;'
        font = QtGui.QFont()
        font.setPointSize(10)
        if cascadia_available:
            font.setFamily("Cascadia Mono")
        else:
            font.setBold(True)
            font.setStyleHint(QFont.Monospace)

        uic.loadUi("snipfuzz.ui",self)
        self.textfield.textChanged.connect(self.update_text)
        self.setStyleSheet("background-color: #000000;") 
        self.text.setStyleSheet(text_style)
        self.text.setFont(font)
        self.textfield.setStyleSheet(text_style)
        self.textfield.setFont(font)
        self.status.setStyleSheet(text_style)
        self.status.setFont(font)

        self.update_text()

    # ----------------------------------------------------------
    def keyPressEvent(self, e):
            if e.key() == Qt.Key_Up:
                self.snippet_index +=1
            elif e.key() == Qt.Key_Down:
                self.snippet_index -=1
            elif e.key() == Qt.Key_Control:
                self.close()

    # ----------------------------------------------------------
    def update_text(self):
        
        input_text = self.textfield.displayText()

        # search string empty, return all snippets
        snippet_matches=self.snippets

        if input_text!="":
            # search snippets for a String
            # create list of matching snippets
            snippet_matches=[]
            for snippet in self.snippets:
                # for k,v in snippet.items():
                for v in snippet.values():
                    if input_text in v:
                        snippet_matches.append(snippet)
                        break

        # update button list
        self.mylist.clear()
        for match in snippet_matches:
            name = match.get("name")
            if name:
                i = PyQt5.QtWidgets.QListWidgetItem()
                i.setText(name)
                self.mylist.addItem(i)

        self.mylist.itemClicked.connect(self.textclick)

        # self.text.setText(out_string)

    def textclick(self,item):
        text = item.text()
        self.text.setText(text)






window = MainWindow()
window.show()

# Start the event loop.
app.exec_()

