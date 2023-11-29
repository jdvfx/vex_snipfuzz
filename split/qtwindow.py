# importing QT libraries 
from PyQt5.QtWidgets import * 
from PyQt5 import QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5 import uic
from PyQt5.QtCore import Qt

from typing import List,Tuple
from enum import Enum

class SearchMode(Enum):
    fuzzy = 0
    hashtag = 1
    exactmatch = 2

# TODO: implement exact match
# use the Alt key to toggle between 3 search modes

class CaseSensive(Enum):
    upperlower = 0
    lower = 1
class MainWindow(QMainWindow):

    # def __init__(self, wrangle, install_dir:str):
    # def __init__(self,*args,**kwargs,install_dir:str):
    def __init__(self,ui_file:str,*args,**kwargs):
        # super(SnipFuzz,self).__init__()

        super(MainWindow, self).__init__(*args,**kwargs)

        self.search_mode = SearchMode.fuzzy
        self.case_sensitive = CaseSensive.lower
        self.snippet_index:int = 0

        # # self.wrangle = wrangle
        #
        # ui_file = f"{install_dir}/snipfuzz.ui"
        # self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.ui = uic.loadUi(ui_file, self) # Load the .ui file
        # 
        # self.input_char_list:List[str] = []
        # vex_file:str = f"{install_dir}/vex.c"
        # self.file = vex_file
        # self.snippets:List[str] = self.get_snippet_list()
        #
        # set font and style        
 

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Up:
            self.snippet_index +=1
        elif e.key() == Qt.Key_Down:
            self.snippet_index -=1
        # Validate search result with Ctrl key
        elif e.key() == Qt.Key_Control:
            self.close()
            # self.wrangle.parm("snippet").set(self.text.text())
                
        t = f"{self.snippet_index}"
        self.ui.status.setText(t)
        
            # self.update_text(self.textfield.displayText())
