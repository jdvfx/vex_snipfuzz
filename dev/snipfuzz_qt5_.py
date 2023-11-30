# houdini imports
# import hou
# from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui
# from PySide2.QtGui import QFont
# from PySide2.QtCore import Qt

# importing QT libraries 
from PyQt5.QtWidgets import * 
from PyQt5 import QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5 import uic
from PyQt5.QtCore import Qt

import re 
import os
from typing import List,Tuple



# self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)

import re
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

app = QApplication([])

# class SnipFuzz(QtWidgets.QWidget):
class MainWindow(QMainWindow):

    # def __init__(self, wrangle, install_dir:str):
    # def __init__(self,*args,**kwargs,install_dir:str):
    def __init__(self,install_dir:str,*args,**kwargs):
        # super(SnipFuzz,self).__init__()
        super(MainWindow, self).__init__(*args,**kwargs)

        self.search_mode = SearchMode.fuzzy
        self.case_sensitive = CaseSensive.lower
        # self.wrangle = wrangle

        ui_file = f"{install_dir}/snipfuzz.ui"
        # self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
        self.ui = uic.loadUi(ui_file, self) # Load the .ui file
        
        self.input_char_list:List[str] = []
        self.snippet_index:int = 0
        vex_file:str = f"{install_dir}/vex.c"
        self.file = vex_file
        self.snippets:List[str] = self.get_snippet_list()

        # set font and style        
        text_style  = 'background-color: #161616; color: #aaaaaa; padding: 7px;'
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setStyleHint(QFont.Monospace)
            
        self.ui.textfield.textChanged.connect(self.textchanged)
        self.ui.setStyleSheet("background-color: #000000;") 
        self.ui.text.setStyleSheet(text_style)
        self.ui.text.setFont(font)
        self.ui.textfield.setStyleSheet(text_style)
        self.ui.textfield.setFont(font)
        self.ui.status.setStyleSheet(text_style)
        self.ui.status.setFont(font)

        # self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        
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
    """
    search for letters in string and return number of matches
    basic 'FZF like' fuzzy search
    """
            
    def fuzzy_search(self, search, string) -> float:
    
        if self.search_mode == SearchMode.hashtag:
            string = self.keep_hashtags_only(string)
    
        s = search
        l = string
        li = 0
        si = 0

        match_score = 0.0
        last_match_index = 0
        letters_found = 0

        while li<len(l) and si<len(s):
            s_ = s[si]
            l_ = l[li]

            if s_==l_:
                letters_found += 1
                si += 1
                li+=1
                dist = abs(last_match_index-li)
                match_score += 1/float(dist)
                last_match_index = li
            else:
                li+=1
        if letters_found<len(search):
            return 0.0
        else:
            return match_score
            
    # ----------------------------------------------------------
    """ keep only hastags in the block of text """
    def keep_hashtags_only(self,text:str) -> str:
        hashtags = ""
        lines = text.split("\n")
        for line in lines:
            if line.startswith("//") and "#" in line:
                filtered = list(filter(lambda b: b.startswith("#"), line.split(" ")))
                h = " ".join(filtered)
                h = re.sub("#","",h)
                hashtags = h
        return hashtags
        
    # ----------------------------------------------------------
    """ fuzzy search in snippet lines, return list of snippets """
    def search_snippets(self,search_string) -> List[Tuple[float,int]]:
    
        search_results = []
        
        if len(search_string)==0:
            return search_results

        for idx,snippet in enumerate(self.snippets):

            if self.case_sensitive == CaseSensive.lower:
                search_string = search_string.lower()
                
            match_score = self.fuzzy_search(search_string,snippet)

            if match_score>0:
                result:Tuple[float,int] = (match_score,idx)
                search_results.append(result)

        search_results.sort(reverse=True)


        return search_results        
        

    # ----------------------------------------------------------      
    """
    up/down: cycle through found snippets
    alt: fuzzy or hashtag search mode
    shift: toggle case sensitive search (default=ignore case)
    ctrl: select current snippetm, copy to wrangle node
    """
    def keyPressEvent(self, e):
    
        key_actions = {
            Qt.Key_Up: lambda: setattr(self, 'snippet_index', self.snippet_index - 1),
            Qt.Key_Down: lambda: setattr(self, 'snippet_index', self.snippet_index + 1),
            Qt.Key_Alt: lambda: setattr(self, 'search_mode', SearchMode.hashtag if self.search_mode is SearchMode.fuzzy else SearchMode.fuzzy),
            Qt.Key_Shift: lambda: setattr(self, 'case_sensitive', CaseSensive.lower if self.case_sensitive is CaseSensive.upperlower else CaseSensive.upperlower),
            Qt.Key_Return: lambda: (self.wrangle.parm("snippet").set(self.ui.text.text()), self.close()),
            Qt.Key_Control: lambda: (self.wrangle.parm("snippet").set(self.ui.text.text()), self.close()) #duplicate, might remove later
        }

        action = key_actions.get(e.key())
        if action:
            action()
        
        self.update_text(self.ui.textfield.displayText())

    # ----------------------------------------------------------
    def update_text(self,text):
    
        results:List[Tuple[float,int]] = self.search_snippets(text)

        case = "A" if self.case_sensitive == CaseSensive.upperlower else "a"
        search_mode = "fuzzy" if self.search_mode == SearchMode.fuzzy else "#"
        s = f"{search_mode} {case}"
        
        if len(results)>0:
            self.snippet_index:int = min(max(0,self.snippet_index),len(results)-1)
            current_snippet = self.snippets[results[self.snippet_index][1]]
            self.ui.text.setText(current_snippet)
            match = results[self.snippet_index][0]

            s = f"{s}  {self.snippet_index+1}/{len(results)}    match:{match:.2f}"

        self.ui.status.setText(s)

    def textchanged(self,text):
        self.update_text(text)

# ----------------------------------------------------------
# """
# what wrangle node we want ot paste the code to:
# is it selected?
# is the display flag on?
#
# """
# def find_wrangle():
#
#     for node in hou.selectedNodes():
#         if node.type().name().endswith("wrangle"):
#             return node
#             
#     sop_wrangle_types = ["attribwrangle","volumewrangle"]
#     for sop_wrangle_type in sop_wrangle_types:
#         for node in hou.sopNodeTypeCategory().nodeTypes()[sop_wrangle_type].instances():
#             if node.isDisplayFlagSet():
#                 # select this node so we can see the wrangle text being updated
#                 node.setSelected("on",clear_all_selected=True)
#                 return node

# ----------------------------------------------------------
"""
where the 'snipfuzz.ui' and 'vex.c' files are located

"""
install_dir = os.getcwd()
print(install_dir)

# wrangle = find_wrangle()
# if wrangle is not None:
#     dialog = SnipFuzz(wrangle,install_dir)
#     dialog.show()
# else:
#     hou.ui.displayMessage("Please select a wrangle node")

# wrangle = ""
# dialog = SnipFuzz(wrangle,install_dir)
# dialog = SnipFuzz(install_dir)
window = MainWindow(install_dir)
window.show()

# Start the event loop.
app.exec_()



