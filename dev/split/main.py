from PyQt5.QtWidgets import QApplication # QT #

import os
from qtwindow import MainWindow 
from shared import Utils

install_dir = os.getcwd()
vex_file:str = f"{install_dir}/vex.c"
ui_file:str = f"{install_dir}/snipfuzz.ui"

app = QApplication([]) # QT #
window = MainWindow(ui_file,vex_file)


window.show()
app.exec_()


# >>> 
# import hou
# from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui
# from PySide2.QtGui import QFont
# from PySide2.QtCore import Qt
#
# install_dir = "/home/bunker/Desktop/git/vex_snipfuzz/"
#
# class SnipFuzz(QtWidgets.QWidget):
#     def __init__(self, install_dir:str):
#         super(SnipFuzz,self).__init__()
#         ui_file = f"{install_dir}/snipfuzz.ui"
#         self.ui = QtUiTools.QUiLoader().load(ui_file, parentWidget=self)
#         self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
#         
# dialog = SnipFuzz(install_dir)
# dialog.show()
#


