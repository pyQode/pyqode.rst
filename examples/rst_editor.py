import logging
from PyQt5 import QtWidgets
from pyqode.rst.widgets import RstCodeEdit
from pyqode.core.widgets import HtmlPreviewWidget

logging.basicConfig(level=logging.DEBUG)

app = QtWidgets.QApplication([])

editor = RstCodeEdit(color_scheme='qt')
editor.file.open('demo.rst')
editor.resize(800, 600)
editor.show()

preview = HtmlPreviewWidget()
preview.set_editor(editor)
preview.show()

app.exec_()
