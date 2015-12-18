import logging
from PyQt5 import QtWidgets
from pyqode.rst.widgets import RstCodeEdit

logging.basicConfig(level=logging.DEBUG)

app = QtWidgets.QApplication([])

editor = RstCodeEdit(color_scheme='default')
editor.file.open('demo.rst')
editor.resize(800, 600)
editor.show()


app.exec_()
