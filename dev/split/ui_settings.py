text_style  = 'background-color: #161616; color: #aaaaaa; padding: 7px;'
font = QtGui.QFont()
font.setPointSize(10)
font.setBold(True)
font.setStyleHint(QFont.Monospace)
#     
# self.ui.textfield.textChanged.connect(self.textchanged)
self.ui.setStyleSheet("background-color: #000000;") 
self.ui.text.setStyleSheet(text_style)
self.ui.text.setFont(font)
self.ui.textfield.setStyleSheet(text_style)
self.ui.textfield.setFont(font)
self.ui.status.setStyleSheet(text_style)
self.ui.status.setFont(font)