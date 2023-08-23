from PySide2 import QtCore
from PySide2 import QtWidgets

import re
import difflib
from typing import List,Tuple

class SnipFuzz(QtWidgets.QWidget):

    def __init__(self, wrangle, file:str):
        QtWidgets.QWidget.__init__(self)

        self.wrangle = wrangle
        self.resize(300,300)

        self.input_char_list:List[str] = []
        self.snippet_index:int = 0
        self.file:str = file
        self.snippets:List[str] = self.get_snippet_list()
        #
        self.textfield = QtWidgets.QLineEdit()
        self.textfield.textChanged.connect(self.textchanged)
        #
        self.text = QtWidgets.QLabel("-")
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.text)
        layout.addWidget(self.textfield)
        self.setLayout(layout)
        self.show()
        
    # ----------------------------------------------------------
    def keyPressEvent(self, e):
            if e.key() == QtCore.Qt.Key_Up:
                self.snippet_index +=1
            elif e.key() == QtCore.Qt.Key_Down:
                self.snippet_index -=1
            # Validate search result with Ctrl key
            elif e.key() == QtCore.Qt.Key_Control:
                self.wrangle.parm("snippet").set(self.text.text())
                self.close()
                
            self.update_text(self.textfield.displayText())

    # ----------------------------------------------------------
    def update_text(self,text):
        results:List[Tuple[float,str]] = self.search(text)
        if len(results)>0:
            self.snippet_index:int = min(max(0,self.snippet_index),len(results)-1)
            current_snippet = results[self.snippet_index][1]
            self.text.setText(current_snippet)

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
    def search(self,search_string) -> List[Tuple[float,str]]:
        search_results = []
        for snippet in self.snippets:
            # if the search string is literally inside the snippet, prioritize it 
            if search_string in snippet:
                ratio = 2.0
                result:Tuple[float,str] = (ratio,snippet)
                search_results.append(result)
            else:
                alpha = re.sub('[^a-za-z]+', ' ', snippet) # alpha only
                words_ = alpha.split(' ')
                words_ = [x for x in words_ if x != ''] # remove empty elements
                words = list(set(words_)) # remove duplicates

                for word in words:
                    ratio:float = difflib.SequenceMatcher(None,search_string,word).ratio()
                    if ratio>0.8:
                        result:Tuple[float,str] = (ratio,snippet)
                        search_results.append(result)
                        break
        #
        search_results.sort(reverse=True)
        return search_results

    
def find_wrangle():
    for node in hou.selectedNodes():
        if node.type().name().endswith("wrangle"):
            return node

# YOUR text file containing VEX snippets (separated by lines with dashes -----)
vex_file:str = "/home/bunker/projects/vex_snipfuzz/vex.c"

wrangle = find_wrangle()
if wrangle is not None:
    dialog = SnipFuzz(wrangle,vex_file)
    dialog.show()

