# importing libraries 
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5 import uic

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
        self.snippets:List[str] = self.get_snippet_list()

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
        self.textfield.textChanged.connect(self.textchanged)
        self.setStyleSheet("background-color: #000000;") 
        self.text.setStyleSheet(text_style)
        self.text.setFont(font)
        self.textfield.setStyleSheet(text_style)
        self.textfield.setFont(font)
        self.status.setStyleSheet(text_style)
        self.status.setFont(font)

    # ----------------------------------------------------------
    def keyPressEvent(self, e):
            if e.key() == QtCore.Qt.Key_Up:
                self.snippet_index +=1
            elif e.key() == QtCore.Qt.Key_Down:
                self.snippet_index -=1
            # Validate search result with Ctrl key
            elif e.key() == QtCore.Qt.Key_Control:
                self.close()
                # self.wrangle.parm("snippet").set(self.text.text())
                
            self.update_text(self.textfield.displayText())

    # ----------------------------------------------------------
    def update_text(self,text):
        results:List[Tuple[float,int]] = self.search(text)

        s = ""
        if len(results)>0:

            self.snippet_index:int = min(max(0,self.snippet_index),len(results)-1)
            current_snippet = self.snippets[results[self.snippet_index][1]]
            self.text.setText(current_snippet)

            for i in range(len(self.snippets)):
                inlist = False
                for idx,j in enumerate(results):
                    if j[1] == i:
                        inlist = True
                        if idx == self.snippet_index:
                            s+="#"
                        else:
                            s+="|"
                        break

                if not inlist:
                    s+="."

            s += f" {self.snippet_index}"

        self.status.setText(s)

    def textchanged(self,text):
        self.update_text(text)

    # ----------------------------------------------------------
    """ split file by separators containing dashes """
    def get_snippet_list(self) -> List[str]:

        with open(self.file,"r") as file:
            lines = file.read().splitlines()

        snippets:list[str] = []
        snip_lines:str = ""
        for line in lines:
            if "-----" not in line:
                snip_lines += f"{line}\n"
            else:
                snippets.append(snip_lines)
                snip_lines = ""
        if len(snip_lines)>0:
            snippets.append(snip_lines)

        return snippets

    # ----------------------------------------------------------
    """ fuzzy search in snippet lines, return list of snippets """
    def search(self,search_string) -> List[Tuple[float,int]]:
        if len(search_string)==0:
            return []
        search_results = []
        for idx,snippet in enumerate(self.snippets):
            # if the search string is literally inside the snippet, prioritize it 
            if search_string in snippet:
                ratio = 2.0
                result:Tuple[float,int] = (ratio,idx)
                search_results.append(result)
            else:
                alpha = re.sub('[^a-za-z]+', ' ', snippet) # alpha only
                words_ = alpha.split(' ')
                words_ = [x for x in words_ if x != ''] # remove empty elements
                words = list(set(words_)) # remove duplicates
                
                # basic fuzzy search with difflib
                for word in words:
                    ratio:float = difflib.SequenceMatcher(None,search_string,word).ratio()
                    if ratio>0.5:
                        result:Tuple[float,int] = (ratio,idx)
                        search_results.append(result)
                        break
        #
        search_results.sort(reverse=True)
        return search_results

window = MainWindow()
window.show()

# Start the event loop.
app.exec_()

