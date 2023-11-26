# importing QT libraries 
from PyQt5.QtWidgets import * 
from PyQt5 import QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5 import uic
from PyQt5.QtCore import Qt

import os
from shared import Utils
from qtwindow import MainWindow

utils = Utils()

# 1> get pwd > load vex file > create list of snippets

install_dir = os.getcwd()
vex_file:str = f"{install_dir}/vex.c"
ui_file:str = f"{install_dir}/snipfuzz.ui"

# inject those snippets 
snippets_list = utils.get_snippet_list(vex_file)
# utils.snippets = my_snippets_list



# utils.test()
# utils.update_text("POP")


# print(my_snippets_list)

# test the fuzzy_search fn
# search = "point"
# string = "list of poin t s 2"
# match_ratio = utils.fuzzy_search(search,string)
# print(match_ratio)
#
# text_with_hashtags = "//#houdini #vex #search"
# print(text_with_hashtags)
# text_without_hashtags =utils.keep_hashtags_only(text_with_hashtags)
# print(text_without_hashtags)

# 2> create QtWindow
app = QApplication([])
window = MainWindow(ui_file)

# e = window.keyPressEvent
# print(">>>" , e)

# def jo(self, e):
#     if e.key() == Qt.Key_Up:
#         self.snippet_index +=1
#     elif e.key() == Qt.Key_Down:
#         self.snippet_index -=1
#     # Validate search result with Ctrl key
#     elif e.key() == Qt.Key_Control:
#         self.close()

#     print(self.snippet_index)

# # keyPressEvent(window,e)
# window.keyPressEvent = jo()




window.ui.text.setText("POPPPPAP")

# window.ui.textfield.textChanged.connect(utils.textchanged)
window.show()
# utils.ui = window.ui



app.exec_()


